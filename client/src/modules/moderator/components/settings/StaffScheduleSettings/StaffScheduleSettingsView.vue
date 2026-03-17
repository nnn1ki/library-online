<script setup lang="ts">
import { computed } from "vue";

import type { LibrarySettings } from "@core/api/types";
import { staffScheduleDayLabels } from "@core/api/types";

const props = defineProps<{
  modelValue: Pick<
    LibrarySettings,
    "staff_digest_week_schedule" | "staff_digest_schedule_overrides"
  >;
}>();

const weekDays = Object.entries(staffScheduleDayLabels) as Array<
  [keyof typeof staffScheduleDayLabels, string]
>;

const overrides = computed(() =>
  Object.entries(props.modelValue.staff_digest_schedule_overrides).sort(([left], [right]) =>
    left.localeCompare(right)
  )
);

const visibleOverrides = computed(() => overrides.value.slice(0, 4));
const remainingOverrides = computed(() => Math.max(overrides.value.length - visibleOverrides.value.length, 0));

function formatWindow(
  window: { enabled: boolean; start?: string; end?: string } | undefined
) {
  if (!window?.enabled) return "Выходной";
  return `${window.start} - ${window.end}`;
}

function formatDate(dateValue: string) {
  return new Intl.DateTimeFormat("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  }).format(new Date(`${dateValue}T00:00:00`));
}
</script>

<template>
  <div class="view-stack">
    <div class="schedule-grid">
      <div v-for="[dayKey, dayLabel] in weekDays" :key="dayKey" class="schedule-row">
        <span class="row-label">{{ dayLabel }}</span>
        <strong>{{ formatWindow(modelValue.staff_digest_week_schedule[dayKey]) }}</strong>
      </div>
    </div>

    <div class="override-card">
      <div class="override-header">
        <span class="row-label">Исключения по датам</span>
        <strong>{{ overrides.length }}</strong>
      </div>

      <div v-if="visibleOverrides.length" class="override-list">
        <div v-for="[dateKey, window] in visibleOverrides" :key="dateKey" class="override-row">
          <span>{{ formatDate(dateKey) }}</span>
          <strong>{{ formatWindow(window) }}</strong>
        </div>

        <p v-if="remainingOverrides" class="hint-text">Еще {{ remainingOverrides }} дат в списке.</p>
      </div>

      <p v-else class="hint-text">Пока используются только стандартные часы недели.</p>
    </div>
  </div>
</template>

<style scoped lang="scss">
.view-stack {
  display: grid;
  gap: 1rem;
}

.schedule-grid,
.override-card {
  display: grid;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 1rem;
  background: linear-gradient(180deg, var(--color-background-50), var(--color-background-100));
  border: 1px solid var(--color-text-200);
}

.schedule-row,
.override-row,
.override-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.row-label,
.hint-text {
  color: var(--color-text-600);
  font-size: var(--text-xs);
}

.override-list {
  display: grid;
  gap: 0.6rem;
}

.hint-text {
  margin: 0;
}

@media (max-width: 640px) {
  .schedule-row,
  .override-row,
  .override-header {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
