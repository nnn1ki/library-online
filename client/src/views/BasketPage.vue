<template>
  <!-- TODO: адаптация под мобилки -->

  <div class="container">
    <SurfaceCard v-if="books.length !== 0">
      <div class="books">
        <div class="select-all">
          <StyledCheckbox
            :checked="allSelected"
            @change="toggleSelectAll"
            aria-label="Выбрать все книги"
          />
          <StyledButton theme="secondary" @click="toggleSelectAll">{{
            allSelected ? "Снять выделение" : "Выбрать все"
          }}</StyledButton>
        </div>

        <div v-for="book in books" :key="book.description" class="book-card">
          <StyledCheckbox
            :checked="selectedBooks.includes(book.id)"
            @change="toggleBookSelection(book.id)"
            aria-label="Выбрать книгу"
          />
          <BookCard :book="book" :show-cart="false" :basket-cart="true" />
        </div>

        <AboutBookDialog v-if="modalBook !== undefined" :book="modalBook" v-model="bookModalOpen" />
      </div>
    </SurfaceCard>

    <SurfaceCard class="sticky">
      <div class="options-card">
        <h5>Итого: {{ selectedBooksText }}</h5>

        <StyledButton
          theme="primary"
          :disabled="books.length === 0 || selectedBooks.length === 0"
          @click="onCreateOrderClick"
        >
          Оформить заказ
        </StyledButton>

        <StyledButton
          theme="secondary"
          :disabled="books.length === 0 || selectedBooks.length === 0"
          @click="saveModalOpen = true"
        >
          Сохранить в файл
        </StyledButton>

        <StyledButton
          theme="accent"
          :disabled="books.length === 0"
          @click="basketStore.clearBooks()"
        >
          Очистить корзину
        </StyledButton>
      </div>

      <!-- Модальное окно для подтверждения сохранения -->
      <ModalDialog v-model="saveModalOpen">
        <p>Вы хотите распечатать книги:</p>
        <hr />
        <div v-html="bookList"></div>
        <hr />
        <p>Всего книг: {{ selectedBooks.length }}</p>

        <label>
          <input type="radio" value="txt" v-model="fileFormat" checked />
          Текстовый файл (.txt)
        </label>

        <label>
          <input type="radio" value="docx" v-model="fileFormat" />
          Word файл (.docx)
        </label>

        <label>
          <input disabled="true" type="radio" value="pdf" v-model="fileFormat" />
          PDF файл (.pdf)
        </label>

        <div class="save-buttons">
          <StyledButton theme="primary" @click="saveBooks"> Сохранить </StyledButton>
          <StyledButton theme="accent" @click="saveModalOpen = false"> Отмена </StyledButton>
        </div>
      </ModalDialog>

      <!-- Модальное окно авторзиации -->
      <NotAllowedBanner v-model="authModalOpen" />
    </SurfaceCard>
  </div>
</template>

<script setup lang="ts">
import type { Book } from "@/api/types";
import AboutBookDialog from "@/components/AboutBookDialog.vue";
import NotAllowedBanner from "@/layouts/NotAllowedBanner.vue";
import { useBasketStore } from "@/stores/basket";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { useOrderStore } from "@/stores/orderStore";
import { computed, ref, watch } from "vue";
import { Document, Packer, Paragraph, TextRun } from "docx";
import { useRouter } from "vue-router";
import ModalDialog from "@/components/ModalDialog.vue";
import SurfaceCard from "@/components/SurfaceCard.vue";
import StyledButton from "@/components/StyledButton.vue";
import BookCard from "@/components/BookCard.vue";
import StyledCheckbox from "@/components/StyledCheckbox.vue";

const router = useRouter();
const basketStore = useBasketStore();
const orderStore = useOrderStore();
const auth = useAuthStore();

const { books } = storeToRefs(basketStore);
const selectedBooks = ref<string[]>([]);
const selectedBooksText = computed(() => {
  // Прекрасный русский язык
  const amount = selectedBooks.value.length;
  const lastDigit = amount % 10;

  if (amount >= 10 && amount <= 19) {
    return `${amount} книг`;
  } else if (lastDigit === 1) {
    return `${amount} книга`;
  } else if (lastDigit >= 2 && lastDigit <= 4) {
    return `${amount} книги`;
  } else {
    return `${amount} книг`;
  }
});

const bookModalOpen = ref(false);
const modalBook = ref<Book>();

const saveModalOpen = ref(false);
const authModalOpen = ref(false);

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

// Функция для сохранения книг
function saveBooks() {
  saveModalOpen.value = false;

  if (fileFormat.value === "txt") {
    // Сохранение в текстовый файл
    // Получаем текстовое содержимое из уже сформированного bookList
    const content = bookList.value.split("<hr>").join("\n"); // Разбиваем текст по "<hr>" и объединяем строки с новой строки

    // Создаём имя файла по умолчанию
    const blob = new Blob([content], { type: "text/plain" }); // Создаём Blob с типом текст

    // Создаём имя файла по умолчанию
    const today = new Date();
    const defaultFileName = `Заказ Литературы_${today.toISOString().split("T")[0]}.txt`;

    downloadBlob(blob, defaultFileName);
  } else if (fileFormat.value === "docx") {
    // Сохранение в .docx файл
    // Получаем текстовое содержимое из уже сформированного bookList
    const content = bookList.value.split("<hr>"); // Разбиваем текст по "<hr>"

    const doc = new Document({
      sections: [
        {
          properties: {},
          children: [
            new Paragraph({
              children: [new TextRun("Список литературы:")],
            }),
            // Добавляем каждую книгу на следующую строку
            ...content.map(
              (item) =>
                new Paragraph({
                  children: [new TextRun(item)],
                })
            ),
          ],
        },
      ],
    });

    Packer.toBlob(doc).then((blob) => {
      const today = new Date();
      const defaultFileName = `Заказ Литературы_${today.toISOString().split("T")[0]}.docx`;

      downloadBlob(blob, defaultFileName);
    });
  } else if (fileFormat.value === "pdf") {
    throw Error("TODO");
  }
}

function downloadBlob(blob: Blob, defaultFilename: string) {
  // Запрашиваем имя файла у пользователя
  const filename = prompt("Введите имя файла:", defaultFilename);

  // Если пользователь нажал "Отмена" или оставил поле пустым, выходим из функции
  if (filename === null || filename.trim() === "") {
    return; // Прерываем выполнение функции
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
  if (!auth.isAuthenticated) {
    authModalOpen.value = true;
    return;
  }

  orderStore.selectedBooks = basketStore.books.filter((b) => {
    return selectedBooks.value.some((selectedBook) => selectedBook === b.id);
  });

  router.push("/order");
}
</script>

<style scoped lang="scss">
.container {
  padding-top: 20px;

  display: flex;
  flex-direction: row;
  column-gap: 3rem;
  align-items: start;
  justify-content: center;
}

.books {
  display: flex;
  flex-direction: column;
  row-gap: 1rem;
}

.select-all {
  display: flex;
  flex-direction: row;
  align-items: center;
  column-gap: 1rem;
}

.book-card {
  display: flex;
  flex-direction: row;
  align-items: center;
  column-gap: 1rem;
}

hr {
  margin: 0.5rem 0;
  border-width: 1px;
  border-color: var(--color-text-950);
}

.sticky {
  position: sticky;
  top: 1rem;
}

.options-card {
  display: flex;
  flex-direction: column;
  row-gap: 1rem;
  min-width: 14rem;
}

.save-buttons {
  margin-top: 1rem;
  display: flex;
  flex-direction: row;
  column-gap: 1rem;
}
</style>
