import vue from '@vitejs/plugin-vue'

export const baseConfig = {
    plugins: [vue()],
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
}
