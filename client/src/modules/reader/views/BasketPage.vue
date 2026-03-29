<template>
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

        <div v-for="book in books" :key="book.id" class="book-card">
          <StyledCheckbox
            :checked="selectedBooks.includes(book.id)"
            @change="toggleBookSelection(book.id)"
            aria-label="Выбрать книгу"
          />
          <BookCard :book="book" :basket-cart="true" />
        </div>
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
            <div v-html="sanitizedBookList"></div>
          <hr />
        <p>Всего книг: {{ selectedBooks.length }}</p>

        <label>
          <input type="radio" value="txt" v-model="fileFormat" />
          Текстовый файл (.txt)
        </label>

        <label>
          <input type="radio" value="docx" v-model="fileFormat" />
          Word файл (.docx)
        </label>

        <label>
          <input type="radio" value="pdf" v-model="fileFormat" />
          PDF файл (.pdf)
        </label>

        <div class="save-buttons">
          <StyledButton theme="primary" @click="saveBooks"> Сохранить </StyledButton>
          <StyledButton theme="accent" @click="saveModalOpen = false"> Отмена </StyledButton>
        </div>
      </ModalDialog>

      <!-- Модальное окно авторизации -->
      <NotAllowedBanner v-model="authModalOpen" />
    </SurfaceCard>
  </div>
</template>

<script setup lang="ts">
import type { Book } from "@api/types";
import NotAllowedBanner from "@reader/components/NotAllowedBanner.vue";
import { useBasketStore } from "@reader/store/basket";
import { useAuthStore } from "@core/store/auth";
import { storeToRefs } from "pinia";
import { useOrderStore } from "@reader/store/orderStore";
import { computed, ref, watch } from "vue";
import { Document, Packer, Paragraph, TextRun } from "docx";
import { useRouter } from "vue-router";
import ModalDialog from "@components/ModalDialog.vue";
import SurfaceCard from "@components/SurfaceCard.vue";
import StyledButton from "@components/StyledButton.vue";
import BookCard from "@reader/components/BookCard.vue";
import StyledCheckbox from "@components/StyledCheckbox.vue";
import { jsPDF } from "jspdf";
import DOMPurify from "dompurify";

const router = useRouter();
const basketStore = useBasketStore();
const orderStore = useOrderStore();
const auth = useAuthStore();

const { books } = storeToRefs(basketStore);
const selectedBooks = ref<string[]>([]);

const selectedBooksText = computed(() => {
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

const allSelected = computed(() => {
  return books.value.length > 0 && selectedBooks.value.length === books.value.length;
});

watch(books, () => {
  const bookIds = new Set(books.value.map((b) => b.id));
  selectedBooks.value = selectedBooks.value.filter((item) => bookIds.has(item));
});

const bookList = computed(() => {
  const allMapped = selectedBooks.value
    .map((bookId) => books.value.find((item) => item.id === bookId))
    .filter((book): book is Book => book !== undefined);

  const allSorted = allMapped.sort((a, b) => a.title[0].localeCompare(b.title[0]));

  const russianBooks = allSorted.filter((b) => b.language[0] === "rus");
  const englishBooks = allSorted.filter((b) => b.language[0] === "eng");
  const otherBooks = allSorted.filter(
    (b) => b.language[0] !== "rus" && b.language[0] !== "eng"
  );

  const combinedBooks = [...russianBooks, ...englishBooks, ...otherBooks];

  return combinedBooks
    .map((book, index) => {
      const brief = book.brief;

      if (brief !== null) {
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

const sanitizedBookList = computed(() => DOMPurify.sanitize(bookList.value));

async function saveBooks() {
  const today = new Date();
  const defaultFileName = `Заказ Литературы_${today.toISOString().split("T")[0]}`;
  const filename = prompt("Введите имя файла:", defaultFileName);

  if (filename === null || filename.trim() === "") {
    return;
  }

  saveModalOpen.value = false;

  try {
    if (fileFormat.value === "txt") {
      await saveAsText(filename);
    } else if (fileFormat.value === "docx") {
      await saveAsDocx(filename);
    } else if (fileFormat.value === "pdf") {
      await saveAsPdf(filename);
    } else {
      throw new Error("Неподдерживаемый формат файла.");
    }
  } catch (error) {
    alert(`Ошибка: ${error}`);
  }
}

async function saveAsText(filename: string) {
  const content = bookList.value.split("<hr>").join("\n");
  const blob = new Blob([content], { type: "text/plain" });
  downloadBlob(blob, filename);
}

async function saveAsDocx(filename: string) {
  const content = bookList.value.split("<hr>");
  const doc = new Document({
    sections: [
      {
        properties: {},
        children: [
          new Paragraph({
            children: [new TextRun("Список литературы:")],
          }),
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

  const blob = await Packer.toBlob(doc);
  downloadBlob(blob, filename);
}

async function saveAsPdf(filename: string) {
  const pdf = new jsPDF();
  await loadFont(pdf);

  const content = bookList.value
    .split("<hr>")
    .map((item) => item.trim())
    .filter((item) => item !== "");

  pdf.text("Список литературы:", 10, 10);

  let yOffset = 20;
  const pageHeight = pdf.internal.pageSize.getHeight();
  const lineHeight = 10;
  const marginBottom = 10;

  content.forEach((item) => {
    const lines = pdf.splitTextToSize(item, 190);
    const blockHeight = lines.length * lineHeight;

    if (yOffset + blockHeight > pageHeight - marginBottom) {
      pdf.addPage();
      yOffset = 10;
    }

    pdf.text(lines, 10, yOffset);
    yOffset += blockHeight;
  });

  pdf.save(filename);
}

async function loadFont(pdf: jsPDF) {
  const fontName = "TimesNewRoman";
  const response = await fetch(`/${fontName}.ttf`);

  if (!response.ok) {
    throw new Error(`Не удалось загрузить шрифт: ${response.statusText}`);
  }

  const fontData = await response.arrayBuffer();
  const uint8Array = new Uint8Array(fontData);

  const base64 = btoa(
    uint8Array.reduce((data, byte) => data + String.fromCharCode(byte), "")
  );

  pdf.addFileToVFS(`${fontName}.ttf`, base64);
  pdf.addFont(`${fontName}.ttf`, fontName, "normal");
  pdf.setFont(fontName);
  pdf.setFontSize(14);
}

function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
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
@use "@assets/styles/breakpoints.scss" as *;

.container {
  padding-top: 20px;

  display: flex;
  flex-direction: row;
  align-items: start;
  justify-content: center;
  gap: 3rem;

  @include media-max-lg {
    flex-direction: column;
    align-items: center;
    width: 90%;
  }
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
  flex-direction: column;
  align-items: center;
  gap: 1rem;

  @include media-lg {
    flex-direction: row;
  }
}

hr {
  margin: 0.5rem 0;
  border-width: 1px;
  border-color: var(--color-text-950);
}

.sticky {
  position: sticky;
  top: 1rem;

  @include media-max-lg {
    width: 100%;
    bottom: 1rem;
    top: 0;
    border-style: solid;
    border-radius: 0.5rem;
    border-width: 1px;
    border-color: var(--color-text-300);
  }
}

.options-card {
  display: flex;
  flex-direction: column;
  row-gap: 1rem;
  min-width: 14rem;

  @include media-max-lg {
    row-gap: 0.5rem;
    h5 {
      margin: 0;
    }
  }
}

.save-buttons {
  margin-top: 1rem;
  display: flex;
  flex-direction: row;
  column-gap: 1rem;
}

:deep(.modal-dialog) {
  width: 80%;

  @include media-max-lg {
    width: 100%;
  }
}
</style>