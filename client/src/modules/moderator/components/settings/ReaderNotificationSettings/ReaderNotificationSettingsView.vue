<script setup lang="ts">
import type { LibrarySettings } from "@core/api/types";

const labels: Record<string, string> = {
  new: "Новый",
  processing: "В работе",
  ready: "Готов",
  done: "Выдан",
  cancelled: "Отменен",
  error: "Ошибка",
  archived: "Архив",
};

defineProps<{
  modelValue: Pick<
    LibrarySettings,
    "reader_status_notifications_enabled" | "reader_notification_statuses"
  >;
}>();
</script>

<template>
  <div class="view-stack">
    <div class="state-row">
      <span class="state-label">Статус</span>
      <strong>{{
        modelValue.reader_status_notifications_enabled ? "Включены" : "Выключены"
      }}</strong>
    </div>

    <div class="status-list">
      <span
        v-for="status in modelValue.reader_notification_statuses"
        :key="status"
        class="status-chip"
      >
        {{ labels[status] ?? status }}
      </span>
      <span
        v-if="!modelValue.reader_notification_statuses.length"
        class="status-chip status-chip-muted"
      >
        Статусы не выбраны
      </span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.view-stack {
  display: grid;
  gap: 1rem;
}

.state-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-radius: 1rem;
  background: linear-gradient(180deg, var(--color-background-50), var(--color-background-100));
  border: 1px solid var(--color-text-200);
}

.state-label {
  color: var(--color-text-600);
  font-size: var(--text-sm);
}

.status-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.status-chip {
  display: inline-flex;
  align-items: center;
  min-height: 2rem;
  padding: 0.4rem 0.8rem;
  border-radius: 999px;
  background: var(--color-background-100);
  border: 1px solid var(--color-text-200);
  color: var(--color-text-800);
  font-size: var(--text-xs);
  font-weight: 600;
}

.status-chip-muted {
  color: var(--color-text-600);
}
</style>
