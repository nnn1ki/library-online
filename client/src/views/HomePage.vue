<script setup>
import { ref, watch } from "vue";
import { useRoute } from "vue-router"; // Для работы с параметрами маршрута
import SearchFilter from "../components/SearchFilter.vue"; // Импорт компонента фильтра
import Card from "../components/Card.vue"; // Импорт компонента карточки книги

// Массив всех книг
const books = ref([
  { title: "Война и мир", author: "Лев Толстой", imageUrl: null, quantity: 10 },
  { title: "Преступление и наказание", author: "Федор Достоевский", imageUrl: null, quantity: 8 },
  { title: "Гарри Поттер и философский камень", author: "Джоан Роулинг", imageUrl: null, quantity: 15 },
  { title: "Сто лет одиночества", author: "Габриэль Гарсиа Маркес", imageUrl: null, quantity: 6 },
  { title: "Великий Гэтсби", author: "Фрэнсис Скотт Фицджеральд", imageUrl: null, quantity: 12 },
  { title: "Мастер и Маргарита", author: "Михаил Булгаков", imageUrl: null, quantity: 9 },
  { title: "Гордость и предубеждение", author: "Джейн Остин", imageUrl: null, quantity: 7 },
  { title: "Властелин колец", author: "Джон Рональд Руэл Толкин", imageUrl: null, quantity: 11 }
]);

// Массив фильтруемых книг
const filteredBooks = ref([...books.value]);

// Стейт для поисковых значений
const searchQuery = ref({
  title: "",
  author: ""
});

// Функция для фильтрации книг на основе значений из формы поиска
function filterBooks() {
  filteredBooks.value = books.value.filter(book => {
    const titleMatch = book.title.toLowerCase().includes(searchQuery.value.title.toLowerCase());
    const authorMatch = book.author.toLowerCase().includes(searchQuery.value.author.toLowerCase());
    return titleMatch && authorMatch; // Книга подходит, если совпадает хотя бы одно из условий
  });
}

// Функция для сброса фильтра (показывать все книги)
function resetFilter() {
  searchQuery.value.title = "";
  searchQuery.value.author = "";
  filteredBooks.value = [...books.value]; // Показываем все книги
}

// Действие при клике на кнопку поиска
function onSearchClick() {
  filterBooks();
}

// Наблюдаем за изменением query параметров в URL, если они есть
const route = useRoute();
watch(() => route.query, filterBooks, { immediate: true });
</script>

<template>
  <div class="container">
    <!-- Компонент фильтра -->
    <SearchFilter v-model:searchQuery="searchQuery" @search="onSearchClick" @reset="resetFilter" />

    <!-- Сетка книг -->
    <div class="books-grid">
      <Card
        v-for="book in filteredBooks"
        :key="book.title"
        :title="book.title"
        :author="book.author"
        :imageUrl="book.imageUrl"
        :quantity="book.quantity"
      />
    </div>
  </div>
</template>

<style scoped>
.container {
  padding: 20px;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}
</style>
