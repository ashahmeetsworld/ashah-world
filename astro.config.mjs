// @ts-check
import { defineConfig } from 'astro/config';

// SITE_URL / BASE_PATH are set by the GitHub Pages workflow.
// With a custom domain (e.g. ashahmeetsworld.com) BASE_PATH stays "/".
export default defineConfig({
  site: process.env.SITE_URL || 'https://example.com',
  base: process.env.BASE_PATH || '/',
  trailingSlash: 'ignore',
  build: { format: process.env.BUILD_FORMAT === 'file' ? 'file' : 'directory' },
});
