import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = await getCollection('posts');
  const projects = await getCollection('projects');

  const postItems = posts.map((post) => ({
    title: post.data.title,
    pubDate: post.data.date,
    description: post.data.description,
    link: `/posts/${post.id}/`,
    categories: [post.data.category],
  }));

  const projectItems = projects.map((project) => ({
    title: `[代码库] ${project.data.name}`,
    pubDate: new Date(),
    description: `${project.data.description} — 技术栈: ${project.data.tech.join(', ')}`,
    link: project.data.github || `/code/`,
    categories: ['code', project.data.category],
  }));

  const allItems = [...postItems, ...projectItems].sort(
    (a, b) => b.pubDate.getTime() - a.pubDate.getTime()
  );

  return rss({
    title: "Ocean's Blog",
    description: '找到一个最长的雪坡，滚雪球',
    site: context.site!,
    items: allItems,
  });
}
