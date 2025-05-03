import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      '@lib/shared': fileURLToPath(new URL('../shared/src', import.meta.url)),
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        api: "modern-compiler",
      },
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
      },
      "/admin": {
        target: "http://localhost:8000",
      },
      "/static": {
        target: "http://localhost:8000",
      },
      "/media": {
        target: "http://localhost:8000",
      },
    },
  },
});
