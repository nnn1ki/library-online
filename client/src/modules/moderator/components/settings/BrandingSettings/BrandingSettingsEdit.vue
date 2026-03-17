<script setup lang="ts">
const emit = defineEmits<{
  "update:file": [value: File | null];
}>();

function onFileChange(event: Event) {
  const target = event.target as HTMLInputElement;
  emit("update:file", target.files?.[0] ?? null);
}
</script>

<template>
  <label class="upload-card">
    <span class="field-title">Выбрать новый логотип</span>
    <span class="field-note">Поддерживаются обычные изображения для сайта.</span>
    <input accept="image/*" type="file" @change="onFileChange" />
  </label>
</template>

<style scoped lang="scss">
.upload-card {
  display: grid;
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
</style>
