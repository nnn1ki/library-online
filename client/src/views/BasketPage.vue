<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Картинки книг и их описание -->
      <div class="col-9">
        <div v-if="books.length !== 0" class="row align-items-center select-all">
          <div class="col-auto">
            <input class="form-check-input" type="checkbox" :checked="allSelected" @change="toggleSelectAll"
              aria-label="Выбрать все книги" />
          </div>
          <div class="col">
            <button class="btn btn-primary" @click="toggleSelectAll">
              {{ allSelected ? "Снять выделение" : "Выбрать все" }}
            </button>
          </div>
        </div>
        <div v-for="book in books" :key="book.description" class="book-card">
          <div class="row align-items-center">
            <div class="col-auto">
              <input class="form-check-input" type="checkbox" :value="book" :checked="selectedBooks.includes(book.id)"
                @change="toggleBookSelection(book.id)" aria-label="Выбрать книгу" />
            </div>
            <div class="col-auto">
              <img v-if="book.cover !== null" :src="book.cover" class="book-image img-fluid" />
              <i v-else class="book-image bi bi-image"></i>
            </div>
            <div class="col">
              <div class="book-info">
                <h6 class="book-title">{{ book.title[0] }} ({{ book.year }})</h6>
                <p class="book-author">{{ book.author.join(", ") }}</p>
                <div class="btn-group">
                  <button class="btn btn-secondary" @click="basketStore.removeBook(book)">
                    Удалить
                  </button>
                  <button class="btn btn-info" @click="modalBook = book; isModalVisible = true">Подробнее</button>
                  <button class="btn btn-primary">Читать онлайн</button>
                </div>
              </div>
            </div>
          </div>
          <AboutBookDialog v-if="modalBook == book" :book="book" v-model="isModalVisible" />
        </div>
      </div>

      <!-- Блок с итогами и действиями -->
      <div class="col-3">
        <div class="summary-box">
          <h5 class="summary-title">Итого: {{ selectedBooks.length }} книг</h5>
          <div class="btn-group-vertical w-100">
            <button class="btn btn-success" :disabled="books.length === 0 || selectedBooks.length === 0">
              Оформить заказ
            </button>
            <button class="btn btn-warning" :disabled="books.length === 0 || selectedBooks.length === 0"
              data-bs-toggle="modal" data-bs-target="#confirmationModal">
              Сохранить в файл
            </button>
            <button class="btn btn-danger" :disabled="books.length === 0" @click="basketStore.clearBooks()">
              Очистить корзину
            </button>
          </div>
        </div>
      </div>

      <!-- Модальное окно для подтверждения сохранения -->
      <div>
        <div class="modal fade" id="confirmationModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
          aria-labelledby="confirmationModalLabel" aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="confirmationModalLabel">
                  Подтверждение сохранения
                </h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
              </div>
              <div class="modal-body">
                <p>Вы хотите распечатать книги:</p>
                <p v-html="bookList"></p>
                <p>Всего книг: {{ selectedBooks.length }}</p>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                  Отмена
                </button>
                <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="saveBooks">
                  Сохранить
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Book } from "@/api/types";
import AboutBookDialog from "@/components/AboutBookDialog.vue";
import { useBasketStore } from "@/stores/basket";
import { storeToRefs } from "pinia";
import { computed, ref, onMounted, watch } from "vue";

const basketStore = useBasketStore();

const { books } = storeToRefs(basketStore);
const selectedBooks = ref<string[]>([]);

const isModalVisible = ref(false);
const modalBook = ref<Book>();



function toggleBookSelection(bookId: string) {
  const index = selectedBooks.value.indexOf(bookId);
  if (index === -1) {
    selectedBooks.value.push(bookId);
  } else {
    selectedBooks.value.splice(index, 1);
  }
};

function toggleSelectAll() {
  if (allSelected.value) {
    selectedBooks.value = [];
  } else {
    selectedBooks.value = books.value.map((b) => b.id);
  }
};

// Вычисляемое свойство для проверки, выбраны ли все книги
const allSelected = computed(() => {
  return (
    books.value.length > 0 && selectedBooks.value.length === books.value.length
  );
});

watch(books, () => {
  selectedBooks.value = selectedBooks.value.filter((item) => books.value.filter((b) => b.id === item).length !== 0);
});

// Расчитываемое свойство для книг в модальном окне
const bookList = computed(() => {
  return selectedBooks.value
    .map((bookId) => books.value.find((item) => item.id == bookId))
    .map((book, index) => `${index + 1}. ${book?.description} (${book?.year})`)
    .join("<br>");
});

// Функция для сохранения книг в текстовый файл
function saveBooks() {
  // Формируем текстовое содержимое
  const content = selectedBooks.value
    .map((bookId) => books.value.find((item) => item.id == bookId))
    .map((book, index) => `${index + 1}. ${book?.description} (${book?.year})`)
    .join("\n"); // Используем \n для переноса строк

  // Создаём имя файла по умолчанию
  const today = new Date();
  const defaultFileName = `Заказ Литературы_${today.toISOString().split('T')[0]}.txt`;

  // Запрашиваем имя файла у пользователя
  const fileName = prompt("Введите имя файла:", defaultFileName) || defaultFileName;

  const blob = new Blob([content], { type: 'text/plain' }); // Создаём Blob с типом текст
  const url = URL.createObjectURL(blob); // Создаём URL для Blob

  const a = document.createElement('a'); // Создаём элемент <a>
  a.href = url; // Устанавливаем href как URL Blob
  a.download = fileName; // Устанавливаем имя файла для скачивания
  document.body.appendChild(a); // Добавляем элемент в DOM
  a.click(); // Эмулируем клик для скачивания
  document.body.removeChild(a); // Удаляем элемент из DOM
  URL.revokeObjectURL(url); // Освобождаем память
};

</script>

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
  font-size: 120px;
  text-align: center;
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

/* Кнопка и чекбокс для "Выбрать все книги" */
.select-all {
  padding: 15px;
  margin-bottom: 0 !important;
}

/* Дополнительные стили */
.container-fluid {
  padding: 30px;
}

.row {
  margin-bottom: 30px;
}
</style>