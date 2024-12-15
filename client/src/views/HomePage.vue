<script setup>
import { ref, watch } from "vue";
import { useRoute } from "vue-router"; // Для работы с параметрами маршрута
import SearchFilter from "../components/SearchFilter.vue"; // Импорт компонента фильтра
import Card from "../components/Card.vue"; // Импорт компонента карточки книги
import { announcesItems } from '@/api/announces.js'
import Announces from "@/components/Announces.vue";

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

const {picture, description, link} = announcesItems;
console.log('announcesItems', announcesItems); 

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

// Функция для загрузки корзины из localStorage
function loadBasket() {
  const savedBasket = localStorage.getItem('basket');
  if (savedBasket) {
    basket.value = JSON.parse(savedBasket); // Загрузите корзину при старте
  }
}

// Загружаем корзину при монтировании компонента
onMounted(() => {
  loadBasket();
});


</script>

<template>
  <div class="container mt-4">
    <!-- Компонент фильтра -->
    <SearchFilter v-model="searchQuery" @search="onSearchClick" @reset="resetFilter" />
    <!-- список новинок -->
     <h3>Новинки</h3>
     <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4 mt-4">
      <!-- <Announces/> //нет доступа к данным со стороннего пользователя --> 
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
