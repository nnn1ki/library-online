<template>
  <div class="table-responsive">
    <table class="table table-light align-middle">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col" @click="sortOrders('user')">
            Клиент
            <span v-if="sortKey === 'user'">
              <i :class="sortOrder === 1 ? 'bi bi-arrow-up' : 'bi bi-arrow-down'"></i>
            </span>
          </th>
          <th scope="col" @click="sortOrders('date')">
            Дата и время
            <span v-if="sortKey === 'date'">
              <i :class="sortOrder === 1 ? 'bi bi-arrow-up' : 'bi bi-arrow-down'"></i>
            </span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in sortedOrders" :key="order.id">
          <th scope="row">{{ order.id }}</th>
          <td>{{ order.user.first_name }} {{ order.user.last_name }}</td>
          <td>{{ formatDate(order.statuses[0].date) }}</td>
          <td>
            <button
              class="btn btn-primary"
              data-bs-toggle="modal"
              data-bs-target="#orderDetailsModal"
              @click="handleOpenOrderDetails(order.id)"
            >
              <EllipsisHorizontalIcon />
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref, computed } from "vue";
import type { UserOrder, OrderStatusEnum } from "@/api/types";
import { updateOrderStatus } from "@/api/order";
import { EllipsisHorizontalIcon } from "@heroicons/vue/24/outline";

const props = defineProps<{
  orders: UserOrder[];
}>();

const emit = defineEmits<{
  (e: "getOrder", id: number): void;
}>();

const sortKey = ref<string>("id");
const sortOrder = ref<number>(1);

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  const year = date.getFullYear().toString().padStart(4, "0");
  const month = (date.getMonth() + 1).toString().padStart(2, "0");
  const day = date.getDate().toString().padStart(2, "0");
  const hours = date.getHours().toString().padStart(2, "0");
  const minutes = date.getMinutes().toString().padStart(2, "0");
  const seconds = date.getSeconds().toString().padStart(2, "0");

  // return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  return `${day}.${month}.${year} | ${hours}:${minutes}:${seconds}`;
}

// Функция для раскраски таблицы
function getRowClass(order: UserOrder) {
  const orderDate = new Date(order.statuses[0].date);
  const currentDate = new Date();
  const timeDifference = currentDate.getTime() - orderDate.getTime();
  const hoursDifference = timeDifference / (1000 * 3600);

  if (order.statuses[0].status === "new") {
    if (hoursDifference < 2) {
      return "table-success"; // Менее 2 часов - зеленый
    } else if (hoursDifference < 6) {
      return "table-warning"; // От 2 до 6 часов - желтый
    } else {
      return "table-danger"; // Более 6 часов - красный
    }
  }

  return "";
}

// Функция сортировки
function sortOrders(key: string) {
  if (sortKey.value === key) {
    sortOrder.value *= -1;
  } else {
    sortKey.value = key;
    sortOrder.value = 1;
  }
}

// Вычисляемый массив для отсортированных заказов
const sortedOrders = computed(() => {
  return [...props.orders].sort((a, b) => {
    let aValue: string | number;
    let bValue: string | number;

    switch (sortKey.value) {
      case "user":
        aValue = `${a.user.first_name} ${a.user.last_name}`;
        bValue = `${b.user.first_name} ${b.user.last_name}`;
        break;
      case "date":
        aValue = new Date(a.statuses[0].date).getTime();
        bValue = new Date(b.statuses[0].date).getTime();
        break;
      case "id":
        aValue = a.id;
        bValue = b.id;
        break;
      default:
        aValue = a.id;
        bValue = b.id;
    }

    if (aValue < bValue) return -1 * sortOrder.value;
    if (aValue > bValue) return 1 * sortOrder.value;
    return 0;
  });
});

const handleOpenOrderDetails = (orderId: number) => {
  emit("getOrder", orderId);
};
</script>

<style scoped>
tr {
  cursor: pointer;
}
</style>
