<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Картинки книг и их описание -->
      <div class="col-9">
        <div v-if="books.length !== 0" class="row align-items-center select-all">
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
        <div v-for="book in books" :key="book.description" class="book-card">
          <div class="row align-items-center">
            <div class="col-auto">
              <input
                class="form-check-input"
                type="checkbox"
                :value="book"
                :checked="selectedBooks.includes(book.id)"
                @change="toggleBookSelection(book.id)"
                aria-label="Выбрать книгу"
              />
            </div>
            <div class="col-auto">
              <img v-if="book.cover !== null" :src="book.cover" class="book-image img-fluid" />
              <i v-else class="book-image bi bi-image"></i>
            </div>
            <div class="col">
              <div class="book-info">
                <h6 class="book-title">
                  {{ book.title[0] }}
                  <span class="other-titles" v-if="book.title.length > 1"
                    >({{ book.title.slice(1).join(", ") }})</span
                  >
                  ({{ book.year }})
                </h6>
                <p v-if="book.author.length > 0" class="book-author">
                  {{ book.author.join(", ") }}
                </p>
                <p v-else class="book-author">{{ book.collective.join(", ") }}</p>
                <div class="btn-group">
                  <button class="btn btn-secondary" @click="basketStore.removeBook(book)">
                    Удалить
                  </button>
                  <button
                    class="btn btn-info"
                    @click="
                      modalBook = book;
                      isModalVisible = true;
                    "
                  >
                    Подробнее
                  </button>
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
            <button
              class="btn btn-success"
              :disabled="books.length === 0 || selectedBooks.length === 0"
              @click="onCreateOrderClick"
            >
              Оформить заказ
            </button>
            <button
              class="btn btn-warning"
              :disabled="books.length === 0 || selectedBooks.length === 0"
              data-bs-toggle="modal"
              data-bs-target="#confirmationModal"
            >
              Сохранить в файл
            </button>
            <button
              class="btn btn-danger"
              :disabled="books.length === 0"
              @click="basketStore.clearBooks()"
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
        >
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="confirmationModalLabel">Подтверждение сохранения</h5>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Закрыть"
                ></button>
              </div>
              <div class="modal-body">
                <p>Вы хотите распечатать книги:</p>
                <hr />
                <!-- Разделительная полоска -->
                <div v-html="bookList"></div>
                <hr />
                <!-- Разделительная полоска -->
                <p>Всего книг: {{ selectedBooks.length }}</p>
              </div>
              <div class="modal-footer">
                <label for="fileFormat">Выберите формат файла:</label>
                <select id="fileFormat" v-model="fileFormat">
                  <option value="txt">Текстовый файл (.txt)</option>
                  <option value="docx">Word файл (.docx)</option>
                  <option value="pdf">PDF файл (.pdf)</option>
                </select>
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="saveBooks">Сохранить</button>
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
import { useOrderStore } from "@/stores/orderStore";
import { computed, ref, watch } from "vue";
import { Document, Packer, Paragraph, TextRun } from "docx";
import { useRouter } from "vue-router";
import { jsPDF } from "jspdf";

const router = useRouter();
const basketStore = useBasketStore();
const orderStore = useOrderStore();

const { books } = storeToRefs(basketStore);
const selectedBooks = ref<string[]>([]);

const isModalVisible = ref(false);
const modalBook = ref<Book>();

const fileFormat = ref<"txt" | "docx" | "pdf">("txt");

function toggleBookSelection(bookId: string) {
  const index = selectedBooks.value.indexOf(bookId);
  if (index === -1) {
    selectedBooks.value.push(bookId);
  } else {
    selectedBooks.value.splice(index, 1);
  }
}

function toggleSelectAll() {
  if (allSelected.value) {
    selectedBooks.value = [];
  } else {
    selectedBooks.value = books.value.map((b) => b.id);
  }
}

// Вычисляемое свойство для проверки, выбраны ли все книги
const allSelected = computed(() => {
  return books.value.length > 0 && selectedBooks.value.length === books.value.length;
});

watch(books, () => {
  selectedBooks.value = selectedBooks.value.filter(
    (item) => books.value.filter((b) => b.id === item).length !== 0
  );
});

// Расчитываемое свойство для книг в модальном окне
const bookList = computed(() => {
  // Разъединяем книги на русском от книг на английском и фильтруем по названиям по алфавиту
  const sortBooks = (language?: string) => {
    const filteredBooks = selectedBooks.value
      .map((bookId) => books.value.find((item) => item.id == bookId)!)
      .filter((book) => (language !== undefined ? book.language[0] === language : true));

    return filteredBooks.sort((a, b) => {
      const titleA = a.title[0];
      const titleB = b.title[0];

      return titleA.localeCompare(titleB);
    });
  };

  // Получаем отсортированные списки книг на русском и английском языках
  const russianBooks = sortBooks("rus");
  const englishBooks = sortBooks("eng");
  const otherBooks = sortBooks().filter(
    (book) => book.language[0] !== "rus" && book.language[0] !== "eng"
  );

  // Объединяем оба списка
  const combinedBooks = [...russianBooks, ...englishBooks, ...otherBooks];

  // Формируем список литературы
  return combinedBooks
    .map((book, index) => {
      // const mainTitle = book.title[0];
      // const authors = book.author;
      // const year = book.year;
      // const city = book.city;
      // const publisher = book.publisher;
      // const subject = book.subject;
      // return `${index + 1}. ${authors[0]} ${mainTitle} : ${subject} / ${authors.join(", ")} - ${city} : ${publisher}, ${year}.`;

      // Используем brief, т.к. он содержит нужную информацию
      const brief = book.brief;

      if (brief !== null) {
        // Извлекаем часть до разделителя ": ил. –" или "– ISBN"
        const endIndex1 = brief.indexOf(": ил. –");
        const endIndex2 = brief.indexOf("– ISBN");

        let briefWithoutPages = brief;

        if (endIndex1 !== -1) {
          briefWithoutPages = brief.substring(0, endIndex1).trim();
        } else if (endIndex2 !== -1) {
          briefWithoutPages = brief.substring(0, endIndex2).trim();
        }
        return `${index + 1}. ${briefWithoutPages}`;
      } else {
        return `${index + 1}. ${book.description}`;
      }
    })
    .join("<hr>");
});

