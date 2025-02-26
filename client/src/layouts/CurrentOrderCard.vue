<template>
  <div class="card order-card">
    <div class="order-header">
      <span class="order-status">● Еще не заказали </span>
    </div>
    <div class="book-list">
      <div v-for="(book, index) in order" :key="book.id" class="book-item">
        <short-book :book="book" :num="index" />
        <hr class="divider" />
      </div>
    </div>
    <div class="order-actions-footer">
      <router-link to="/order">
        <button class="btn btn-cancel">Продолжить оформление</button>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Book } from "@/api/types";
import ShortBook from "@/components/ShortBook.vue";

const { order } = defineProps<{
  order: Book[];
}>();
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
  justify-content: flex-end;
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
  color: #212bc3;
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
