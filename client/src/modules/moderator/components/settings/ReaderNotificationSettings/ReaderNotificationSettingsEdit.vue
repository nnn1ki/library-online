<script setup lang="ts">
import type { LibrarySettings } from "@core/api/types";

type ReaderNotificationSettings = Pick<
  LibrarySettings,
  "reader_status_notifications_enabled" | "reader_notification_statuses"
>;

const readerStatusOptions = [
  { label: "В работе", value: "processing" },
  { label: "Готов", value: "ready" },
  { label: "Отменен", value: "cancelled" },
] as const;

const props = defineProps<{
  modelValue: ReaderNotificationSettings;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: ReaderNotificationSettings];
}>();

function updateEnabled(enabled: boolean) {
  emit("update:modelValue", {
    ...props.modelValue,
    reader_status_notifications_enabled: enabled,
  });
}

function toggleStatus(status: string) {
  const statuses = new Set(props.modelValue.reader_notification_statuses);

  if (statuses.has(status)) {
    statuses.delete(status);
  } else {
    statuses.add(status);
  }

  emit("update:modelValue", {
    ...props.modelValue,
    reader_notification_statuses: Array.from(statuses),
  });
}
</script>

<template>
  <div class="edit-stack">
    <label class="toggle-card">
      <div>
        <span class="field-title">Включить reader-уведомления</span>
        <p class="field-note">Глобальный переключатель отправки писем читателю.</p>
      </div>
      <input
        :checked="modelValue.reader_status_notifications_enabled"
        type="checkbox"
        @change="updateEnabled(($event.target as HTMLInputElement).checked)"
      />
    </label>

    <div class="status-list">
      <label
        v-for="statusOption in readerStatusOptions"
        :key="statusOption.value"
        class="status-option"
      >
        <input
          :checked="modelValue.reader_notification_statuses.includes(statusOption.value)"
          type="checkbox"
          @change="toggleStatus(statusOption.value)"
        />
        <span>{{ statusOption.label }}</span>
      </label>
    </div>
  </div>
</template>

<style scoped lang="scss">
.edit-stack {
  display: grid;
  gap: 1rem;
}

.toggle-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 0.65rem;
  padding: 1rem;
  border: 1px solid var(--color-text-200);
  border-radius: 1rem;
  background: linear-gradient(180deg, var(--color-background-50), var(--color-background-100));
}

.field-title {
  color: var(--color-text-900);
  font-size: var(--text-sm);
  font-weight: 700;
}

.field-note {
  margin: 0.3rem 0 0;
  color: var(--color-text-600);
  font-size: var(--text-xs);
  line-height: 1.55;
}

.status-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.status-option {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.7rem 0.9rem;
  border-radius: 999px;
  background: var(--color-background-100);
  border: 1px solid var(--color-text-200);
  color: var(--color-text-800);
  font-size: var(--text-sm);
}

input[type="checkbox"] {
  width: 1.1rem;
  height: 1.1rem;
  accent-color: var(--color-primary-500);
}

@media (max-width: 640px) {
  .toggle-card {
    grid-template-columns: 1fr;
  }
}
</style>
