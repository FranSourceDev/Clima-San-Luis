import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // Configuración para producción
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    // Optimizaciones para producción
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'chart-vendor': ['recharts'],
          'map-vendor': ['leaflet', 'react-leaflet', 'leaflet.heat']
        }
      }
    }
  },
  // Variables de entorno públicas (prefijo VITE_)
  envPrefix: 'VITE_',
  // Configuración del servidor de desarrollo
  server: {
    port: 5173,
    host: true
  }
})
