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
        <div class="filter-parameter">
          <SelectList
            class="and-or"
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
        </div>

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
    <div v-if="loading" class="loading">
      <strong> Загрузка... </strong>
      <LoadingSpinner />
    </div>
    <div v-else class="flex flex-col">
      <h3>Результаты поиска</h3>
      <div v-if="paginatedResults.length > 0" class="books-list">
        <BookCard v-for="book in paginatedResults" :key="book.id" :book="book" />
      </div>
      <div v-else class="not-found">Книги не найдены</div>

      <div v-if="pageEntries.length > 1" class="pagination">
        <span>Отображено {{ paginatedResults.length }} из {{ results.length }} результатов</span>
        <nav class="pagination-slider" aria-label="Навигация по страницам">
          <template v-for="page in pageEntries" v-bind:key="page">
            <button
              v-if="page !== -1"
              :class="{
                left: page === 1,
                right: page === totalPages,
                active: page === currentPage,
              }"
              @click="currentPage = page"
            >
              {{ page }}
            </button>
            <span v-else>...</span>
          </template>
        </nav>
      </div>
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
import LoadingSpinner from "@/components/LoadingSpinner.vue";

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
    currentPage.value = 1;
  } catch (error) {
    console.error("Ошибка поиска:", error);
    results.value = [];
  } finally {
    loading.value = false;
  }
}

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

const pageEntries = computed(() => {
  const current = currentPage.value;
  const total = totalPages.value;

  if (current === undefined || total === undefined) {
    return [];
  }

  const pages = new Set(
    [1, 2, current - 1, current, current + 1, total - 1, total].filter((x) => x >= 1 && x <= total)
  );
  const result = [...pages];

  for (let i = 0; i < result.length - 1; i++) {
    if (result[i] + 1 !== result[i + 1]) {
      result.splice(i + 1, 0, -1);
      i += 1;
    }
  }

  return result;
});

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
</script>

<style scoped lang="scss">
@use "@/styles/breakpoints.scss" as *;
@use "@/styles/colors.scss" as *;

.filter-condition {
  padding-top: 1rem;

  display: flex;
  flex-direction: row;
  align-items: center;
  column-gap: 0.5rem;
}

.actions {
  padding-top: 2rem;
  display: flex;
  justify-content: space-between;
}

.remove-button {
  padding: 0.75rem;
}

.button-icon {
  width: 1.2em;
  height: 1.2em;
  &.offset {
    margin-left: 0.5em;
  }
}

.loading {
  margin-top: 1rem;
  display: flex;
  flex-direction: row;
  align-items: center;
  column-gap: 1rem;
}

.books-list {
  display: flex;
  flex-direction: column;
  row-gap: 0.5rem;
}

.not-found {
  background-color: var(--color-accent-200);
  padding: 1rem;
  border-radius: 1rem;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.pagination {
  align-self: end;
  margin-top: 1rem;

  display: flex;
  flex-direction: column;
  align-items: end;
  row-gap: 0.25rem;
}

.pagination-slider {
  width: fit-content;

  background-color: var(--color-background-50);
  color: var(--color-text-950);

  border-style: solid;
  border-radius: 2rem;
  border-width: 1px;
  border-color: var(--color-text-300);

  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);

  display: flex;
  flex-direction: row;
  align-items: center;

  button {
    border: 0;
    background-color: var(--color-background-50);
    color: var(--color-text-950);

    cursor: pointer;

    padding: 0.25rem 0.5rem;
    display: flex;
    flex-direction: row;
    align-items: center;

    &.left {
      border-top-left-radius: 2rem;
      border-bottom-left-radius: 2rem;
    }

    &.right {
      border-top-right-radius: 2rem;
      border-bottom-right-radius: 2rem;
    }

    transition: 0.05s;
    @include light-theme {
      &:hover,
      &.active {
        background-color: var(--color-background-100);
      }
    }
    @include dark-theme {
      &:hover,
      &.active {
        background-color: var(--color-background-200);
      }
    }
  }
}

@media (min-width: 768px) {
  .filter-parameter {
    display: flex;
    flex-direction: row;
    align-items: center;
    column-gap: 0.5rem;
  }
}

@media (max-width: 767px) {
  .filter-condition {
    padding-top: 1rem;

    display: flex;
    flex-direction: column;
    gap: 16px;
    align-items: center;
    column-gap: 0.5rem;

    .filter-parameter {
      display: flex;
      flex-direction: row;
      align-items: center;
      column-gap: 0.5rem;
    }

    .and-or {
      width: 30%;
    }

    .and-or:hover {
      width: 30%;
    }

    select {
      width: 100%;
    }

    select:focus {
      width: 100%;
    }

    input {
      width: 100%;
    }
  }
}
</style>
