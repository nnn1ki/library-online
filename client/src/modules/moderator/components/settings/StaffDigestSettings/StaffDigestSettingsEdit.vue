<script setup lang="ts">
import type { LibrarySettings } from "@core/api/types";

type StaffDigestSettings = Pick<
  LibrarySettings,
  "staff_digest_enabled" | "staff_notification_active_hours" | "staff_digest_stale_order_hours"
>;

const props = defineProps<{
  modelValue: StaffDigestSettings;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: StaffDigestSettings];
}>();

function updateField<K extends keyof StaffDigestSettings>(key: K, value: StaffDigestSettings[K]) {
  emit("update:modelValue", {
    ...props.modelValue,
    [key]: value,
  });
}
</script>

<template>
  <div class="form-grid">
    <label class="toggle-card field-card-wide">
      <div>
        <span class="field-title">Включить рассылку сотрудникам</span>
        <p class="field-note">Общий переключатель рассылки о необработанных заказах.</p>
      </div>
      <input
        :checked="modelValue.staff_digest_enabled"
        type="checkbox"
        @change="updateField('staff_digest_enabled', ($event.target as HTMLInputElement).checked)"
      />
    </label>

    <label class="field-card">
      <span class="field-title">Недавняя активность сотрудника</span>
      <span class="field-note">Через сколько часов после последней активности сотрудник считается активным.</span>
      <input
        :value="modelValue.staff_notification_active_hours"
        type="number"
        @input="
          updateField(
            'staff_notification_active_hours',
            Number(($event.target as HTMLInputElement).value)
          )
        "
      />
    </label>

    <label class="field-card">
      <span class="field-title">Интервал отправки дайджеста</span>
      <span class="field-note">Как часто система может отправлять дайджест сотрудникам.</span>
      <input
        :value="modelValue.staff_digest_stale_order_hours"
        type="number"
        @input="
          updateField(
            'staff_digest_stale_order_hours',
            Number(($event.target as HTMLInputElement).value)
          )
        "
      />
    </label>
  </div>
</template>

<style scoped lang="scss">
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.9rem;
}

.field-card,
.toggle-card {
  display: grid;
  gap: 0.65rem;
  padding: 1rem;
  border: 1px solid var(--color-text-200);
  border-radius: 1rem;
  background: linear-gradient(180deg, var(--color-background-50), var(--color-background-100));
}

.field-card-wide {
  grid-column: 1 / -1;
}

.toggle-card {
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
}

.field-title {
  color: var(--color-text-900);
  font-size: var(--text-sm);
  font-weight: 700;
}

.field-note {
  color: var(--color-text-600);
  font-size: var(--text-xs);
  line-height: 1.55;
}

input[type="number"] {
  width: 100%;
  min-height: 2.85rem;
  padding: 0.65rem 0.85rem;
  border: 1px solid var(--color-text-300);
  border-radius: 0.8rem;
  background: var(--color-background-50);
  color: var(--color-text-950);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  font-size: var(--text-sm);
}

input[type="checkbox"] {
  width: 1.1rem;
  height: 1.1rem;
  accent-color: var(--color-primary-500);
}

input[type="number"]:focus {
  outline: none;
  border-color: var(--color-primary-400);
  box-shadow: 0 0 0 3px var(--color-primary-100);
}

@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .toggle-card {
    grid-template-columns: 1fr;
  }
}
</style>
