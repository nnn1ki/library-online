<script setup lang="ts">
import type { LibrarySettings } from "@core/api/types";

type GeneralSettings = Pick<
  LibrarySettings,
  | "max_books_per_order"
  | "max_books_per_reader"
  | "max_borrow_days"
  | "new_order_wait"
  | "processing_order_wait"
>;

const props = defineProps<{
  modelValue: GeneralSettings;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: GeneralSettings];
}>();

function updateField<K extends keyof GeneralSettings>(key: K, value: GeneralSettings[K]) {
  emit("update:modelValue", {
    ...props.modelValue,
    [key]: value,
  });
}
</script>

<template>
  <div class="form-grid">
    <label class="field-card">
      <span class="field-title">Максимум книг в заказе</span>
      <span class="field-note">Сколько позиций можно добавить в один заказ.</span>
      <input
        :value="modelValue.max_books_per_order"
        type="number"
        @input="
          updateField('max_books_per_order', Number(($event.target as HTMLInputElement).value))
        "
      />
    </label>

    <label class="field-card">
      <span class="field-title">Максимум книг на руках</span>
      <span class="field-note">Лимит всех активных выдач читателя.</span>
      <input
        :value="modelValue.max_books_per_reader"
        type="number"
        @input="
          updateField('max_books_per_reader', Number(($event.target as HTMLInputElement).value))
        "
      />
    </label>

    <label class="field-card">
      <span class="field-title">Срок выдачи</span>
      <span class="field-note">Количество дней на пользование книгой.</span>
      <input
        :value="modelValue.max_borrow_days"
        type="number"
        @input="updateField('max_borrow_days', Number(($event.target as HTMLInputElement).value))"
      />
    </label>

    <label class="field-card">
      <span class="field-title">Ожидание нового заказа</span>
      <span class="field-note">Через сколько часов новый заказ считается задержанным.</span>
      <input
        :value="modelValue.new_order_wait"
        type="number"
        @input="updateField('new_order_wait', Number(($event.target as HTMLInputElement).value))"
      />
    </label>

    <label class="field-card field-card-wide">
      <span class="field-title">Задержка исполнения заказа</span>
      <span class="field-note">Порог для заказов, которые уже находятся в работе.</span>
      <input
        :value="modelValue.processing_order_wait"
        type="number"
        @input="
          updateField('processing_order_wait', Number(($event.target as HTMLInputElement).value))
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

.field-card {
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

input {
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

input:focus {
  outline: none;
  border-color: var(--color-primary-400);
  box-shadow: 0 0 0 3px var(--color-primary-100);
}

@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
