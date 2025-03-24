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
          <StyledButton
            @click="onAddToOrderClick(orderBook.book)"
            theme="secondary"
            v-if="canReorder"
          >
            Заказать
          </StyledButton>
        </div>

      </div>
    </div>
    <div class="order-actions-footer" v-if="showOrderActions">
      <StyledButton @click="onCancelOrderClick" v-if="canCancelOrder">
        Отказаться
      </StyledButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { type OrderStatusEnum, type Order, orderStatuses } from "@/api/types";
import type { Book } from "@/api/types";
import { useOrderStore } from "@/stores/orderStore";
import ShortBookCard from "@/components/ShortBookCard.vue";``
import StyledButton from "@/components/StyledButton.vue";
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

.book-info {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.order-card {
  border-radius: 12px;
  box-shadow: 0 2px 4px var(--color-primary-600);
  transition:
  transform 0.2s ease,
  box-shadow 0.3s ease;
  background-color: var(--color-background-100);
  color: var(--color-text-900);
  margin: 1rem 0;
  padding: 1.5rem;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 12px var(--color-background-500);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--color-primary-800);
}

.order-number {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-primary-800);
}

.order-status {
  font-size: 0.9rem;
  padding: 4px 8px;
  border-radius: 16px;
  background: var(--color-primary-800);
}

.order-status.new {
  color: var(--color-status-new);
  background: var(--background-status-new);
}

.order-status.processing {
  color: var(--color-status-processing);
  background: var(--background-status-processing);
}

.order-status.ready {
  color: var(--color-status-ready);
  background: var(--background-status-ready);
}

.order-status.done {
  color: var(--color-status-done);
  background: var(--background-status-done);
}

.order-status.cancelled {
  color: var(--color-status-cancelled);
  background: var(--background-status-cancelled);
}

.order-status.error {
  color: var(--color-status-error);
  background: var(--background-status-error);
}

.order-status.archived {
  color: var(--color-status-archived);
  background: var(--background-status-archived);
}
.book-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.book-item {
  position: relative;
}

.order-actions-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 2px solid var(--color-primary-800);
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

</style>
