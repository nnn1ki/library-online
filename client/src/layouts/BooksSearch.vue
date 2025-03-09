<template>
  <!-- TODO: адаптация под мобилки -->

  <SurfaceCard>
    <form @submit.prevent="search" class="flex flex-col">
      <SelectList
        v-model="library"
        :options="
          libraries.map((x) => {
            return { id: x.id, name: `${x.address} (${x.description})` };
          })
        "
        blank-option="Все библиотеки"
        @change="updateSearchParams"
      />

      <div v-for="(condition, index) in conditions" :key="index" class="filter-condition">
        <SelectList
          v-if="index !== 0"
          v-model="condition.operator"
          :options="[
            { id: '*', name: 'И' },
            { id: '+', name: 'ИЛИ' },
          ]"
          :default-option="'*'"
          @change="updateSearchParams"
        />

        <SelectList
          v-model="condition.scenarioPrefix"
          :options="
            scenarios.map((x) => {
              return {
                id: x.prefix,
                name: `${x.description}`,
              };
            })
          "
          :default-option="defaultScenario"
          @change="updateSearchParams"
        />

        <TextField
          v-model="condition.value"
          placeholder="Введите значение"
          @input="updateSearchParams"
        />

        <StyledButton
          v-if="index !== 0"
          theme="accent"
          class="remove-button"
          @click="removeCondition(index)"
        >
          <XMarkIcon class="button-icon" />
        </StyledButton>
      </div>

      <div class="actions">
        <StyledButton theme="secondary" @click="addCondition"
          >Добавить условие <PlusIcon class="button-icon offset"
        /></StyledButton>
        <StyledButton theme="primary" type="submit"
          >Поиск <MagnifyingGlassIcon class="button-icon offset"
        /></StyledButton>
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
  </SurfaceCard>
</template>

<script setup lang="ts">
import { nextTick, onBeforeMount, ref, computed } from "vue";
import { useRouter } from "vue-router";
import { PlusIcon, MagnifyingGlassIcon, XMarkIcon } from "@heroicons/vue/24/outline";
import { searchBooks } from "@/api/books";
import { scenariosList } from "@/api/scenarios";
import type { Book, Library, Scenario } from "@/api/types";
import { librariesList } from "@/api/libraries";
import SurfaceCard from "@/components/SurfaceCard.vue";
import BookCard from "@/components/BookCard.vue";
import SelectList from "@/components/SelectList.vue";
import StyledButton from "@/components/StyledButton.vue";
import TextField from "@/components/TextField.vue";

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

const results = ref<Book[]>();
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
  [scenarios.value, libraries.value] = await Promise.all([scenariosList(), librariesList()]);

  const queryParam = router.currentRoute.value.query["query"];
  const libraryParam = router.currentRoute.value.query["library"];

  if (typeof libraryParam === "string") {
    const id = parseInt(libraryParam);
    if (!isNaN(id)) {
      library.value = id;
    }
  }

  if (typeof queryParam === "string" && queryParam.length !== 0) {
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
});

// Пагинация найденных книг
const currentPage = ref(1);
const itemsPerPage = 10;

const totalPages = computed(() => {
  return Math.ceil(results.value.length / itemsPerPage);
});

const paginatedResults = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return results.value.slice(start, start + itemsPerPage);
});

const pagesToShow = computed(() => {
  const pages = [];
  const startPage = Math.max(2, currentPage.value - 1);
  const endPage = Math.min(totalPages.value - 1, currentPage.value + 1);

  if (currentPage.value === 5) {
    pages.push(startPage - 2);
  }

  if (startPage > 2) {
    pages.push(startPage - 1);
  }

  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }

  if (endPage < totalPages.value - 1) {
    pages.push(endPage + 1);
  }

  if (totalPages.value - currentPage.value === 4) {
    pages.push(endPage + 2);
  }

  return pages;
});

const showEllipsisLeft = computed(() => {
  return currentPage.value > 5;
});

const showEllipsisRight = computed(() => {
  return currentPage.value < totalPages.value - 4;
});

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
}

function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
}
</script>
