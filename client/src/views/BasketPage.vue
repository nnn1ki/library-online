<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import _ from "lodash";

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
  books.value = [];
  selectedBooks.value = [];
};
</script>

<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col" style="margin: 0 30px 0 10px">
        <div
          class="row"
          v-for="book in books"
          :key="book.title"
          style="padding: 10px 0 10px 0; border-top: 1px solid gray"
        >
          <div
            class="col-auto d-flex justify-content-center align-items-center"
          >
            <input
              class="form-check-input"
              type="checkbox"
              id="checkboxNoLabel"
              :value="book"
              @change="toggleBookSelection(book)"
              aria-label="..."
            />
          </div>
          <div
            class="col-auto image-container d-flex justify-content-center align-items-center"
          >
            <img
              src="https://i.pinimg.com/736x/05/fd/d8/05fdd8079f6e2e7fe66124954346145a.jpg"
              :alt="book.title"
              class="book-image img-thumbnail"
            />
          </div>

          <div class="col">
            <div class="row">
              <div class="col">
                <div class="card-body">
                  <h6 class="card-title">{{ book.title }}</h6>
                  <h7 class="card-title">{{ book.author }}</h7>
                  <h7 class="card-title">{{ book.year }}</h7>
                  <h7 class="card-title">{{ book.catalog }}</h7>
                </div>
              </div>
              <div class="col-auto">
                <div class="row" style="padding-bottom: 3px">
                  <button type="button" class="btn btn-secondary">
                    Читать онлайн
                  </button>
                </div>
                <div class="row" style="padding-bottom: 3px">
                  <button type="button" class="btn btn-secondary">
                    Подробнее
                  </button>
                </div>
                <div class="row">
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
          </div>
        </div>
      </div>
      <div class="col-2">
        <div
          style="
            margin: 0 10px 0 0;
            border: 1px solid gray;
            border-radius: 10px;
            padding: 20px;
          "
        >
          <div class="row">
            <h5>Итого: {{ selectedCount }} к заказу</h5>
          </div>
          <div class="row" style="padding-bottom: 5px">
            <button type="button" class="btn btn-success">
              Оформить заказ
            </button>
          </div>
          <div class="row" style="padding-bottom: 5px">
            <button type="button" class="btn btn-warning">
              Сохранить в файл
            </button>
          </div>
          <div class="row">
            <button type="button" class="btn btn-danger" @click="clearBasket">
              Очистить корзину
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.image-container {
  height: 100px;
}

.book-image {
  width: 100%;
  height: auto;
  max-height: 100%;
}
</style>