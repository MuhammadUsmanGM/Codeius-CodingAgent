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
        target: 'http://127.0.0.1:8080', // Default Flask backend port
        changeOrigin: true,
        secure: false,
      },
    },
  },
})