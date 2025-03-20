import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from '@tailwindcss/vite'
import * as fs from "fs";

import path from 'path';

const resolvePath = (p: string) => path.resolve(__dirname, p);

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 443,
    host: "0.0.0.0",
    hmr: {
        host: 'tg-mini-app.local',
        port: 443,
    },
    https: {
      key: fs.readFileSync('./.cert/localhost-key.pem'),
      cert: fs.readFileSync('./.cert/localhost.pem'),
    },
  },
  resolve: {
    alias: {
        '@components': resolvePath('src/components'),
        '@shared': resolvePath('src/shared'),
        '@pages': resolvePath('src/pages'),
        '@variables': resolvePath('src/shared/styles/variables.module.scss'),
        '@mixins': resolvePath('src/shared/styles/mixins.scss'),
        '@images': resolvePath('public/images'),
        "@widgets": resolvePath("src/widgets")
    },
},
})

// Все одинаковые, просты мыслят по разному (С) Максим Бильчук
