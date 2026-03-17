<script setup lang="ts">
withDefaults(
  defineProps<{
    title?: string;
    kicker: string;
    badge?: string;
    isEditing?: boolean;
    isSaving?: boolean;
    canSave?: boolean;
    showEditButton?: boolean;
  }>(),
  {
    title: "",
    badge: "",
    isEditing: false,
    isSaving: false,
    canSave: false,
    showEditButton: true,
  }
);

defineEmits<{
  edit: [];
  cancel: [];
  save: [];
}>();
</script>

<template>
  <section class="settings-card">
    <header class="card-heading">
      <div>
        <p class="card-kicker">{{ kicker }}</p>
        <h2 v-if="title">{{ title }}</h2>
      </div>

      <div class="card-actions">
        <span v-if="badge" class="card-badge">{{ badge }}</span>

        <template v-if="showEditButton">
          <button v-if="!isEditing" class="edit-button" type="button" @click="$emit('edit')">
            Редактировать
          </button>

          <div v-else class="edit-actions">
            <button class="ghost-button" type="button" @click="$emit('cancel')">Отмена</button>
            <button
              class="edit-button"
              :disabled="!canSave || isSaving"
              type="button"
              @click="$emit('save')"
            >
              Сохранить
            </button>
          </div>
        </template>
      </div>
    </header>

    <div v-if="isSaving" class="loading-panel" aria-live="polite">
      <div class="spinner"></div>
      <p>Обновляем настройки...</p>
    </div>

    <div v-else-if="isEditing" class="edit-panel">
      <slot name="edit" />
    </div>

    <div v-else class="view-panel">
      <slot name="view" />
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

.card-heading {
  display: flex;
  align-items: center;
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

.card-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.edit-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
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

.edit-button,
.ghost-button {
  min-height: 2.35rem;
  padding: 0.55rem 0.9rem;
  border-radius: 999px;
  font-size: var(--text-sm);
  font-weight: 600;
  cursor: pointer;
}

.edit-button {
  border: 1px solid var(--color-text-300);
  background: var(--color-background-100);
  color: var(--color-text-900);
}

.edit-button:hover {
  background: var(--color-primary-100);
  border-color: var(--color-primary-300);
}

.edit-button:disabled {
  cursor: default;
  opacity: 0.55;
}

.ghost-button {
  border: 1px solid var(--color-text-300);
  background: transparent;
  color: var(--color-text-800);
}

.ghost-button:hover {
  background: var(--color-background-100);
}

.loading-panel {
  display: grid;
  align-content: center;
  justify-items: center;
  gap: 0.6rem;
  min-height: 10rem;
  padding: 1.25rem;
  border-radius: 1rem;
  background: linear-gradient(180deg, var(--color-background-50), var(--color-background-100));
  border: 1px dashed var(--color-text-200);
}

.loading-panel p {
  margin: 0;
  color: var(--color-text-600);
  font-size: var(--text-sm);
}

.spinner {
  width: 2.5rem;
  height: 2.5rem;
  border: 3px solid var(--color-background-300);
  border-top-color: var(--color-primary-500);
  border-radius: 999px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 640px) {
  .settings-card {
    padding: 1rem;
  }

  .card-heading,
  .card-actions,
  .edit-actions {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
