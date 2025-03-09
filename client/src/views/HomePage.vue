<template>
  <div class="container">
    <BooksSearch />

    <div class="announces">
      <div v-for="book in announces" :key="book.id" class="announce-book">
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

.announces {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
}

.announce-book {
  flex-basis: 20%;
}
</style>
