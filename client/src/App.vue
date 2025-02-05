<template>
  <div class="app">
    <Header></Header>

    <main>
      <div>
        <RouterView />
      </div>
    </main>
  </div>
  <Footer />
</template>

<script setup lang="ts">
import Header from "@/layouts/Header.vue";
import Footer from "@/layouts/Footer.vue";
import { RouterView } from "vue-router";
</script>

<style scoped lang="scss">
/* Корневой контейнер для всей страницы */
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  /* Обеспечивает, чтобы футер всегда был внизу страницы */
}

main {
  flex: 1;
  /* Это заставляет основной контент занять все доступное пространство */
  padding: 20px;
}
</style>
