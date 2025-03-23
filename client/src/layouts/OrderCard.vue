<template>
  <div class="card order-card">
    <div class="order-header">
      <span class="order-number">📦 Заказ #{{ num }} oт {{ orderedDate }}</span>
      <span class="order-status" :class="statusClass"
        >● {{ orderStatuses[currentStatus] }} {{ lastStatusDate }}</span
      >
    </div>
    <div class="book-list">
      <div
        v-for="(orderBook, index) in order.books"
        :key="orderBook.book.id"
        class="book-item"
      >
        <div class="book-info">
          <ShortBookCard :book="orderBook.book" :num="index" />
          <button
            class="btn btn-add-book"
            @click="onAddToOrderClick(orderBook.book)"
            v-if="canReorder"
          >
            Заказать
          </button>
        </div>

      </div>
    </div>
    <div class="order-actions-footer" v-if="showOrderActions">
      <button class="btn btn-cancel" @click="onCancelOrderClick" v-if="canCancelOrder">
        Отказаться
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { type OrderStatusEnum, type Order, orderStatuses } from "@/api/types";
import ShortBookCard from "@/components/ShortBookCard.vue";
import { useOrderStore } from "@/stores/orderStore";
import type { Book } from "@/api/types";
const allowedCancelStatuses: OrderStatusEnum[] = ["new", "processing", "ready"];
const notAllowedToReOrderBoookStatuses: OrderStatusEnum[] = ["new"];
const orderStore = useOrderStore();

const { order, num } = defineProps<{
  order: Order;
  num: number;
}>();

const emit = defineEmits<{
  (e: "cancel", orderId: number): number;
}>();

const canCancelOrder = computed(() => allowedCancelStatuses.includes(currentStatus.value));

const canReorder = computed(() => !notAllowedToReOrderBoookStatuses.includes(currentStatus.value));
const showOrderActions = computed(() => canCancelOrder.value);

const orderedDate = order.statuses.at(0)?.date.slice(0, 10);
const lastStatusDate = order.statuses.at(-1)?.date.slice(0, 10);

const currentStatus = computed(() => {
  const lastStatus = order.statuses[order.statuses.length - 1]?.status;
  return lastStatus;
});

const statusClass = computed(() => {
  const status = currentStatus.value as OrderStatusEnum;
  return {
    [status]: true,
  };
});

async function onCancelOrderClick() {
  emit("cancel", order.id);
}

const onAddToOrderClick = (bookToOrder: Book) => {
  const isInCurrentOrder = orderStore.selectedBooks.some((book) => {
    return book.id === bookToOrder.id;
  });
  if (isInCurrentOrder) {
    return;
  } else {
    orderStore.addBook(bookToOrder);
  }
};
</script>

<style scoped lang="scss">
$color-white: #ffffff;
$color-black-5: rgba(0, 0, 0, 0.05);
$color-black-10: rgba(0, 0, 0, 0.1);
$color-gray-light: #f0f0f0;
$color-gray-divider: #eee;
$color-primary: #2c3e50;
$color-status-new: #42a7b9;
$color-status-processing: #2196f3;
$color-status-ready: #27b029;
$color-status-done: #9c27b0;
$color-status-cancelled: #601318;
$color-status-error: #b02735;
$color-status-archived: #5b585c;
$background-status-new: #e8f5e9;
$background-status-processing: #e3f2fd;
$background-status-ready: #f3e5f5;
$background-status-done: #f3e5f5;
$background-status-cancelled: #f3e5f5;
$background-status-error: #f3e5f5;
$background-status-archived: #f3e5f5;

.book-info {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.order-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px $color-black-5;
  transition:
    transform 0.2s ease,
    box-shadow 0.3s ease;
  background: $color-white;
  margin: 1rem 0;
  padding: 1.5rem;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 12px $color-black-10;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid $color-gray-light;
}

.order-number,
.order-cancel {
  font-size: 1.2rem;
  font-weight: 600;
  color: $color-primary;
}

.order-status {
  font-size: 0.9rem;
  padding: 4px 8px;
  border-radius: 16px;
  background: $color-gray-light;
}

.order-status.new {
  color: $color-status-new;
  background: $background-status-new;
}

.order-status.processing {
  color: $color-status-processing;
  background: $background-status-processing;
}

.order-status.ready {
  color: $color-status-ready;
  background: $background-status-ready;
}

.order-status.done {
  color: $color-status-done;
  background: $background-status-done;
}

.order-status.cancelled {
  color: $color-status-cancelled;
  background: $background-status-cancelled;
}

.order-status.error {
  color: $color-status-error;
  background: $background-status-error;
}

.order-status.archived {
  color: $color-status-archived;
  background: $background-status-archived;
}

.book-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.book-item {
  position: relative;
}

.divider {
  border: none;
  border-top: 1px solid $color-gray-divider;
  margin: 1rem 0;
}

.order-actions-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid $color-gray-divider;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-add-book {
  border-radius: 16px;
  font-size: 0.95rem;
  color: $color-status-archived;
  transition:
    color 0.3s ease,
    background 0.3s ease;
}

.btn-add-book:hover {
  color: $color-status-new;
  background: $background-status-new;
}
</style>
