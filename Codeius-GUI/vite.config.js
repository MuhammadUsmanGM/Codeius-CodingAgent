import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true, // Automatically open the browser
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // Default Flask backend port
        changeOrigin: true,
        secure: false,
      },
    },
  },
  build: {
    rollupOptions: {
      external: ['tslib'],
    },
  },
})
