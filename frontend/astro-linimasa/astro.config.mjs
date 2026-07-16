import { defineConfig } from 'astro/config';
import preact from '@astrojs/preact';
import tailwind from '@astrojs/tailwind';
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',
  adapter: node({ mode: 'standalone' }),
  integrations: [preact(), tailwind()],
  server: { port: 4321, host: '0.0.0.0' },
  vite: {
    build: { cssMinify: true }
  }
});
