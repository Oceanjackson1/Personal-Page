import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    slug: z.string().optional(),
    description: z.string(),
    category: z.enum(['perp-dex', 'prediction-market', 'product-growth', 'web3', 'ai', 'stories', 'travel', 'reflections']),
    date: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
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

const skills = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/skills' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    category: z.enum(['development', 'workflow', 'research', 'writing', 'devops', 'other']),
    source: z.enum(['community', 'official']).default('community'),
    sourceUrl: z.string().optional(),
    author: z.string().optional(),
    tags: z.array(z.string()).default([]),
    date: z.coerce.date(),
  }),
});

const aiShares = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/ai-shares' }),
  schema: z.object({
    title: z.string(),
    slug: z.string().optional(),
    description: z.string(),
    date: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    source: z.string().optional(),
  }),
});

export const collections = { posts, projects, skills, aiShares };
