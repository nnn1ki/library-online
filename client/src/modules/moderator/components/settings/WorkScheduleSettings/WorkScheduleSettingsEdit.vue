<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { Calendar } from "v-calendar";

import type {
  LibrarySettings,
  StaffDigestWeekSchedule,
  StaffScheduleDayKey,
  StaffScheduleWindow,
} from "@core/api/types";
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

type DayClickEvent = {
  date: Date;
};

type CalendarPage = {
  month: number;
  year: number;
};

const props = defineProps<{
  modelValue: WorkScheduleSettings;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: WorkScheduleSettings];
}>();

const weekDays = Object.entries(staffScheduleDayLabels) as Array<[StaffScheduleDayKey, string]>;
const today = new Date();
const calendarRef = ref<any>(null);
const currentPage = ref<CalendarPage>({
  month: today.getMonth() + 1,
  year: today.getFullYear(),
});

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

const sortedOverrides = computed(() => {
  const monthPrefix = `${currentPage.value.year}-${String(currentPage.value.month).padStart(2, "0")}-`;
  return Object.keys(props.modelValue.staff_digest_schedule_overrides)
    .filter(dateKey => dateKey.startsWith(monthPrefix))
    .sort((left, right) => left.localeCompare(right));
});

function formatCalendarDate(date: Date): string {
  return [
    date.getFullYear(),
    String(date.getMonth() + 1).padStart(2, "0"),
    String(date.getDate()).padStart(2, "0"),
  ].join("-");
}

function normalizeWindow(window: StaffScheduleWindow, fallback: StaffScheduleWindow): StaffScheduleWindow {
  if (!window.enabled) return { enabled: false };
  return {
    enabled: true,
    start: window.start ?? fallback.start ?? "10:00",
    end: window.end ?? fallback.end ?? "17:00",
  };
}

function emitValue(value: WorkScheduleSettings) {
  emit("update:modelValue", value);
}

function toggleHoliday(day: DayClickEvent) {
  const dateKey = formatCalendarDate(day.date);
  const holidays = new Set(props.modelValue.holidays);

  if (holidays.has(dateKey)) {
    holidays.delete(dateKey);
  } else {
    holidays.add(dateKey);
  }

  emitValue({
    ...props.modelValue,
    holidays: Array.from(holidays).sort(),
  });
}

function updateWeekSchedule(dayKey: StaffScheduleDayKey, patch: Partial<StaffScheduleWindow>) {
  const currentWindow = props.modelValue.staff_digest_week_schedule[dayKey];
  const nextWindow = normalizeWindow({ ...currentWindow, ...patch }, currentWindow);

  emitValue({
    ...props.modelValue,
    staff_digest_week_schedule: {
      ...props.modelValue.staff_digest_week_schedule,
      [dayKey]: nextWindow,
    } as StaffDigestWeekSchedule,
  });
}

function getDayKeyForDate(dateValue: string): StaffScheduleDayKey {
  const dayIndex = new Date(`${dateValue}T00:00:00`).getDay();
  const weekDayMap: StaffScheduleDayKey[] = [
    "sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
  ];
  return weekDayMap[dayIndex];
}

function getDefaultOverrideWindow(dateValue: string): StaffScheduleWindow {
  const scheduleWindow = props.modelValue.staff_digest_week_schedule[getDayKeyForDate(dateValue)];
  return normalizeWindow(scheduleWindow, { enabled: true, start: "10:00", end: "17:00" });
}

function getNextAvailableDate() {
  const existingKeys = new Set(Object.keys(props.modelValue.staff_digest_schedule_overrides));
  const candidate = new Date(currentPage.value.year, currentPage.value.month - 1, 1);
  const targetMonth = candidate.getMonth();

  while (candidate.getMonth() === targetMonth) {
    const dateKey = formatCalendarDate(candidate);
    if (!existingKeys.has(dateKey)) return dateKey;
    candidate.setDate(candidate.getDate() + 1);
  }

  while (true) {
    const dateKey = formatCalendarDate(candidate);
    if (!existingKeys.has(dateKey)) return dateKey;
    candidate.setDate(candidate.getDate() + 1);
  }
}

