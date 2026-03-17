<script setup lang="ts">
import { computed } from "vue";

import type {
  LibrarySettings,
  StaffDigestWeekSchedule,
  StaffScheduleDayKey,
  StaffScheduleWindow,
} from "@core/api/types";
import { staffScheduleDayLabels } from "@core/api/types";

type StaffScheduleSettings = Pick<
  LibrarySettings,
  "staff_digest_week_schedule" | "staff_digest_schedule_overrides"
>;

const props = defineProps<{
  modelValue: StaffScheduleSettings;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: StaffScheduleSettings];
}>();

const weekDays = Object.entries(staffScheduleDayLabels) as Array<[StaffScheduleDayKey, string]>;

function normalizeWindow(window: StaffScheduleWindow, fallback: StaffScheduleWindow): StaffScheduleWindow {
  if (!window.enabled) return { enabled: false };
  return {
    enabled: true,
    start: window.start ?? fallback.start ?? "10:00",
    end: window.end ?? fallback.end ?? "17:00",
  };
}

function emitValue(value: StaffScheduleSettings) {
  emit("update:modelValue", value);
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
  const candidate = new Date();

  while (true) {
    const dateKey = [
      candidate.getFullYear(),
      String(candidate.getMonth() + 1).padStart(2, "0"),
      String(candidate.getDate()).padStart(2, "0"),
    ].join("-");
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
    nextOverrides[dateKey === oldDateKey ? newDateKey : dateKey] = dateKey === oldDateKey
      ? normalizeWindow(value, getDefaultOverrideWindow(newDateKey))
      : { ...value };
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

const sortedOverrides = computed(() =>
  Object.keys(props.modelValue.staff_digest_schedule_overrides).sort((left, right) =>
    left.localeCompare(right)
  )
);
</script>

<template>
  <div class="edit-stack">
    <div class="section-card">
      <div class="section-heading">
        <div>
          <h3>Базовый шаблон недели</h3>
          <p>Используется по умолчанию. Праздники из календаря выше автоматически делают день нерабочим.</p>
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
          <p>Если неделя нестандартная, можно вручную поправить отдельные даты.</p>
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

      <p v-else class="empty-note">Пока нет отдельных дат. Используется только шаблон недели.</p>
    </div>
  </div>
</template>

<style scoped lang="scss">
.edit-stack {
  display: grid;
  gap: 1rem;
}

.section-card {
  display: grid;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid var(--color-text-200);
  border-radius: 1rem;
  background: linear-gradient(180deg, var(--color-background-50), var(--color-background-100));
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

.day-row,
.override-row {
  display: grid;
  gap: 0.85rem;
  padding: 0.9rem;
  border-radius: 0.9rem;
  background: var(--color-background-50);
  border: 1px solid var(--color-text-200);
}

.day-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
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

@media (max-width: 640px) {
  .section-heading,
  .day-main {
    align-items: flex-start;
    flex-direction: column;
  }

  .time-grid {
    grid-template-columns: 1fr;
  }
}
</style>
