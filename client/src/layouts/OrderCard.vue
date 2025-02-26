<template>
  <div class="card order-card">
    <div class="order-header">
      <span class="order-number">📦 Заказ #{{ num }}</span>
      <span class="order-status" :class="statusClass">● {{ orderStatuses[currentStatus] }}</span>
    </div>
    <div class="book-list">
      <div v-for="(orderBook, index) in order.books" :key="orderBook.book.id" class="book-item">
        <short-book :book="orderBook.book" :num="index" />
        <hr v-if="index < order.books.length - 1" class="divider" />
      </div>
    </div>
    <div class="order-actions-footer" v-if="showOrderActions">
      <button class="btn btn-cancel" @click="onCancelOrderClick" v-if="canCancelOrder">
        Отказаться
      </button>
      <button class="btn btn-edit" @click="onEditOrderClick" v-if="canEditOrder">
        Редактировать
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { type OrderStatusEnum, type Order, orderStatuses } from "@/api/types";
import ShortBook from "@/components/ShortBook.vue";
import { useOrderStore } from "@/stores/orderStore";
const allowedCancelStatuses: OrderStatusEnum[] = ["new", "processing", "ready"];
const allowedEditStatuses: OrderStatusEnum[] = ["new"];
const orderStore = useOrderStore();

const { order, num } = defineProps<{
  order: Order;
  num: number;
}>();

const emit = defineEmits(["delete"]);

const canCancelOrder = computed(() => allowedCancelStatuses.includes(currentStatus.value));

const canEditOrder = computed(() => allowedEditStatuses.includes(currentStatus.value));
const showOrderActions = computed(() => canCancelOrder.value || canEditOrder.value);

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
  emit("delete");
  await orderStore.handleDeleteOrder(order.id);
}

async function onEditOrderClick() {
  console.log("Edit order:", order.id);
}
</script>

<style scoped lang="scss">
.order-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition:
    transform 0.2s ease,
    box-shadow 0.3s ease;
  background: #ffffff;
  margin: 1rem 0;
  padding: 1.5rem;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f0f0f0;
}

.order-number {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
}

.order-cancel {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
}

.order-status {
  font-size: 0.9rem;
  padding: 4px 8px;
  border-radius: 16px;
  background: #f0f0f0;
}

.order-status.new {
  color: #42a7b9;
  background: #e8f5e9;
}

.order-status.processing {
  color: #2196f3;
  background: #e3f2fd;
}

.order-status.ready {
  color: #27b029;
  background: #f3e5f5;
}

.order-status.done {
  color: #9c27b0;
  background: #f3e5f5;
}

.order-status.cancelled {
  color: #601318;
  background: #f3e5f5;
}

.order-status.error {
  color: #b02735;
  background: #f3e5f5;
}

.order-status.archived {
  color: #5b585c;
  background: #f3e5f5;
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
  border-top: 1px solid #eee;
  margin: 1rem 0;
}

.order-actions-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}
</style>
