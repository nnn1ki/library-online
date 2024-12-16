<script setup>
import { computed, ref, onMounted } from "vue";

const books = ref([]);
const selectedBooks = ref([]);

// Вычисляемое свойство для проверки, пуста ли корзина
const isBasketEmpty = computed(() => {
  return books.value.length === 0; // Возвращает true, если корзина пуста
});

// Функция для загрузки выбранных книг из localStorage
const loadBasket = () => {
  const basket = localStorage.getItem("basket");
  if (basket) {
    books.value = JSON.parse(basket);
  }
};

const toggleBookSelection = (book) => {
  const index = selectedBooks.value.indexOf(book);
  if (index === -1) {
    selectedBooks.value.push(book);
  } else {
    selectedBooks.value.splice(index, 1);
  }
};

// Функция для выбора/снятия выбора всех книг
const toggleSelectAll = () => {
  if (allSelected.value) {
    selectedBooks.value = [];
  } else {
    selectedBooks.value = [...books.value];
  }
};

// Вычисляемое свойство для проверки, выбраны ли все книги
const allSelected = computed(() => {
  return (
    books.value.length > 0 && selectedBooks.value.length === books.value.length
  );
});

const selectedCount = computed(() => selectedBooks.value.length);

const removeBook = (book) => {
  const index = books.value.indexOf(book);
  if (index !== -1) {
    books.value.splice(index, 1); // Удалить книгу из списка книг
  }
  const selectedIndex = selectedBooks.value.indexOf(book);
  if (selectedIndex !== -1) {
    selectedBooks.value.splice(selectedIndex, 1); // Удалить книгу из выбранных
  }
  // Обновление localStorage после удаления книги
  localStorage.setItem("basket", JSON.stringify(books.value)); // Сохраняем оставшиеся книги
};

const clearBasket = () => {
  books.value = [];
  selectedBooks.value = [];
  localStorage.removeItem("basket");
};

// Загрузка выбранных книг при монтировании компонента
onMounted(() => {
  loadBasket();
});

// Расчитываемое свойство для книг в модальном окне
const bookList = computed(() => {
  return selectedBooks.value
    .map((book, index) => `${index + 1}. ${book.title} — ${book.author}`)
    .join("<br>");
});

// Функция для сохранения книг в текстовый файл
const saveBooks = () => {
  // Формируем текстовое содержимое
  const content = selectedBooks.value
    .map((book, index) => `${index + 1}. ${book.title} — ${book.author}`)
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

<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Картинки книг и их описание -->
      <div class="col-9">
        <div v-if="!isBasketEmpty" class="row align-items-center select-all">
          <div class="col-auto">
            <input
              class="form-check-input"
              type="checkbox"
              :checked="allSelected"
              @change="toggleSelectAll"
              aria-label="Выбрать все книги"
            />
          </div>
          <div class="col">
            <button class="btn btn-primary" @click="toggleSelectAll">
              {{ allSelected ? "Снять выделение" : "Выбрать все" }}
            </button>
          </div>
        </div>
        <div v-for="book in books" :key="book.title" class="book-card">
          <div class="row align-items-center">
            <div class="col-auto">
              <input
                class="form-check-input"
                type="checkbox"
                :value="book"
                :checked="selectedBooks.includes(book)"
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
                  <button class="btn btn-secondary" @click="removeBook(book)">
                    Удалить
                  </button>
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
            <button
              class="btn btn-success"
              :disabled="isBasketEmpty || selectedCount === 0"
            >
              Оформить заказ
            </button>
            <button
              class="btn btn-warning"
              :disabled="isBasketEmpty || selectedCount === 0"
              data-bs-toggle="modal"
              data-bs-target="#confirmationModal"
            >
              Сохранить в файл
            </button>
            <button
              class="btn btn-danger"
              :disabled="isBasketEmpty"
              @click="clearBasket"
            >
              Очистить корзину
            </button>
          </div>
        </div>
      </div>

      <!-- Модальное окно для подтверждения сохранения -->
      <div>
        <div
          class="modal fade"
          id="confirmationModal"
          data-bs-backdrop="static"
          data-bs-keyboard="false"
          tabindex="-1"
          aria-labelledby="confirmationModalLabel"
          aria-hidden="true"
        >
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="confirmationModalLabel">
                  Подтверждение сохранения
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Закрыть"
                ></button>
              </div>
              <div class="modal-body">
                <p>Вы хотите распечатать книги:</p>
                <p v-html="bookList"></p>
                <p>Всего книг: {{ selectedCount }}</p>
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Отмена
                </button>
                <button
                  type="button"
                  class="btn btn-primary"
                  data-bs-dismiss="modal"
                  @click="saveBooks"
                >
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