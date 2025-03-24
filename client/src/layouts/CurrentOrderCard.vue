<template>
  <div class="card order-card">
    <div class="order-header">
      <span class="order-status">● Еще не заказали </span>
    </div>
    <div class="book-list">
      <div v-for="(book, index) in order" :key="book.id" class="book-item">
        <ShortBookCard :book="book" :num="index" />
        <hr class="divider" />
      </div>
    </div>
    <div class="order-actions-footer">
      <RouterLink to="/order">
        <StyledButton theme="primary" >Продолжить оформление</StyledButton>
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Book } from "@/api/types";
import ShortBookCard from "@/components/ShortBookCard.vue";
import StyledButton from "@/components/StyledButton.vue";
const { order } = defineProps<{
  order: Book[];
}>();
</script>

<style scoped lang="scss">
.order-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px var(--color-primary-700);
  transition:
  transform 0.2s ease,
  box-shadow 0.3s ease;
  background-color: var(--color-background-200);
  color: var(--color-text-900);
  margin: 1rem 0;
  padding: 1.5rem;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 12px var(--color-primary-700);
}

.order-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--color-primary-700);
}

.order-number {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-text-900);
}

.order-cancel {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-text-900);
}

.order-status {
  font-size: 0.9rem;
  padding: 4px 8px;
  border-radius: 16px;
  background-color: var(--color-primary-500);
  color: #ffffff;
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
  margin: 1rem 0;
}

.order-actions-footer {
  margin-top: 0.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-primary-700);
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}
</style>
