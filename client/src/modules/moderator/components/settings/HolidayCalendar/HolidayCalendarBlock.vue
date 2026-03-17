<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useDebounceFn } from "@vueuse/core";
import { DatePicker } from "v-calendar";

type CalendarAttribute = {
  key: string;
  highlight: {
    color: string;
    fillMode: "solid";
  };
  dates: string[];
};

type DayClickEvent = {
  date: Date;
};

const props = defineProps<{
  holidays: string[];
}>();

const emit = defineEmits<{
  "update:holidays": [value: string[]];
}>();

const localHolidays = ref<string[]>([]);
const holidayPreviewLimit = 10;

const holidayAttributes = computed<CalendarAttribute[]>(() => [
  {
    key: "selected-holidays",
    highlight: {
      color: "purple",
      fillMode: "solid",
    },
    dates: localHolidays.value,
  },
]);

const holidayPreview = computed(() => localHolidays.value.slice(0, holidayPreviewLimit));
const remainingHolidayCount = computed(() =>
  Math.max(localHolidays.value.length - holidayPreviewLimit, 0)
);

watch(
  () => props.holidays,
  (holidays) => {
    localHolidays.value = [...holidays];
  },
  { immediate: true }
);

const emitDebouncedUpdate = useDebounceFn(() => {
  emit("update:holidays", [...localHolidays.value]);
}, 250);

function formatCalendarDate(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function toggleHoliday(day: DayClickEvent) {
  const clickedDay = formatCalendarDate(day.date);
  const holidays = new Set(localHolidays.value);

  if (holidays.has(clickedDay)) {
    holidays.delete(clickedDay);
  } else {
    holidays.add(clickedDay);
  }

  localHolidays.value = Array.from(holidays).sort();
  emitDebouncedUpdate();
}
</script>

<template>
  <section class="settings-card calendar-card">
    <header class="card-heading">
      <div>
        <p class="card-kicker">Календарь</p>
        <h2>Праздники и выходные</h2>
      </div>
      <span class="card-badge">Календарь</span>
    </header>

    <p class="section-note">Клик по дате добавляет или убирает её из списка праздничных дней.</p>

    <DatePicker :attributes="holidayAttributes" is-expanded locale="ru" @dayclick="toggleHoliday" />

    <div class="holiday-list">
      <div class="holiday-list-header">
        <span>Выбранные даты</span>
        <span>{{ localHolidays.length }}</span>
      </div>

      <div v-if="holidayPreview.length" class="holiday-chips">
        <span v-for="holiday in holidayPreview" :key="holiday" class="holiday-chip">
          {{ holiday }}
        </span>
        <span v-if="remainingHolidayCount" class="holiday-chip holiday-chip-muted">
          +{{ remainingHolidayCount }} еще
        </span>
      </div>

      <p v-else class="section-note">Праздничные даты пока не выбраны.</p>
    </div>
  </section>
</template>

<style scoped lang="scss">
.settings-card {
  display: grid;
  gap: 1rem;
  padding: 1.3rem;
  background: var(--color-background-50);
  border: 1px solid var(--color-text-200);
  border-radius: 1.2rem;
  box-shadow: 0 12px 30px rgba(17, 12, 29, 0.06);
}

.calendar-card {
  position: sticky;
  top: 1rem;
}

.card-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}

.card-kicker {
  margin: 0 0 0.35rem;
  color: var(--color-text-600);
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.card-heading h2 {
  margin: 0;
  font-size: var(--text-xl);
}

.card-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.45rem 0.7rem;
  border-radius: 999px;
  background: var(--color-primary-100);
  color: var(--color-primary-700);
  font-size: var(--text-xs);
  font-weight: 700;
}

.section-note {
  margin: 0;
  color: var(--color-text-600);
  font-size: var(--text-xs);
  line-height: 1.55;
}

.holiday-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 0.9rem 1rem;
  border-radius: 1rem;
  background: var(--color-background-100);
  border: 1px solid var(--color-text-200);
}

.holiday-list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: var(--text-sm);
  font-weight: 700;
  color: var(--color-text-800);
}

.holiday-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.holiday-chip {
  display: inline-flex;
  align-items: center;
  min-height: 2rem;
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  background: var(--color-primary-100);
  color: var(--color-primary-700);
  font-size: var(--text-xs);
  font-weight: 600;
}

.holiday-chip-muted {
  background: var(--color-background-200);
  color: var(--color-text-700);
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
  background: var(--color-primary-500);
  color: var(--color-text-50);
}

:deep(.vc-day.is-not-in-month .vc-day-content) {
  color: var(--color-text-400);
}

@media (max-width: 960px) {
  .calendar-card {
    position: static;
  }
}

@media (max-width: 640px) {
  .settings-card {
    padding: 1rem;
  }

  .card-heading {
    flex-direction: column;
  }
}
</style>
