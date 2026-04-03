import { getCollection } from 'astro:content';

export async function GET() {
  const posts = await getCollection('posts');
  const projects = await getCollection('projects');

  const postIndex = posts.map((post) => ({
    type: 'post' as const,
    slug: post.id,
    title: post.data.title,
    description: post.data.description,
    category: post.data.category,
    url: `/posts/${post.data.slug || post.id}/`,
    body: (post.body ?? '').slice(0, 3000),
  }));

  const projectIndex = projects.map((project) => ({
    type: 'project' as const,
    slug: project.id,
    title: project.data.name,
    description: project.data.description,
    category: project.data.category,
    url: project.data.github || `/code/${project.data.category}/`,
    body: `项目名称：${project.data.name}\n简介：${project.data.description}\n技术栈：${project.data.tech.join('、')}\n分类：${project.data.category === 'infra' ? '数据基建' : '产品与交易工具'}${project.data.github ? `\nGitHub：${project.data.github}` : ''}`,
  }));

  return new Response(JSON.stringify([...postIndex, ...projectIndex]), {
    headers: { 'Content-Type': 'application/json' },
  });
}
