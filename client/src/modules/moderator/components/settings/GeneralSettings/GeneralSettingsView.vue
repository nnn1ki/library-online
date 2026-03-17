<script setup lang="ts">
import type { LibrarySettings } from "@core/api/types";

defineProps<{
  modelValue: Pick<
    LibrarySettings,
    | "max_books_per_order"
    | "max_books_per_reader"
    | "max_borrow_days"
    | "new_order_wait"
    | "processing_order_wait"
  >;
}>();
</script>

<template>
  <div class="stats-grid">
    <div class="stat-box">
      <span class="stat-name">В заказе</span>
      <strong>{{ modelValue.max_books_per_order }}</strong>
    </div>
    <div class="stat-box">
      <span class="stat-name">На руках</span>
      <strong>{{ modelValue.max_books_per_reader }}</strong>
    </div>
    <div class="stat-box">
      <span class="stat-name">Срок выдачи</span>
      <strong>{{ modelValue.max_borrow_days }} дн.</strong>
    </div>
    <div class="stat-box">
      <span class="stat-name">Новый заказ</span>
      <strong>{{ modelValue.new_order_wait }} ч.</strong>
    </div>
    <div class="stat-box stat-box-wide">
      <span class="stat-name">Порог в работе</span>
      <strong>{{ modelValue.processing_order_wait }} ч.</strong>
    </div>
  </div>
</template>

<style scoped lang="scss">
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.9rem;
}

.stat-box {
  display: grid;
  gap: 0.3rem;
  padding: 1rem;
  border-radius: 1rem;
  background: linear-gradient(180deg, var(--color-background-50), var(--color-background-100));
  border: 1px solid var(--color-text-200);
}

.stat-box strong {
  font-size: var(--text-lg);
}

.stat-name {
  color: var(--color-text-600);
  font-size: var(--text-xs);
}

.stat-box-wide {
  grid-column: 1 / -1;
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
