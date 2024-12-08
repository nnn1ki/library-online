<script setup>
import { computed, ref } from "vue";

const books = ref([
  { title: "Война и мир", author: "Лев Толстой", imageUrl: null, quantity: 10 },
  { title: "Преступление и наказание", author: "Федор Достоевский", imageUrl: null, quantity: 8 },
  { title: "Гарри Поттер и философский камень", author: "Джоан Роулинг", imageUrl: null, quantity: 15 },
  { title: "Сто лет одиночества", author: "Габриэль Гарсиа Маркес", imageUrl: null, quantity: 6 },
  { title: "Великий Гэтсби", author: "Фрэнсис Скотт Фицджеральд", imageUrl: null, quantity: 12 },
  { title: "Мастер и Маргарита", author: "Михаил Булгаков", imageUrl: null, quantity: 9 },
  { title: "Гордость и предубеждение", author: "Джейн Остин", imageUrl: null, quantity: 7 },
  { title: "Властелин колец", author: "Джон Рональд Руэл Толкин", imageUrl: null, quantity: 11 },
]);

const selectedBooks = ref([]);

const toggleBookSelection = (book) => {
  const index = selectedBooks.value.indexOf(book);
  if (index === -1) {
    selectedBooks.value.push(book);
  } else {
    selectedBooks.value.splice(index, 1);
  }
};

const selectedCount = computed(() => selectedBooks.value.length);

const removeBook = (book) => {
  const index = books.value.indexOf(book);
  if (index !== -1) {
    books.value.splice(index, 1);
  }
  const selectedIndex = selectedBooks.value.indexOf(book);
  if (selectedIndex !== -1) {
    selectedBooks.value.splice(selectedIndex, 1);
  }
};

const clearBasket = () => {
  selectedBooks.value = [];
};
</script>

<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Картинки книг и их описание -->
      <div class="col-9">
        <div v-for="book in books" :key="book.title" class="book-card">
          <div class="row align-items-center">
            <div class="col-auto">
              <input
                class="form-check-input"
                type="checkbox"
                :value="book"
                @change="toggleBookSelection(book)"
                aria-label="Выбрать книгу"
              />
            </div>
            <div class="col-auto">
              <img
                :src="book.imageUrl || 'https://via.placeholder.com/150'"
                :alt="book.title"
                class="book-image img-fluid"
              />
            </div>
            <div class="col">
              <div class="book-info">
                <h6 class="book-title">{{ book.title }}</h6>
                <p class="book-author">{{ book.author }}</p>
                <div class="btn-group">
                  <button class="btn btn-secondary" @click="removeBook(book)">Удалить</button>
                  <button class="btn btn-info">Подробнее</button>
                  <button class="btn btn-primary">Читать онлайн</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Блок с итогами и действиями -->
      <div class="col-3">
        <div class="summary-box">
          <h5 class="summary-title">Итого: {{ selectedCount }} книг</h5>
          <div class="btn-group-vertical w-100">
            <button class="btn btn-success" :disabled="selectedCount === 0">Оформить заказ</button>
            <button class="btn btn-warning">Сохранить в файл</button>
            <button class="btn btn-danger" @click="clearBasket">Очистить корзину</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Основной контейнер для карточек */
.book-card {
  padding: 15px;
  border-bottom: 1px solid #ddd;
  margin-bottom: 15px;
}

/* Стиль для изображения книги */
.book-image {
  max-width: 120px;
  max-height: 160px;
  object-fit: cover;
  border-radius: 8px;
}

/* Информация о книге */
.book-info {
  padding-left: 15px;
}

.book-title {
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.book-author {
  color: #777;
  font-size: 0.9rem;
  margin-bottom: 10px;
}

/* Кнопки в карточке книги */
.btn-group button {
  margin-right: 5px;
}

/* Блок с итогами корзины */
.summary-box {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.summary-title {
  font-size: 1.2rem;
  margin-bottom: 15px;
  font-weight: bold;
}

.btn-group-vertical .btn {
  margin-bottom: 10px;
}

/* Дополнительные стили */
.container-fluid {
  padding: 30px;
}

.row {
  margin-bottom: 30px;
}
</style>
