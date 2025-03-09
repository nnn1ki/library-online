<template>
  <div class="container">
    <BooksSearch />

<<<<<<< HEAD
    <div class="announces">
      <div v-for="book in announces" :key="book.id" class="announce-book">
        <BookCard :book="book" />
=======
    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4 mt-4">
      <div v-for="book in announces" :key="book.id" class="col">
        <AnnouncementBookCard :book="book" />
>>>>>>> main
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
<<<<<<< HEAD
import BooksSearch from "@/layouts/BooksSearch.vue";
import BookCard from "@/components/BookCard.vue";
=======
import SearchFilter from "@/layouts/BooksSearch.vue";
import AnnouncementBookCard from "@/components/AnnouncementBookCard.vue";
>>>>>>> main
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
