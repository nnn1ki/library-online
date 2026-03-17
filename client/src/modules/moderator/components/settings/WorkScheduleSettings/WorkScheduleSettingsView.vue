<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { Calendar } from "v-calendar";

import type { LibrarySettings } from "@core/api/types";
import { staffScheduleDayLabels } from "@core/api/types";

type WorkScheduleSettings = Pick<
  LibrarySettings,
  "holidays" | "staff_digest_week_schedule" | "staff_digest_schedule_overrides"
>;

type CalendarAttribute = {
  key: string;
  highlight: {
    color: string;
    fillMode: "solid" | "outline";
  };
  dates: string[];
};

type CalendarPage = {
  month: number;
  year: number;
};

const props = defineProps<{
  modelValue: WorkScheduleSettings;
}>();

const today = new Date();
const calendarRef = ref<any>(null);
const currentPage = ref<CalendarPage>({
  month: today.getMonth() + 1,
  year: today.getFullYear(),
});

const weekDays = Object.entries(staffScheduleDayLabels) as Array<
  [keyof typeof staffScheduleDayLabels, string]
>;

const overrides = computed(() => {
  const monthPrefix = `${currentPage.value.year}-${String(currentPage.value.month).padStart(2, "0")}-`;
  return Object.entries(props.modelValue.staff_digest_schedule_overrides)
    .filter(([dateKey]) => dateKey.startsWith(monthPrefix))
    .sort(([left], [right]) => left.localeCompare(right));
});

const visibleOverrides = computed(() => overrides.value.slice(0, 4));
const remainingOverrides = computed(() => Math.max(overrides.value.length - visibleOverrides.value.length, 0));

const calendarAttributes = computed<CalendarAttribute[]>(() => [
  {
    key: "holidays",
    highlight: {
      color: "red",
      fillMode: "solid",
    },
    dates: props.modelValue.holidays,
  },
  {
    key: "overrides",
    highlight: {
      color: "blue",
      fillMode: "outline",
    },
    dates: Object.keys(props.modelValue.staff_digest_schedule_overrides),
  },
]);

function formatWindow(window: { enabled: boolean; start?: string; end?: string } | undefined) {
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

function updateCurrentPage(page: CalendarPage) {
  currentPage.value = {
    month: page.month,
    year: page.year,
  };
}

watch(
  () => [calendarRef.value?.firstPage?.year, calendarRef.value?.firstPage?.month],
  ([year, month]) => {
    if (!year || !month) return;
    updateCurrentPage({ year, month });
  },
  { immediate: true }
);
</script>

<template>
  <div class="view-layout">
    <div class="calendar-card">
      <p class="section-note">Красным отмечены нерабочие праздничные даты, синей рамкой выделены дни с ручными исключениями.</p>
      <Calendar
        ref="calendarRef"
        :from-page="currentPage"
        :attributes="calendarAttributes"
        is-expanded
        locale="ru"
        @update:from-page="updateCurrentPage"
      />
    </div>

    <div class="summary-stack">
      <div class="summary-card">
        <div class="summary-header">
          <span class="summary-title">Шаблон недели</span>
        </div>

        <div class="schedule-grid">
          <div v-for="[dayKey, dayLabel] in weekDays" :key="dayKey" class="schedule-row">
            <span class="row-label">{{ dayLabel }}</span>
            <strong>{{ formatWindow(modelValue.staff_digest_week_schedule[dayKey]) }}</strong>
          </div>
        </div>
      </div>

      <div class="summary-card">
        <div class="summary-header">
          <span class="summary-title">Исключения по датам</span>
          <strong>{{ overrides.length }}</strong>
        </div>

        <div v-if="visibleOverrides.length" class="override-list">
          <div v-for="[dateKey, window] in visibleOverrides" :key="dateKey" class="override-row">
            <span>{{ formatDate(dateKey) }}</span>
            <strong>{{ formatWindow(window) }}</strong>
          </div>

          <p v-if="remainingOverrides" class="section-note">Еще {{ remainingOverrides }} дат в списке.</p>
        </div>

        <p v-else class="section-note">Для открытого месяца исключений пока нет.</p>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.view-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(18rem, 0.95fr);
  gap: 1rem;
}

.calendar-card,
.summary-card {
  display: grid;
  gap: 0.85rem;
  padding: 1rem;
  border-radius: 1rem;
  background: linear-gradient(180deg, var(--color-background-50), var(--color-background-100));
  border: 1px solid var(--color-text-200);
}

.summary-stack {
  display: grid;
  gap: 1rem;
}

.summary-header,
.schedule-row,
.override-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.summary-title,
.row-label,
.section-note {
  color: var(--color-text-600);
  font-size: var(--text-xs);
}

.section-note {
  margin: 0;
  line-height: 1.55;
}

.schedule-grid,
.override-list {
  display: grid;
  gap: 0.75rem;
}

:deep(.vc-container) {
  width: 100%;
  border: none;
  border-radius: 1rem;
  background: transparent;
  color: var(--color-text-900);
  font-family: inherit;
}

:deep(.vc-header) {
  margin-bottom: 0.75rem;
}

:deep(.vc-title) {
  color: var(--color-text-900);
  font-size: var(--text-lg);
  font-weight: 700;
}

:deep(.vc-weekday) {
  color: var(--color-text-600);
  font-size: var(--text-xs);
  font-weight: 700;
  text-transform: uppercase;
}

:deep(.vc-arrow) {
  color: var(--color-primary-600);
  border-radius: 999px;
}

:deep(.vc-arrow:hover),
:deep(.vc-nav-item:hover),
:deep(.vc-day-content:hover) {
  background: var(--color-primary-100);
}

:deep(.vc-day-content) {
  color: var(--color-text-800);
  font-size: var(--text-sm);
  font-weight: 600;
  border-radius: 0.75rem;
}

:deep(.vc-highlight-content-solid) {
  color: var(--color-text-50);
}

:deep(.vc-highlight-content-outline) {
  border-width: 2px;
}

:deep(.vc-day.is-not-in-month .vc-day-content) {
  color: var(--color-text-400);
}

@media (max-width: 960px) {
  .view-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .summary-header,
  .schedule-row,
  .override-row {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
