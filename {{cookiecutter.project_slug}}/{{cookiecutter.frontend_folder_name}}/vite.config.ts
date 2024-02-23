import path from 'path'

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default () => {
  const serverConfig = {
    host: true,
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000',
    },
  }

   return defineConfig({
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        fastui: '@pydantic/fastui',
      },
    },
    server: serverConfig,
    preview: serverConfig,
    build: {
      sourcemap: true,
      outDir: '../dist',
      // we don't need hashes in URLs, we the URL will change when we release a new version
      rollupOptions: {
        output: {
          entryFileNames: `assets/[name].js`,
          chunkFileNames: `assets/[name].js`,
          assetFileNames: `assets/[name].[ext]`,
        },
      },
    },
  })
}
