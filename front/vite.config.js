import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  },
  server: {
    host: '127.0.0.1',
    port: 5173,
    proxy: {
      '/chat': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/casas': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/scraping': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
})

