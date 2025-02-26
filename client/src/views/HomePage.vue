<template>
  <div class="container">
    <BooksSearch />

    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4 mt-4">
      <div v-for="book in announces" :key="book.id" class="col">
        <BookCard :book="book" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import BooksSearch from "@/layouts/BooksSearch.vue";
import BookCard from "@/components/BookCard.vue";
import type { Book } from "@/api/types";
import { announcesList } from "@/api/announces";

const announces = ref<Book[]>([]);

onMounted(async () => {
  announces.value = await announcesList();
});
</script>

<style scoped lang="scss">
.container {
  padding-top: 20px;
}
</style>
