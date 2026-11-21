import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const essays = defineCollection({
  loader: glob({ pattern: '*.mdx', base: './src/content/essays' }),
  schema: z.object({
    title: z.string(),
    number: z.number(),
    summary: z.string(),
    drafted: z.coerce.date(),
    revised: z.coerce.date().optional(),
    status: z.enum(['draft', 'published']),
  }),
});

const experiments = defineCollection({
  loader: glob({ pattern: '*.mdx', base: './src/content/experiments' }),
  schema: z.object({
    title: z.string(),
    code: z.string(),
    question: z.string(),
    claim: z.enum(['Forecast', 'Market response', 'Execution']),
    status: z.enum(['Draft', 'Registered', 'Running', 'Positive', 'Null', 'Inconclusive', 'Killed']),
    registered: z.coerce.date().optional(),
    spec: z.string(),
    verdict: z.string(),
  }),
});

export const collections = { essays, experiments };
