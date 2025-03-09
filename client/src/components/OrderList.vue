<template>
  <div>
    <table class="table-primary">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">ФИО клиента</th>
          <th scope="col">Статус</th>
          <th scope="col">Дата</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in orders" :key="order.id">
          <th scope="row">{{ order.id }}</th>
          <td>{{ order.user.username }}</td>
          <td>{{ order.statuses[0].status }}</td>
          <td>{{ formatDate(order.statuses[0].date) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import type { UserOrder } from "@/api/types";

const props = defineProps<{
  orders: UserOrder[];
}>();

// Функция для форматирования даты в нужный формат
function formatDate(dateString: string): string {
  const date = new Date(dateString);

  const year = date.getFullYear().toString().padStart(4, "0");
  const month = (date.getMonth() + 1).toString().padStart(2, "0");
  const day = date.getDate().toString().padStart(2, "0");
  const hours = date.getHours().toString().padStart(2, "0");
  const minutes = date.getMinutes().toString().padStart(2, "0");
  const seconds = date.getSeconds().toString().padStart(2, "0");

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
</style>