function addOverride() {
  const dateKey = getNextAvailableDate();
  emitValue({
    ...props.modelValue,
    staff_digest_schedule_overrides: {
      ...props.modelValue.staff_digest_schedule_overrides,
      [dateKey]: getDefaultOverrideWindow(dateKey),
    },
  });
}

function removeOverride(dateKey: string) {
  const nextOverrides = { ...props.modelValue.staff_digest_schedule_overrides };
  delete nextOverrides[dateKey];

  emitValue({
    ...props.modelValue,
    staff_digest_schedule_overrides: nextOverrides,
  });
}

function renameOverrideDate(oldDateKey: string, newDateKey: string) {
  if (!newDateKey || newDateKey === oldDateKey) return;
  if (props.modelValue.staff_digest_schedule_overrides[newDateKey]) return;

  const nextOverrides: Record<string, StaffScheduleWindow> = {};
  for (const [dateKey, value] of Object.entries(props.modelValue.staff_digest_schedule_overrides)) {
    nextOverrides[dateKey === oldDateKey ? newDateKey : dateKey] =
      dateKey === oldDateKey ? normalizeWindow(value, getDefaultOverrideWindow(newDateKey)) : { ...value };
  }

  emitValue({
    ...props.modelValue,
    staff_digest_schedule_overrides: nextOverrides,
  });
}

function updateOverride(dateKey: string, patch: Partial<StaffScheduleWindow>) {
  const currentWindow = props.modelValue.staff_digest_schedule_overrides[dateKey];
  const nextWindow = normalizeWindow({ ...currentWindow, ...patch }, getDefaultOverrideWindow(dateKey));

  emitValue({
    ...props.modelValue,
    staff_digest_schedule_overrides: {
      ...props.modelValue.staff_digest_schedule_overrides,
      [dateKey]: nextWindow,
    },
  });
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
  <div class="edit-layout">
    <div class="calendar-panel">
      <p class="section-note">Клик по дате в календаре переключает праздничный выходной. Праздник всегда делает день нерабочим.</p>
      <Calendar
        ref="calendarRef"
        :from-page="currentPage"
        :attributes="calendarAttributes"
        is-expanded
        locale="ru"
        @dayclick="toggleHoliday"
        @update:from-page="updateCurrentPage"
      />
    </div>

    <div class="editor-stack">
      <div class="section-card">
        <div class="section-heading">
          <div>
            <h3>Базовый шаблон недели</h3>
            <p>Используется по умолчанию, если дата не помечена как праздник и для нее нет отдельного исключения.</p>
          </div>
        </div>

        <div class="day-list">
          <div v-for="[dayKey, dayLabel] in weekDays" :key="dayKey" class="day-row">
            <div class="day-main">
              <strong>{{ dayLabel }}</strong>
              <label class="toggle-label">
                <input
                  :checked="modelValue.staff_digest_week_schedule[dayKey].enabled"
                  type="checkbox"
                  @change="
                    updateWeekSchedule(dayKey, {
                      enabled: ($event.target as HTMLInputElement).checked,
                    })
                  "
                />
                <span>Рабочий день</span>
              </label>
            </div>

            <div v-if="modelValue.staff_digest_week_schedule[dayKey].enabled" class="time-grid">
              <label class="time-field">
                <span>С</span>
                <input
                  :value="modelValue.staff_digest_week_schedule[dayKey].start"
                  type="time"
                  @input="
                    updateWeekSchedule(dayKey, {
                      start: ($event.target as HTMLInputElement).value,
                    })
                  "
                />
              </label>
              <label class="time-field">
                <span>До</span>
                <input
                  :value="modelValue.staff_digest_week_schedule[dayKey].end"
                  type="time"
                  @input="
                    updateWeekSchedule(dayKey, {
                      end: ($event.target as HTMLInputElement).value,
                    })
                  "
                />
              </label>
            </div>

            <span v-else class="day-off">Выходной</span>
          </div>
        </div>
      </div>

      <div class="section-card">
        <div class="section-heading section-heading-compact">
          <div>
            <h3>Исключения по датам</h3>
            <p>Для сокращенных дней, переносов или разовых открытий добавь отдельную дату в список.</p>
          </div>
          <button class="add-button" type="button" @click="addOverride">Добавить дату</button>
        </div>

        <div v-if="sortedOverrides.length" class="override-list">
          <div v-for="dateKey in sortedOverrides" :key="dateKey" class="override-row">
            <label class="date-field">
              <span>Дата</span>
              <input
                :value="dateKey"
                type="date"
                @input="renameOverrideDate(dateKey, ($event.target as HTMLInputElement).value)"
              />
            </label>

            <label class="toggle-label">
              <input
                :checked="modelValue.staff_digest_schedule_overrides[dateKey].enabled"
                type="checkbox"
                @change="
                  updateOverride(dateKey, {
                    enabled: ($event.target as HTMLInputElement).checked,
                  })
                "
              />
              <span>Рабочий день</span>
            </label>

            <div
              v-if="modelValue.staff_digest_schedule_overrides[dateKey].enabled"
              class="time-grid time-grid-override"
            >
              <label class="time-field">
                <span>С</span>
                <input
                  :value="modelValue.staff_digest_schedule_overrides[dateKey].start"
                  type="time"
                  @input="
                    updateOverride(dateKey, {
                      start: ($event.target as HTMLInputElement).value,
                    })
                  "
                />
              </label>
              <label class="time-field">
                <span>До</span>
                <input
                  :value="modelValue.staff_digest_schedule_overrides[dateKey].end"
                  type="time"
                  @input="
                    updateOverride(dateKey, {
                      end: ($event.target as HTMLInputElement).value,
                    })
                  "
                />
              </label>
            </div>

            <span v-else class="day-off">Выходной</span>

            <button class="remove-button" type="button" @click="removeOverride(dateKey)">Удалить</button>
          </div>
        </div>

        <p v-else class="empty-note">Для открытого месяца исключений пока нет.</p>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.edit-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(18rem, 1fr);
  gap: 1rem;
}

