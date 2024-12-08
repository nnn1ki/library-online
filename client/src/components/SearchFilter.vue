<template>
  <div class="search-filter p-3 border rounded bg-light">

    <!-- Фильтры -->
    <div v-for="(condition, index) in conditions" :key="index" class="filter-condition mb-3">
      <div class="d-flex align-items-center gap-2">
        
        <!-- Операторы AND/OR -->
        <select v-model="condition.andOrOperator" class="form-select form-select-sm" @change="updateSearchParams">
          <option v-for="andOr in andOrFilters" :key="andOr">{{ andOr }}</option>
        </select>

        <!-- Тип фильтра (Название, Автор, Количество) -->
        <select v-model="condition.filterType" class="form-select form-select-sm" @change="updateSearchParams">
          <option v-for="filter in filters" :key="filter">{{ filter }}</option>
        </select>

        <!-- Значение фильтра (ввод текста) -->
        <input
          v-model="condition.filterValue"
          type="text"
          class="form-control form-control-sm"
          placeholder="Введите значение"
          @input="updateSearchParams"
        />

        <!-- Удалить условие -->
        <button v-if="index > 0" class="btn btn-danger btn-sm" @click="removeCondition(index)">
          <i class="bi bi-x-square"></i>
        </button>
      </div>
    </div>

    <!-- Кнопки для добавления нового условия и запуска поиска -->
    <div class="actions d-flex justify-content-between">
      <button class="btn btn-outline-primary btn-sm" @click="addCondition">
        Добавить условие <i class="bi bi-plus-square"></i>
      </button>
      <button class="btn btn-success btn-sm" @click="search">
        Поиск <i class="bi bi-search"></i>
      </button>
    </div>
  </div>
</template>

<style scoped>
.search-filter {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.filter-condition {
  display: flex;
  align-items: center;
}

.actions button {
  min-width: 120px;
}
</style>

<script setup>
import { ref, defineEmits, watch } from "vue";
import { useRouter, useRoute } from "vue-router";

// События для передачи изменений в родительский компонент
const emit = defineEmits();

// Получаем данные маршрута (для работы с query параметрами)
const route = useRoute();
const router = useRouter();

// Начальные значения фильтров
const filters = ref(["Заглавие/Название", "Автор", "Ключевые слова"]);
const andOrFilters = ref(["И", "ИЛИ"]);

// Начальные условия
const conditions = ref([
  {
    filterType: "Заглавие/Название",
    filterValue: "",
    andOrOperator: null,
  },
]);

// Функция для добавления нового условия
function addCondition() {
  conditions.value.push({
    filterType: "Заглавие/Название",
    filterValue: "",
    andOrOperator: "И",
  });
}

// Функция для удаления условия
function removeCondition(index) {
  conditions.value.splice(index, 1);
}

// Обновление URL с новыми query параметрами
function updateSearchParams() {
  const searchParams = {};

  // Преобразуем данные фильтров в query параметры
  conditions.value.forEach((condition, index) => {
    if (condition.filterValue) {
      searchParams[`filter${index}Type`] = condition.filterType;
      searchParams[`filter${index}Value`] = condition.filterValue;
      if (condition.andOrOperator) {
        searchParams[`filter${index}Operator`] = condition.andOrOperator;
      }
    }
  });

  // Обновляем URL с новыми параметрами
  router.push({ path: '/', query: searchParams });
}

// Обработчик поиска
function search() {
  updateSearchParams();
}
</script>

<!-- <style scoped>
.search-filter {
  background: #f4f4ff;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filter-condition {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.filter-condition-row {
  display: flex;
  gap: 10px;
  align-items: center;
}

.form-select,
.form-control {
  min-width: 150px;
}

.actions {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  gap: 10px;
}
</style> -->
