import { fileURLToPath, URL } from "node:url";
import { baseConfig } from "../vite.base.config";
import { defineConfig } from "vite";

export default defineConfig({
  ...baseConfig,
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      "@lib/shared": fileURLToPath(new URL("../shared/src", import.meta.url)),
    },
  },
});
