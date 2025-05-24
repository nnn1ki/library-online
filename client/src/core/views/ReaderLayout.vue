<template>
    <div class="app">
      <PageHeader />
  
      <main>
        <div>
          <RouterView />
        </div>
      </main>
    </div>
  
    <PageFooter class="footer" />
  </template>
  
  <script setup lang="ts">
  import PageHeader from "@reader/components/PageHeader.vue";
  import PageFooter from "@reader/components/PageFooter.vue";
  import { RouterView } from "vue-router";
  </script>
  
  <style scoped lang="scss">
  .app {
    display: flex;
    flex-direction: column;
    min-height: 100vh; /* Обеспечивает, чтобы футер всегда был внизу страницы */
  }
  
  main {
    flex: 1;
  }
  
  .footer {
    margin-top: 2rem;
  }
  </style>