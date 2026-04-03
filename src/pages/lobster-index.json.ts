import { getCollection } from 'astro:content';

export async function GET() {
  const posts = await getCollection('posts');

  const index = posts.map((post) => ({
    slug: post.id,
    title: post.data.title,
    description: post.data.description,
    category: post.data.category,
    url: `/posts/${post.data.slug || post.id}/`,
    body: (post.body ?? '').slice(0, 3000),
  }));

  return new Response(JSON.stringify(index), {
    headers: { 'Content-Type': 'application/json' },
  });
}
