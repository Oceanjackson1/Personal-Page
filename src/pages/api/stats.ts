import type { APIRoute } from 'astro';

export const prerender = false;

const AMPLITUDE_HOST = 'https://amplitude.com';
const PV_EVENT = '[Amplitude] Page Viewed';

// The free Amplitude plan only retains ~12 months of data. Querying a start
// date older than the retention cutoff makes the Dashboard API error out, so
// we always look back a fixed window that stays safely inside retention.
const LOOKBACK_DAYS = 360;

// Historical counts from before Amplitude/retention window (busuanzi era).
// Added on top so the displayed numbers stay continuous.
const HISTORY_UV_OFFSET = 22;
const HISTORY_PV_OFFSET = 32;

function toYmd(d: Date): string {
  const y = d.getUTCFullYear();
  const m = String(d.getUTCMonth() + 1).padStart(2, '0');
  const day = String(d.getUTCDate()).padStart(2, '0');
  return `${y}${m}${day}`;
}

async function amplitudeGET(path: string, auth: string): Promise<any> {
  const res = await fetch(`${AMPLITUDE_HOST}${path}`, {
    headers: { Authorization: `Basic ${auth}` },
  });
  if (!res.ok) {
    const body = await res.text().catch(() => '');
    const endpoint = path.split('?')[0];
    throw new Error(`Amplitude ${endpoint} → ${res.status} ${body.slice(0, 300)}`);
  }
  return res.json();
}

// Total unique visitors = sum of daily NEW users over the window. A user is
// only "new" once, so summing daily-new equals the deduped visitor count.
async function fetchNewUsers(auth: string, start: string, end: string): Promise<number> {
  const data = await amplitudeGET(
    `/api/2/users?start=${start}&end=${end}&m=new&i=1`,
    auth,
  );
  const series: number[][] = data?.data?.series ?? [];
  return series.flat().reduce<number>((s, n) => s + (Number(n) || 0), 0);
}

// Total page views = sum of the Page Viewed event totals over the window.
async function fetchPageViews(auth: string, start: string, end: string): Promise<number> {
  const e = encodeURIComponent(JSON.stringify({ event_type: PV_EVENT }));
  const data = await amplitudeGET(
    `/api/2/events/segmentation?e=${e}&start=${start}&end=${end}&m=totals&i=1`,
    auth,
  );
  const series: number[][] = data?.data?.series ?? [];
  return series.flat().reduce<number>((s, n) => s + (Number(n) || 0), 0);
}

export const GET: APIRoute = async () => {
  const apiKey = process.env.AMPLITUDE_API_KEY ?? import.meta.env.AMPLITUDE_API_KEY;
  const secretKey = process.env.AMPLITUDE_SECRET_KEY ?? import.meta.env.AMPLITUDE_SECRET_KEY;

  if (!apiKey || !secretKey) {
    return new Response(
      JSON.stringify({ error: 'missing_credentials' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } },
    );
  }

  const auth = Buffer.from(`${apiKey}:${secretKey}`).toString('base64');

  const now = new Date();
  const end = toYmd(now);
  const start = toYmd(new Date(now.getTime() - LOOKBACK_DAYS * 86400 * 1000));

  try {
    const [uvRaw, pvRaw] = await Promise.all([
      fetchNewUsers(auth, start, end),
      fetchPageViews(auth, start, end),
    ]);
    const uv = uvRaw + HISTORY_UV_OFFSET;
    const pv = pvRaw + HISTORY_PV_OFFSET;

    return new Response(
      JSON.stringify({ uv, pv }),
      {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400',
        },
      },
    );
  } catch (err) {
    const message = (err as Error).message || String(err);
    // Surfaces in Vercel runtime logs for diagnosis (bad secret key, date
    // restriction, rate limit, etc.).
    console.error('[/api/stats] Amplitude request failed:', message);
    return new Response(
      JSON.stringify({ error: message }),
      { status: 502, headers: { 'Content-Type': 'application/json' } },
    );
  }
};