.calendar-panel,
.section-card {
  display: grid;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid var(--color-text-200);
  border-radius: 1rem;
  background: linear-gradient(180deg, var(--color-background-50), var(--color-background-100));
}

.editor-stack {
  display: grid;
  gap: 1rem;
}

.section-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}

.section-heading h3 {
  margin: 0;
  font-size: var(--text-base);
}

.section-heading p,
.section-note,
.empty-note,
.day-off {
  margin: 0.35rem 0 0;
  color: var(--color-text-600);
  font-size: var(--text-xs);
  line-height: 1.55;
}

.day-list,
.override-list {
  display: grid;
  gap: 0.85rem;
}

.day-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.day-row,
.override-row {
  display: grid;
  gap: 0.85rem;
  padding: 0.9rem;
  border-radius: 0.9rem;
  background: var(--color-background-50);
  border: 1px solid var(--color-text-200);
}

.toggle-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text-800);
  font-size: var(--text-sm);
}

.time-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.75rem;
}

.time-grid-override {
  max-width: 20rem;
}

.time-field,
.date-field {
  display: grid;
  gap: 0.4rem;
}

.time-field span,
.date-field span {
  color: var(--color-text-600);
  font-size: var(--text-xs);
}

input[type="time"],
input[type="date"] {
  width: 100%;
  min-height: 2.75rem;
  padding: 0.65rem 0.85rem;
  border: 1px solid var(--color-text-300);
  border-radius: 0.8rem;
  background: var(--color-background-50);
  color: var(--color-text-950);
  font-size: var(--text-sm);
}

input[type="checkbox"] {
  width: 1.1rem;
  height: 1.1rem;
  accent-color: var(--color-primary-500);
}

.add-button,
.remove-button {
  min-height: 2.35rem;
  padding: 0.55rem 0.9rem;
  border: 1px solid var(--color-text-300);
  border-radius: 999px;
  background: var(--color-background-100);
  color: var(--color-text-900);
  font-size: var(--text-sm);
  font-weight: 600;
  cursor: pointer;
}

.remove-button {
  justify-self: start;
}

.add-button:hover,
.remove-button:hover {
  background: var(--color-primary-100);
  border-color: var(--color-primary-300);
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
  .edit-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .section-heading,
  .holiday-list-header,
  .day-main {
    align-items: flex-start;
    flex-direction: column;
  }

  .time-grid {
    grid-template-columns: 1fr;
  }
}
</style>
