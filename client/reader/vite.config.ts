import { fileURLToPath, URL } from "node:url";
import { baseConfig } from "../vite.base.config";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  ...baseConfig,
    resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      "@lib/shared": fileURLToPath(new URL("../shared/src", import.meta.url)),
      "@reader": fileURLToPath(new URL("../reader/src", import.meta.url)),
      "@staff": fileURLToPath(new URL("../staff-panel/src", import.meta.url)),
    },
  },
});
