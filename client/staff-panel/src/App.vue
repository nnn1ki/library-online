<template>
  <div class="app">
    <main>
      <div>
        <RouterView />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">

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
