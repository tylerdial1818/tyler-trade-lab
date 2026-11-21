import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://tylerdial.dev',
  base: '/labs',
  integrations: [mdx()],
  markdown: { smartypants: true },
});
