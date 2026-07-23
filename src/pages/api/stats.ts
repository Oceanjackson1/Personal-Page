import type { APIRoute } from 'astro';

export const prerender = false;

const AMPLITUDE_HOST = 'https://amplitude.com';
const AMPLITUDE_START = '20250512';
const PV_EVENT = '[Amplitude] Page Viewed';
const HISTORY_UV_OFFSET = 22;
const HISTORY_PV_OFFSET = 32;
const CHUNK_DAYS = 300;

function toYmd(d: Date): string {
  const y = d.getUTCFullYear();
  const m = String(d.getUTCMonth() + 1).padStart(2, '0');
  const day = String(d.getUTCDate()).padStart(2, '0');
  return `${y}${m}${day}`;
}

function ymdToDate(ymd: string): Date {
  return new Date(Date.UTC(
    Number(ymd.slice(0, 4)),
    Number(ymd.slice(4, 6)) - 1,
    Number(ymd.slice(6, 8)),
  ));
}

function chunkRange(startYmd: string, endYmd: string, chunkDays: number): Array<[string, string]> {
  const chunks: Array<[string, string]> = [];
  const end = ymdToDate(endYmd);
  let cur = ymdToDate(startYmd);
  while (cur.getTime() <= end.getTime()) {
    const chunkEnd = new Date(cur);
    chunkEnd.setUTCDate(chunkEnd.getUTCDate() + chunkDays - 1);
    if (chunkEnd.getTime() > end.getTime()) chunkEnd.setTime(end.getTime());
    chunks.push([toYmd(cur), toYmd(chunkEnd)]);
    cur = new Date(chunkEnd);
    cur.setUTCDate(cur.getUTCDate() + 1);
  }
  return chunks;
}

async function amplitudeGET(path: string, auth: string): Promise<any> {
  const res = await fetch(`${AMPLITUDE_HOST}${path}`, {
    headers: { Authorization: `Basic ${auth}` },
  });
  if (!res.ok) {
    throw new Error(`Amplitude ${path} → ${res.status}`);
  }
  return res.json();
}

async function fetchNewUsers(auth: string, start: string, end: string): Promise<number> {
  const data = await amplitudeGET(`/api/2/users?start=${start}&end=${end}`, auth);
  const series: number[][] = data?.data?.series ?? [];
  const labels: string[] = data?.data?.seriesLabels ?? [];
  const newIdx = labels.findIndex((l) => l.toLowerCase().includes('new'));
  const pickIdx = newIdx >= 0 ? newIdx : 0;
  const daily = series[pickIdx] ?? [];
  return daily.reduce<number>((s, n) => s + (Number(n) || 0), 0);
}

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
  const chunks = chunkRange(AMPLITUDE_START, toYmd(new Date()), CHUNK_DAYS);

  try {
    const results = await Promise.all(
      chunks.map(async ([start, end]) => {
        const [uv, pv] = await Promise.all([
          fetchNewUsers(auth, start, end),
          fetchPageViews(auth, start, end),
        ]);
        return { uv, pv };
      }),
    );
    const uv = results.reduce((s, r) => s + r.uv, 0) + HISTORY_UV_OFFSET;
    const pv = results.reduce((s, r) => s + r.pv, 0) + HISTORY_PV_OFFSET;

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
    return new Response(
      JSON.stringify({ error: (err as Error).message }),
      { status: 502, headers: { 'Content-Type': 'application/json' } },
    );
  }
};
