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
            Дата
            <span v-if="sortKey === 'date'">
              <i :class="sortOrder === 1 ? 'bi bi-arrow-up' : 'bi bi-arrow-down'"></i>
            </span>
          </th>
          <th scope="col">Информация</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="order in sortedOrders"
          :key="order.id"
          :class="[selectedOrderId === order.id ? 'table-primary' : getRowClass(order)]"
          @click="selectOrder(order.id)"
          @dblclick="handleUpdateOrderStatus(order.id, 'processing')"
        >
          <th scope="row">{{ order.id }}</th>
          <td>{{ order.user.first_name }} {{ order.user.last_name }}</td>
          <td>{{ formatDate(order.statuses[0].date) }}</td>
          <td>{{ order }}</td>
        </tr>
      </tbody>
    </table>
    <div>
      <button
        class="btn btn-primary"
        :disabled="selectedOrderId === null"
        data-bs-toggle="modal"
        data-bs-target="#orderDetailsModal"
        @click="showOrderDetails(selectedOrderId)"
      >
        Подробнее
      </button>
    </div>
    <div
      class="modal fade"
      id="orderDetailsModal"
      tabindex="-1"
      aria-labelledby="orderDetailsModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="orderDetailsModalLabel">Детали заказа</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
          </div>
          <div class="modal-body">
            <h6>Книги в заказе:</h6>
            <ul>
              <li v-for="book in selectedOrderBooks" :key="book.id">
                {{ book.title }} ({{ book.year }}) - {{ book.author.join(", ") }}
              </li>
            </ul>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref, computed } from "vue";
import type { UserOrder, OrderStatusEnum, Order } from "@/api/types";
import { updateOrderStatus } from "@/api/order";

const props = defineProps<{
  orders: UserOrder[];
}>();

const selectedOrderId = ref<number | null>(null);
const selectedOrderBooks = ref<any[]>([]);
const sortKey = ref<string>("id");
const sortOrder = ref<number>(1);

function selectOrder(orderId: number) {
  selectedOrderId.value = selectedOrderId.value === orderId ? null : orderId;
}

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
    let aValue: any;
    let bValue: any;

    if (sortKey.value === "user") {
      aValue = `${a.user.first_name} ${a.user.last_name}`;
      bValue = `${b.user.first_name} ${b.user.last_name}`;
    } else if (sortKey.value === "date") {
      aValue = new Date(a.statuses[0].date).getTime();
      bValue = new Date(b.statuses[0].date).getTime();
    } else {
      aValue = a[sortKey.value];
      bValue = b[sortKey.value];
    }

    if (aValue < bValue) return -1 * sortOrder.value;
    if (aValue > bValue) return 1 * sortOrder.value;
    return 0;
  });
});

// Функция для обновления статуса заказа
async function handleUpdateOrderStatus(orderId: number, newStatus: OrderStatusEnum) {
  const description = "Статус заказа обновлен";
  try {
    await updateOrderStatus(orderId, newStatus, description); // Или передайте описание, если нужно
  } catch (error) {
    console.error("Ошибка при обновлении статуса заказа", error);
  }
}

// Функция для отображения деталей заказа
function showOrderDetails(orderId: number | null) {
  if (orderId !== null) {
    const order = props.orders.find(o => o.id === orderId);
    selectedOrderBooks.value = order ? order.books : [];
  }
}
</script>

<style scoped>
tr {
  cursor: pointer;
}
</style>
