<template>
    <div class="search-filter">
      <!-- Фильтры -->
      <div v-for="(condition, index) in conditions" :key="index" class="filter-condition">
        <div class="filter-condition-row">
          <select v-model="condition.andOrOperator" class="form-select">
            <option v-for="andOr in andOrFilters" :key="andOr">{{ andOr }}</option>
          </select>
  
          <select v-model="condition.filterType" class="form-select">
            <option v-for="filter in filters" :key="filter">{{ filter }}</option>
          </select>
  
          <input v-model="condition.filterValue" type="text" class="form-control" placeholder="Введите значение" />
  
          <button v-if="index > 0" class="btn btn-danger" @click="removeCondition(index)">
            <i class="bi bi-x-square"></i>
          </button>
        </div>
      </div>
  
      <!-- Кнопки для добавления условия и запуска поиска -->
      <div class="actions">
        <button class="btn btn-primary" @click="addCondition">
          Добавить условие <i class="bi bi-plus-square"></i>
        </button>
        <button class="btn btn-success" @click="search">
          Поиск <i class="bi bi-search"></i>
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, defineEmits } from "vue";
  
  // События для передачи изменений в родительский компонент
  const emit = defineEmits();
  
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
  
  // Функция для запуска поиска и отправки данных в родительский компонент
  function search() {
    emit("search", conditions.value);
  }
  </script>
  
  <style scoped>
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
  </style>
  