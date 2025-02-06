<template>
  <div class="search-filter p-3 border rounded bg-light">
    <!-- Библиотеки -->
    <span>Библиотека</span>
    <select v-model="library" class="form-select form-select-sm" @change="updateSearchParams">
      <option :value="undefined"></option>
      <option v-for="lib in libraries" :key="lib.id" :value="lib.id">
        {{ lib.description }} ({{ lib.address }})
      </option>
    </select>

    <form @submit.prevent="search">
      <!-- Сценарии -->
      <div v-for="(condition, index) in conditions" :key="index" class="filter-condition mb-3 mt-3">
        <div class="d-flex align-items-center gap-2">
          <!-- Операторы И/ИЛИ -->
          <select
            v-if="index !== 0"
            v-model="condition.operator"
            class="form-select form-select-sm"
            @change="updateSearchParams"
          >
            <option
              v-for="[description, operator] in [
                ['И', '*'],
                ['ИЛИ', '+'],
              ]"
              :key="operator"
              :value="operator"
            >
              {{ description }}
            </option>
          </select>

          <!-- Тип фильтра -->
          <select
            v-model="condition.scenarioPrefix"
            class="form-select form-select-sm"
            @change="updateSearchParams"
          >
            <option v-for="scenario in scenarios" :key="scenario.prefix" :value="scenario.prefix">
              {{ scenario.description }}
            </option>
          </select>

          <!-- Значение фильтра -->
          <input
            v-model="condition.value"
            type="text"
            class="form-control form-control-sm"
            placeholder="Введите значение"
            @input="updateSearchParams"
          />

          <!-- Удалить условие -->
          <button
            v-if="index !== 0"
            type="button"
            class="btn btn-danger btn-sm"
            @click="removeCondition(index)"
          >
            <i class="bi bi-x-square"></i>
          </button>
        </div>
      </div>

      <!-- Кнопки -->
      <div class="actions d-flex justify-content-between">
        <button type="button" class="btn btn-outline-primary btn-sm" @click="addCondition">
          Добавить условие <i class="bi bi-plus-square"></i>
        </button>
        <button type="submit" class="btn btn-success btn-sm">
          Поиск <i class="bi bi-search"></i>
        </button>
      </div>
    </form>

    <!-- Результаты поиска -->
    <div v-if="loading" class="mt-3">Загрузка...</div>
    <div v-else class="mt-3">
      <h3>Результаты поиска</h3>
      <ul v-if="results.length" class="list-group">
        <li v-for="book in results" :key="book.id" class="list-group-item">
          <BookCard :book="book" />
        </li>
      </ul>
      <div v-else class="alert alert-warning mt-2">Книги не найдены</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onBeforeMount, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { searchBooks } from "@/api/books";
import { scenariosList } from "@/api/scenarios";
import type { Book, Library, Scenario } from "@/api/types";
import { librariesList } from "@/api/libraries";
import BookCard from "@/components/BookCard.vue";

// Состояния
const router = useRouter();

const scenarios = ref<Scenario[]>([]);
const libraries = ref<Library[]>([]);

const defaultScenario = "T=";

const library = ref<number>();
const conditions = ref<
  {
    scenarioPrefix: string;
    operator: "+" | "*";
    value: string;
  }[]
>([
  {
    scenarioPrefix: defaultScenario,
    operator: "*",
    value: "",
  },
]);

const results = ref<Book[]>([]);
const loading = ref(false);

// Функции для управления фильтрами
function addCondition() {
  conditions.value.push({
    scenarioPrefix: defaultScenario,
    operator: "*",
    value: "",
  });
}

function removeCondition(index: number) {
  conditions.value.splice(index, 1);
  nextTick(updateSearchParams);
}

function buildQuery(): string {
  const query = conditions.value
    .filter((condition) => condition.value !== "")
    .map((condition) => `${condition.operator}(${condition.scenarioPrefix}${condition.value}$)`)
    .reduce((a, b) => a + b, "");
  return query.substring(1);
}

function updateSearchParams() {
  router.push({
    path: "",
    query: {
      query: buildQuery(),
      library: library.value,
    },
  });
}

// Поиск книг
async function search() {
  loading.value = true;
  try {
    const query = buildQuery();
    results.value = await searchBooks(query, library.value);
  } catch (error) {
    console.error("Ошибка поиска:", error);
    results.value = [];
  } finally {
    loading.value = false;
  }
}

onBeforeMount(async () => {
  const queryParam = router.currentRoute.value.query["query"];
  const libraryParam = router.currentRoute.value.query["library"];

  if (typeof libraryParam === "string") {
    const id = parseInt(libraryParam);
    if (!isNaN(id)) {
      library.value = id;
    }
  }

  if (typeof queryParam === "string") {
    conditions.value = queryParam
      .split(")")
      .map((item) => item.replace("(", "").replace("$", ""))
      .filter((item) => item !== "")
      .map((item) => {
        let operator = item.charAt(0);
        if (operator == "*" || operator == "+") {
          item = item.substring(1);
        } else {
          operator = "*";
        }

        const [prefix, value] = item.split("=");

        return {
          operator: operator as "*" | "+",
          scenarioPrefix: `${prefix}=`,
          value: value,
        };
      });

    search();
  }

  [scenarios.value, libraries.value] = await Promise.all([scenariosList(), librariesList()]);
});
</script>
