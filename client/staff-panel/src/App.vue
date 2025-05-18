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
import { RouterView } from "vue-router";
import PageHeader from "@/layouts/PageHeader.vue";
</script>

<style scoped lang="scss">
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
}

.footer {
  margin-top: 2rem;
}
</style>
