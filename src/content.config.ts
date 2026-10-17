import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Portfolio pieces. One markdown file = one case study at /work/<file-name>.
const work = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/work' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    client: z.string().default('Ashah Meets World'),
    year: z.coerce.string(),
    skill: z.enum(['Creative Direction', 'Ecosystem Design', 'Cultural Leadership', 'Campaign Marketing']),
    role: z.string().optional(),
    cover: z.string(),
    coverRatio: z.enum(['landscape', 'portrait']).default('landscape'),
    gallery: z.array(z.object({ image: z.string(), caption: z.string().optional() })).default([]),
    link: z.string().optional(),
    featured: z.boolean().default(true),
    order: z.number().default(100),
    draft: z.boolean().default(false),
  }),
});

// Sales pages. One markdown file = one offer page at /<file-name>.
const offers = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/offers' }),
  schema: z.object({
    title: z.string(),
    eyebrow: z.string().optional(),
    headline: z.string(),
    subhead: z.string(),
    problem: z.object({ title: z.string(), points: z.array(z.object({ label: z.string(), text: z.string() })), thoughtsTitle: z.string().optional(), thoughts: z.array(z.object({ q: z.string(), a: z.string() })).default([]) }),
    promise: z.object({ title: z.string(), text: z.string(), outcomes: z.array(z.string()) }),
    tiers: z.array(z.object({
      stage: z.string(),
      name: z.string(),
      price: z.string(),
      text: z.string(),
      includes: z.array(z.string()).default([]),
      highlight: z.boolean().default(false),
    })),
    steps: z.array(z.object({ title: z.string(), text: z.string() })).default([]),
    transformation: z.object({ title: z.string(), before: z.array(z.string()), after: z.array(z.string()) }).optional(),
    fit: z.object({ yes: z.array(z.string()), no: z.array(z.string()) }),
    objections: z.array(z.object({ q: z.string(), a: z.string(), group: z.enum(['habit', 'anxiety']).default('anxiety') })).default([]),
    assurances: z.object({ title: z.string(), text: z.string().optional(), items: z.array(z.string()) }).optional(),
    founding: z.object({ title: z.string(), text: z.string(), perks: z.array(z.string()).default([]) }).optional(),
    faq: z.array(z.object({ q: z.string(), a: z.string() })).default([]),
    cta: z.object({ title: z.string(), text: z.string(), label: z.string() }),
    draft: z.boolean().default(false),
  }),
});

// Field Notes. Each one is a cover image + a link to the post.
const notes = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/notes' }),
  schema: z.object({
    title: z.string(),
    number: z.coerce.string(),
    cover: z.string(),
    link: z.string().optional(),
    date: z.coerce.date().optional(),
  }),
});

export const collections = { work, offers, notes };
