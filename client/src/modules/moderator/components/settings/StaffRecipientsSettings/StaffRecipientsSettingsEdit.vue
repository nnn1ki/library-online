<script setup lang="ts">
import { computed } from "vue";

import { staffNotificationModeLabels } from "@core/api/types";
import type {
  StaffNotificationMode,
  StaffNotificationRecipient,
} from "@core/api/types";

const props = defineProps<{
  searchQuery: string;
  recipients: StaffNotificationRecipient[];
  loading?: boolean;
  updatingIds: number[];
  errorMessage?: string | null;
}>();

const emit = defineEmits<{
  "update:searchQuery": [value: string];
  "update-mode": [payload: { profileId: number; mode: StaffNotificationMode }];
}>();

const modeOptions: Array<{ value: StaffNotificationMode; label: string }> = [
  {
    value: "auto",
    label: "По активности",
  },
  {
    value: "always",
    label: "Всегда",
  },
  {
    value: "disabled",
    label: "Не слать",
  },
];

const updatingSet = computed(() => new Set(props.updatingIds));

function isUpdating(profileId: number) {
  return updatingSet.value.has(profileId);
}

function updateMode(profileId: number, mode: StaffNotificationMode) {
  emit("update-mode", { profileId, mode });
}

function getDisplayName(recipient: StaffNotificationRecipient) {
  const nameFromUser = [recipient.first_name, recipient.last_name].filter(Boolean).join(" ").trim();
  return nameFromUser || recipient.fullname || recipient.username;
}

function formatLastSeen(value: string | null) {
  if (!value) return "Активность не зафиксирована";

  return new Intl.DateTimeFormat("ru-RU", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(value));
}
</script>

<template>
  <div class="edit-stack">
    <div class="toolbar">
      <label class="search-field">
        <span class="search-label">Поиск сотрудника</span>
        <input
          :value="searchQuery"
          class="search-input"
          placeholder="ФИО, логин или отдел"
          type="text"
          @input="emit('update:searchQuery', ($event.target as HTMLInputElement).value)"
        />
      </label>

      <p class="toolbar-note">
        Пустой поиск показывает всех сотрудников.
      </p>
    </div>

    <div v-if="loading" class="state-panel">
      <div class="spinner"></div>
      <span>Ищем сотрудников...</span>
    </div>

    <div v-else-if="!recipients.length" class="state-panel state-panel-muted">
      <span>Сотрудники по текущему запросу не найдены.</span>
    </div>

    <div v-else class="recipient-list">
      <div v-if="errorMessage" class="error-panel">
        {{ errorMessage }}
      </div>

      <article v-for="recipient in recipients" :key="recipient.id" class="recipient-card">
        <div class="recipient-main">
          <div class="recipient-copy">
            <h3>{{ getDisplayName(recipient) }}</h3>
            <p class="recipient-meta">
              <span>{{ recipient.department || "Отдел не указан" }}</span>
              <span>@{{ recipient.username }}</span>
              <span v-if="recipient.current_role">Роль: {{ recipient.current_role }}</span>
            </p>
          </div>

          <div class="recipient-status">
            <strong>{{ staffNotificationModeLabels[recipient.staff_notification_mode] }}</strong>
            <span class="last-seen">{{ formatLastSeen(recipient.last_seen) }}</span>
          </div>
        </div>

        <div class="mode-grid">
          <button
            v-for="option in modeOptions"
            :key="option.value"
            class="mode-button"
            :class="{
              'mode-button-active': recipient.staff_notification_mode === option.value,
              'mode-button-loading': isUpdating(recipient.id),
            }"
            :disabled="isUpdating(recipient.id)"
            type="button"
            @click="updateMode(recipient.id, option.value)"
          >
            <span class="mode-button-label">{{ option.label }}</span>
          </button>
        </div>
      </article>
    </div>
  </div>
</template>

<style scoped lang="scss">
.edit-stack {
  display: grid;
  gap: 0.85rem;
}

.toolbar {
  display: grid;
  gap: 0.65rem;
}

.search-field {
  display: grid;
  gap: 0.45rem;
}

.search-label {
  color: var(--color-text-700);
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.search-input {
  width: 100%;
  min-height: 3rem;
  padding: 0.8rem 0.95rem;
  border: 1px solid var(--color-text-200);
  border-radius: 0.95rem;
  background: var(--color-background-100);
  color: var(--color-text-900);
  font-size: var(--text-sm);
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary-400);
  box-shadow: 0 0 0 3px rgba(var(--color-primary-500-rgb, 102, 69, 186), 0.12);
}

.toolbar-note {
  margin: 0;
  color: var(--color-text-600);
  font-size: var(--text-xs);
  line-height: 1.45;
}

.state-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.65rem;
  min-height: 8rem;
  padding: 1rem;
  border-radius: 1rem;
  border: 1px dashed var(--color-text-200);
  background: var(--color-background-100);
  color: var(--color-text-700);
  text-align: center;
}

.state-panel-muted {
  color: var(--color-text-600);
}

.spinner {
  width: 1.2rem;
  height: 1.2rem;
  border: 2px solid var(--color-background-300);
  border-top-color: var(--color-primary-500);
  border-radius: 999px;
  animation: spin 0.8s linear infinite;
}

.recipient-list {
  display: grid;
  gap: 0.7rem;
}

.error-panel {
  padding: 0.85rem 1rem;
  border-radius: 0.9rem;
  border: 1px solid var(--color-accent-200);
  background: var(--background-status-error);
  color: var(--color-status-error);
  font-size: var(--text-sm);
}

.recipient-card {
  display: grid;
  gap: 0.75rem;
  padding: 0.9rem 1rem;
  border-radius: 0.95rem;
  border: 1px solid var(--color-text-200);
  background: var(--color-background-50);
}

.recipient-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.recipient-copy {
  display: grid;
  gap: 0.35rem;
}

.recipient-copy h3 {
  margin: 0;
  font-size: var(--text-base);
}

.recipient-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem 0.8rem;
  margin: 0;
  color: var(--color-text-600);
  font-size: var(--text-xs);
}

.recipient-status {
  display: grid;
  gap: 0.1rem;
  min-width: 10rem;
  justify-items: end;
  text-align: right;
}

.recipient-status strong {
  font-size: var(--text-sm);
}

.last-seen {
  color: var(--color-text-600);
  font-size: var(--text-xs);
}

.mode-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.mode-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.3rem;
  padding: 0.55rem 0.85rem;
  border: 1px solid var(--color-text-200);
  border-radius: 999px;
  background: var(--color-background-50);
  color: var(--color-text-900);
  cursor: pointer;
  transition:
    border-color 0.2s ease,
    background 0.2s ease,
    transform 0.2s ease;
}

.mode-button:hover:not(:disabled) {
  border-color: var(--color-primary-300);
  background: var(--color-primary-100);
  transform: translateY(-1px);
}

.mode-button-active {
  border-color: var(--color-primary-500);
  background: var(--color-primary-100);
  box-shadow: none;
}

.mode-button-loading {
  opacity: 0.7;
}

.mode-button:disabled {
  cursor: default;
}

.mode-button-label {
  font-size: var(--text-sm);
  font-weight: 700;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 960px) {
  .recipient-main {
    flex-direction: column;
    align-items: flex-start;
  }

  .recipient-status {
    min-width: 0;
    justify-items: start;
    text-align: left;
  }

  .mode-grid {
    width: 100%;
  }
}
</style>
