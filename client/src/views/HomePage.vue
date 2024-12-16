<script setup>
import { ref, watch, onMounted } from "vue";
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

// Стейт для корзины
const basket = ref([]);

// Функция для добавления книги в корзину
function addToBasket(book) {
  const existingBook = basket.value.find(item => item.title === book.title);
  if (existingBook) return; // Если книга уже в корзине, ничего не делать

  basket.value.push({ ...book }); // Добавляем книгу в корзину
  localStorage.setItem('basket', JSON.stringify(basket.value)); // Сохраняем корзину в localStorage
}

// Функция для фильтрации книг на основе значений из формы поиска
function filterBooks() {
  const { title, author } = searchQuery.value;
  filteredBooks.value = books.value.filter(book => {
    const titleMatch = book.title.toLowerCase().includes(title.toLowerCase());
    const authorMatch = book.author.toLowerCase().includes(author.toLowerCase());
    return titleMatch && authorMatch; // Книга подходит, если совпадает хотя бы одно из условий
  });
}

// Функция для сброса фильтра (показывать все книги)
function resetFilter() {
  searchQuery.value = { title: "", author: "" };
  filteredBooks.value = [...books.value]; // Показываем все книги
}

// Действие при клике на кнопку поиска
function onSearchClick() {
  filterBooks();
}

// Функция для загрузки корзины из localStorage
function loadBasket() {
  const savedBasket = localStorage.getItem('basket');
  if (savedBasket) {
    basket.value = JSON.parse(savedBasket); // Загрузите корзину при старте
  }
}

// Наблюдаем за изменением query параметров в URL, если они есть
const route = useRoute();
watch(() => route.query, () => {
  searchQuery.value.title = route.query.title || "";
  searchQuery.value.author = route.query.author || "";
  filterBooks();
}, { immediate: true });

// Загружаем корзину при монтировании компонента
onMounted(() => {
  loadBasket();
});
</script>

<template>
  <div class="container mt-4">
    <!-- Компонент фильтра -->
    <SearchFilter v-model="searchQuery" @search="onSearchClick" @reset="resetFilter" />

    <!-- Сетка книг (Bootstrap grid system) -->
    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4 mt-4">
      <div 
        v-for="book in filteredBooks"
        :key="book.title"
        class="col"
      >
        <Card 
          :title="book.title"
          :author="book.author"
          :imageUrl="book.imageUrl"
          :quantity="book.quantity"
          :addToBasket="addToBasket"
          :isInBasket="basket.some(item => item.title === book.title)"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Убираем паддинг у контейнера */
.container {
  padding: 20px;
}

/* Можно добавить любые дополнительные стили для карточек, если нужно */
</style>