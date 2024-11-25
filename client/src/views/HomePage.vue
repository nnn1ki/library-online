<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import _ from "lodash";
import { createCanvas, loadImage } from "canvas";

const filters = ref(["Заглавие/Название", "Автор", "Ключевые слова"]);
const andOrFilters = ref(["И", "ИЛИ"]);

const conditions = ref([
  {
    filterType: "Заглавие/Название",
    filterValue: "",
    andOrOperator: null,
  },
]);

function addCondition() {
  conditions.value.push({
    filterType: "Заглавие/Название",
    filterValue: "",
    andOrOperator: "И",
  });
}
function removeCondition(index) {
  conditions.value.splice(index, 1);
}

const books = ref([
  {
    title: "Война и мир",
    author: "Лев Толстой",
    imageUrl: null,
    quantity: 10,
  },
  {
    title: "Преступление и наказание",
    author: "Федор Достоевский",
    imageUrl: null,
    quantity: 8,
  },
  {
    title: "Гарри Поттер и философский камень",
    author: "Джоан Роулинг",
    imageUrl: null,
    quantity: 15,
  },
  {
    title: "Сто лет одиночества",
    author: "Габриэль Гарсиа Маркес",
    imageUrl: null,
    quantity: 6,
  },
  {
    title: "Великий Гэтсби",
    author: "Фрэнсис Скотт Фицджеральд",
    imageUrl: null,
    quantity: 12,
  },
  {
    title: "Мастер и Маргарита",
    author: "Михаил Булгаков",
    imageUrl: null,
    quantity: 9,
  },
  {
    title: "Гордость и предубеждение",
    author: "Джейн Остин",
    imageUrl: null,
    quantity: 7,
  },
  {
    title: "Властелин колец",
    author: "Джон Рональд Руэл Толкин",
    imageUrl: null,
    quantity: 11,
  },
]);

const displayedBooks = ref([]);

onBeforeMount(async () => {
  for (const book of books.value) {
    book.imageUrl = await generateBookImage(book.title, book.author);
  }
  displayedBooks.value = books.value;
});

async function generateBookImage(title, author) {
  const height = 700;
  const width = height * (3 / 4);
  const canvas = createCanvas(width, height);
  const ctx = canvas.getContext("2d");

  // Заливка белым фоном
  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Рисование текста
  ctx.font = "24px Arial";
  ctx.fillStyle = "black";
  ctx.textAlign = "center";
  ctx.fillText(title, canvas.width / 2, canvas.height / 2 - 20);
  ctx.fillText(author, canvas.width / 2, canvas.height / 2 + 20);

  return canvas.toDataURL("image/png");
}

function search() {
  displayedBooks.value = filteredBooks();
}

function filteredBooks() {
  return books.value.filter((book) => {
    let match = false;
    for (const condition of conditions.value) {
      const { filterType, filterValue, andOrOperator } = condition;
      let bookValue = "";
      switch (filterType) {
        case "Заглавие/Название":
          bookValue = book.title;
          break;
        case "Автор":
          bookValue = book.author;
          break;
      }
      if (andOrOperator === null || andOrOperator === "И") {
        match = match && bookValue.includes(filterValue);
      } else {
        match = match || bookValue.includes(filterValue);
      }
    }
    return match;
  });
}
</script>

<template>
  <div class="container-fluid">
    <div style="background: #f4f4ff; margin: 40px 180px 40px 180px">
      <div
        v-for="(condition, index) in conditions"
        :key="index"
        class="row"
        style="padding-bottom: 10px"
      >
        <div class="col-auto" v-if="index > 0">
          <select v-model="condition.andOrOperator" class="form-select">
            <option v-for="andOrFilter in andOrFilters" :key="andOrFilter">
              {{ andOrFilter }}
            </option>
          </select>
        </div>
        <div class="col-auto">
          <select v-model="condition.filterType" class="form-select">
            <option v-for="filter in filters" :key="filter">
              {{ filter }}
            </option>
          </select>
        </div>
        <div class="col">
          <input
            v-model="condition.filterValue"
            type="text"
            class="form-control"
          />
        </div>
        <div class="col-auto" v-if="index > 0">
          <button
            type="button"
            class="btn btn-primary"
            @click="removeCondition(index)"
          >
            <i class="bi bi-x-square"></i>
          </button>
        </div>
      </div>
      <div class="row" style="padding-bottom: 10px">
        <div class="col-auto">
          <button type="button" class="btn btn-primary" @click="addCondition">
            Добавить условие <i class="bi bi-plus-square"></i>
          </button>
        </div>
      </div>
      <div class="row" style="justify-content: center">
        <div class="col-auto">
          <button type="button" class="btn btn-primary" @click="search">
            Поиск <i class="bi bi-search"></i>
          </button>
        </div>
      </div>
    </div>
    <div class="row">
      <div
        class="col-md-3"
        v-for="book in displayedBooks"
        :key="book.title"
        style="margin-bottom: 20px"
      >
        <div class="card">
          <img :src="book.imageUrl" class="card-img-top" :alt="book.title" />
          <div class="card-body">
            <h5 class="card-title">{{ book.title }}</h5>
            <h6 class="card-title">{{ book.author }}</h6>
            <button class="btn btn-info" type="button">
              <i class="bi bi-cart3"></i>
            </button>
            <p class="card-text">{{ book.quantity }} шт</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
</style>