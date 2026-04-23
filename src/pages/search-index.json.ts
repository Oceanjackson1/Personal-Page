import { getCollection } from 'astro:content';

export async function GET() {
  const posts = await getCollection('posts');
  const projects = await getCollection('projects');
  const aiShares = await getCollection('aiShares');

  const index = [
    ...posts.map((post) => ({
      type: 'post' as const,
      slug: post.id,
      title: post.data.title,
      description: post.data.description,
      category: post.data.category,
      date: post.data.date.toISOString().slice(0, 10),
      url: `/posts/${post.id}/`,
    })),
    ...projects.map((project) => ({
      type: 'project' as const,
      slug: project.id,
      title: project.data.name,
      description: project.data.description,
      category: project.data.category,
      date: '',
      url: `/code/${project.data.category}/`,
    })),
    ...aiShares.map((share) => ({
      type: 'ai-share' as const,
      slug: share.id,
      title: share.data.title,
      description: share.data.description,
      category: 'ai-share',
      date: share.data.date.toISOString().slice(0, 10),
      url: `/ai-shares/${share.data.slug || share.id}/`,
    })),
  ];

  return new Response(JSON.stringify(index), {
    headers: { 'Content-Type': 'application/json' },
  });
}
