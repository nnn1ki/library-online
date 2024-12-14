<script setup>
import { ref, computed } from 'vue'

const books = ref([
  { title: 'Война и мир', author: 'Лев Толстой', quantity: 10 },
  { title: 'Преступление и наказание', author: 'Федор Достоевский', quantity: 8 },
  { title: 'Гарри Поттер и философский камень', author: 'Джоан Роулинг', quantity: 15 },
  { title: 'Сто лет одиночества', author: 'Габриэль Гарсиа Маркес', quantity: 6 },
  { title: 'Великий Гэтсби', author: 'Фрэнсис Скотт Фицджеральд', quantity: 12 },
  { title: 'Мастер и Маргарита', author: 'Михаил Булгаков', quantity: 9 },
  { title: 'Гордость и предубеждение', author: 'Джейн Остин', quantity: 7 },
  { title: 'Властелин колец', author: 'Джон Рональд Руэл Толкин', quantity: 11 },
])

const selectedBooks = ref([])

const toggleBookSelection = (book) => {
  const index = selectedBooks.value.indexOf(book)
  if (index === -1) {
    selectedBooks.value.push(book)
  } else {
    selectedBooks.value.splice(index, 1)
  }
}

const selectedCount = computed(() => selectedBooks.value.length)

const removeBook = (book) => {
  const index = books.value.indexOf(book)
  if (index !== -1) {
    books.value.splice(index, 1)
  }
  const selectedIndex = selectedBooks.value.indexOf(book)
  if (selectedIndex !== -1) {
    selectedBooks.value.splice(selectedIndex, 1)
  }
}

const clearBasket = () => {
  books.value = []
  selectedBooks.value = []
}
</script>

<template>
  <div class="container mt-4">
    <div class="row">
      <div class="col-md-8">
        <div class="list-group">
          <div 
            v-for="book in books" 
            :key="book.title" 
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            <div class="d-flex align-items-center">
              <input
                type="checkbox"
                class="form-check-input me-3"
                :value="book"
                @change="toggleBookSelection(book)"
              />
              <div class="me-3">
                <img
                  src="https://via.placeholder.com/50"
                  :alt="book.title"
                  class="img-fluid"
                  style="max-height: 50px; object-fit: cover;"
                />
              </div>
              <div>
                <h5 class="mb-1">{{ book.title }}</h5>
                <p class="mb-1">{{ book.author }}</p>
                <small>{{ book.quantity }} книг в наличии</small>
              </div>
            </div>
            <button 
              type="button" 
              class="btn btn-danger"
              @click="removeBook(book)"
            >
              Удалить
            </button>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Итого: {{ selectedCount }} к заказу</h5>
            <button class="btn btn-success w-100 mb-2">Оформить заказ</button>
            <button class="btn btn-warning w-100 mb-2">Сохранить в файл</button>
            <button class="btn btn-danger w-100" @click="clearBasket">Очистить корзину</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
img {
  max-width: 100%;
  height: auto;
}
</style>
