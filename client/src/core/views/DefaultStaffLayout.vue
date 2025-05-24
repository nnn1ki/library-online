<template>
  <div class="app">
    <PageHeader />
    <main>
      <div>
        <RouterView />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import PageHeader from "@modules/staff/components/PageHeader.vue";
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