async function saveBooks() {
  // Получаем текущую дату для формирования имени файла
  const today = new Date();
  const defaultFileName = `Заказ Литературы_${today.toISOString().split("T")[0]}`;

  try {
    // Проверяем выбранный формат файла и вызываем соответствующую функцию
    if (fileFormat.value === "txt") {
      await saveAsText(defaultFileName);
    } else if (fileFormat.value === "docx") {
      await saveAsDocx(defaultFileName);
    } else if (fileFormat.value === "pdf") {
      await saveAsPdf(defaultFileName);
    } else {
      throw new Error("Неподдерживаемый формат файла.");
    }
  } catch (error) {
    alert(`Ошибка: ${error.message}`);
  }
}

async function saveAsText(defaultFileName) {
  // Формируем содержимое для текстового файла
  const content = bookList.value.split("<hr>").join("\n");
  const blob = new Blob([content], { type: "text/plain" });
  downloadBlob(blob, defaultFileName);
}

async function saveAsDocx(defaultFileName) {
  // Формируем содержимое для Word документа
  const content = bookList.value.split("<hr>");
  const doc = new Document({
    sections: [
      {
        properties: {},
        children: [
          new Paragraph({
            children: [new TextRun("Список литературы:")],
          }),
          ...content.map(item => new Paragraph({
            children: [new TextRun(item)],
          })),
        ],
      },
    ],
  });

  const blob = await Packer.toBlob(doc);
  downloadBlob(blob, defaultFileName);
}

async function saveAsPdf(defaultFileName) {
  const pdf = new jsPDF();
  await loadFont(pdf);

  const filename = prompt("Введите имя файла для PDF:", defaultFileName);
  if (filename === null || filename.trim() === "") {
    return;
  }
  // Формируем содержимое для PDF документа
  const content = bookList.value.split("<hr>").map(item => item.trim()).filter(item => item !== "");

  pdf.text("Список литературы:", 10, 10);
  
  // Устанавливаем начальную позицию для текста
  let yOffset = 20;

  content.forEach((item) => {
    // Разбиваем текст на строки, чтобы они не выходили за пределы страницы
    const lines = pdf.splitTextToSize(item, 190); // 190 - ширина текста
    pdf.text(lines, 10, yOffset);
    yOffset += lines.length * 10; // Увеличиваем смещение по Y на количество строк
  });

  pdf.save(filename);
}

// Функция для загрузки шрифта
async function loadFont(pdf) {
  try {
    const fontName = "Tinos-Regular";
    const response = await fetch(`src/views/${fontName}.ttf`);
    const fontData = await response.arrayBuffer();
    const uint8Array = new Uint8Array(fontData);
    
    // Преобразование Uint8Array в строку
    let binaryString = '';
    for (let i = 0; i < uint8Array.length; i++) {
      binaryString += String.fromCharCode(uint8Array[i]);
    }

    pdf.addFileToVFS(`${fontName}.ttf`, btoa(binaryString));
    pdf.addFont(`${fontName}.ttf`, fontName, "normal");
    pdf.setFont(fontName);
    pdf.setFontSize(14);
  } catch (error) {
    console.error('Ошибка загрузки шрифта:', error);
  }
}

function downloadBlob(blob, defaultFilename) {
  // Запрашиваем имя файла у пользователя
  const filename = prompt("Введите имя файла:", defaultFilename);

  // Если пользователь нажал "Отмена" или оставил поле пустым, выходим из функции
  if (filename === null || filename.trim() === "") {
    return;
  }

  const url = URL.createObjectURL(blob); // Создаём URL для Blob
  const a = document.createElement("a"); // Создаём элемент <a>
  a.href = url; // Устанавливаем href как URL Blob
  a.download = filename; // Устанавливаем имя файла для скачивания
  document.body.appendChild(a); // Добавляем элемент в DOM
  a.click(); // Эмулируем клик для скачивания
  document.body.removeChild(a); // Удаляем элемент из DOM
  URL.revokeObjectURL(url); // Освобождаем память
}

async function onCreateOrderClick() {
  orderStore.selectedBooks = basketStore.books.filter((b) => {
    return selectedBooks.value.some((selectedBook) => selectedBook === b.id);
  });

  router.push("/order");
}
</script>

<style scoped lang="scss">
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

.book-title .other-titles {
  font-style: italic;
}

.book-author {
  color: #777;
  font-size: 0.9rem;
  margin-bottom: 10px;
}

hr {
  margin: 10px 0;
  border-width: 3px;
  border-color: #000000;
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
