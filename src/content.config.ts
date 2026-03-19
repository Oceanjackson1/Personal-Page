import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    category: z.enum(['perp-dex', 'prediction-market', 'product-growth', 'web3', 'ai', 'stories', 'travel', 'reflections']),
    date: z.coerce.date(),
    featured: z.boolean().default(false),
  }),
});

const projects = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/projects' }),
  schema: z.object({
    name: z.string(),
    description: z.string(),
    category: z.enum(['infra', 'products']),
    tech: z.array(z.string()),
    github: z.string().optional(),
    demo: z.string().optional(),
    order: z.number().default(0),
  }),
});

export const collections = { posts, projects };
