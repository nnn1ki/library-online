<template>
  <div class="search-filter p-3 border rounded bg-light">
    <!-- Фильтры -->
    <div
      v-for="(condition, index) in conditions"
      :key="index"
      class="filter-condition mb-3"
    >
      <div class="d-flex align-items-center gap-2">
        <!-- Операторы AND/OR -->
        <select
          v-model="condition.andOrOperator"
          class="form-select form-select-sm"
          @change="updateSearchParams"
        >
          <option v-for="andOr in andOrFilters" :key="andOr">{{ andOr }}</option>
        </select>

        <!-- Тип фильтра -->
        <select
          v-model="condition.filterType"
          class="form-select form-select-sm"
          @change="updateSearchParams"
        >
          <option v-for="filter in filters" :key="filter">{{ filter }}</option>
        </select>

        <!-- Значение фильтра -->
        <input
          v-model="condition.filterValue"
          type="text"
          class="form-control form-control-sm"
          placeholder="Введите значение"
          @input="updateSearchParams"
        />

        <!-- Удалить условие -->
        <button
          v-if="index > 0"
          class="btn btn-danger btn-sm"
          @click="removeCondition(index)"
        >
          <i class="bi bi-x-square"></i>
        </button>
      </div>
    </div>

    <!-- Кнопки -->
    <div class="actions d-flex justify-content-between">
      <button class="btn btn-outline-primary btn-sm" @click="addCondition">
        Добавить условие <i class="bi bi-plus-square"></i>
      </button>
      <button class="btn btn-success btn-sm" @click="search">
        Поиск <i class="bi bi-search"></i>
      </button>
    </div>

    <!-- Результаты поиска -->
    <div v-if="loading" class="mt-3">Загрузка...</div>
    <div v-else class="mt-3">
      <h3>Результаты поиска</h3>
      <ul v-if="results.length" class="list-group">
        <li v-for="book in results" :key="book.id" class="list-group-item">
          <strong>{{ book.title }}</strong> — {{ book.author }}
        </li>
      </ul>
      <div v-else class="alert alert-warning mt-2">Книги не найдены</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { searchBooks } from "@/api/search.js";

// Состояния
const router = useRouter();
const route = useRoute();

const filters = ["Заглавие/Название", "Автор", "Ключевые слова", "УДК", "ББК", 
    "Инв.N, Штрих-код", "Заглавие - журналы", "Вид/Тип документа", "Характер документа", 
    "Коллектив/Мероприятие", "Издающая организация", "Место издания", "Год издания", "Предметные рубрики", 
    "Географические рубрики", "Язык", "Персоналия", "Партия книг (N записи КСУ)", "Партия книг (N Акта ИУ)", 
    "Инв.N, утерянные", "Номер партии книг выбытия", "Списанные:Инв./ШКод/Шифр выпуска журнала", "ISBN/ISSN",
    "Шифр документа", "Заглавие - серии", "Целевое назначение", "Физический носитель информации", 
    "Индекс для СУ", "Диссертация - Код специальности", "Заглавие - Ист.статьи", "Страна издания", 
    "Журнал за ... (год)", "Другая классификация", "Раздел знаний", "Тематический рубрикатор", 
    "Автор-сотрудник", "Место работы автора/редактора", "Автограф", 
    "Наименование коллекции", "Держатель документа", "Редкие книги", "Музыкальные: жанры и средства", 
    "Нотный инципит", "Цитируемость", "Дата ввода", "Дата поступления экземпляра", "Место хранения экз-ра", 
    "Канал поступления экз-ра", "Инв.N,сортированные", "Инв.N списанные,сортированные", "Технология", "Периодика, подлежащая списанию",
    "Период подписки периодики", "Учебная дисциплина", "Электронный ресурс", "Гриф учебной литературы", "Номер карточки комплектования",
    "Учебный фонд", "Фонд редких книг", "Коллекция", "Библиографическая база", "Раздел указателя", "Статус экземпляра", "Выставка",
    "Штрих-код экземпляра", "RFID экземпляра", "Количество экземпляров", "Номер КСУ", "Номер акта", "Вид документа", "ПНР", 
    "ЭБС", "Подразделение/филиал", "Договор, ФИО", "Договор, доступ", "Договор, номер", "Проверка фонда", "Уровень записи", 
    "Подписка", "Все префиксы", 
];
const andOrFilters = ["И", "ИЛИ"];
const conditions = ref([
  {
    filterType: "Заглавие/Название",
    filterValue: "",
    andOrOperator: null,
  },
]);

const results = ref([]);
const loading = ref(false);

// Функции для управления фильтрами
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

function updateSearchParams() {
  const searchParams = {};
  conditions.value.forEach((condition, index) => {
    if (condition.filterValue) {
      searchParams[`filter${index}Type`] = condition.filterType;
      searchParams[`filter${index}Value`] = condition.filterValue;
      if (condition.andOrOperator) {
        searchParams[`filter${index}Operator`] = condition.andOrOperator;
      }
    }
  });
  router.push({ path: "/", query: searchParams });
}

// Поиск книг
async function search() {
  loading.value = true;
  try {
    const query = conditions.value
      .filter((condition) => condition.filterValue)
      .map((condition) => ({
        type: condition.filterType,
        value: condition.filterValue,
        operator: condition.andOrOperator,
      }));
    const response = await searchBooks(query);
    results.value = response.data;
  } catch (error) {
    console.error("Ошибка поиска:", error);
    results.value = [];
  } finally {
    loading.value = false;
  }
}
</script>