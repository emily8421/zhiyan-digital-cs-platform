import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const backendProxyTarget = process.env.ZYCS_BACKEND_PROXY_URL ?? 'http://127.0.0.1:8000';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5174,
    proxy: {
      '/api': backendProxyTarget
    }
  }
});
