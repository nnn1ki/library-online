<script setup lang="ts">
import { computed, ref, watch } from "vue";

import type { LibrarySettings } from "@core/api/types";
import EditableSettingsSection from "../shared/EditableSettingsSection.vue";
import GeneralSettingsView from "./GeneralSettingsView.vue";
import GeneralSettingsEdit from "./GeneralSettingsEdit.vue";

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
  saving: boolean;
  syncToken: number;
}>();

const emit = defineEmits<{
  save: [value: GeneralSettings];
}>();

const isEditing = ref(false);
const pendingSyncToken = ref<number | null>(null);
const draft = ref<GeneralSettings>({ ...props.modelValue });

watch(
  () => props.modelValue,
  (value) => {
    draft.value = { ...value };
    if (!props.saving) isEditing.value = false;
  },
  { deep: true, immediate: true }
);

const canSave = computed(() => JSON.stringify(draft.value) !== JSON.stringify(props.modelValue));

watch(
  () => props.syncToken,
  (value) => {
    if (pendingSyncToken.value === null || value === pendingSyncToken.value) return;
    draft.value = { ...props.modelValue };
    isEditing.value = false;
    pendingSyncToken.value = null;
  }
);

watch(
  () => props.saving,
  (saving) => {
    if (!saving && pendingSyncToken.value === props.syncToken) pendingSyncToken.value = null;
  }
);

function startEditing() {
  draft.value = { ...props.modelValue };
  isEditing.value = true;
}

function cancelEditing() {
  draft.value = { ...props.modelValue };
  isEditing.value = false;
  pendingSyncToken.value = null;
}

function saveChanges() {
  pendingSyncToken.value = props.syncToken;
  emit("save", { ...draft.value });
}
</script>

<template>
  <EditableSettingsSection
    kicker="Основные правила"
    :can-save="canSave"
    :is-editing="isEditing"
    :is-saving="saving"
    @cancel="cancelEditing"
    @edit="startEditing"
    @save="saveChanges"
  >
    <template #view>
      <GeneralSettingsView :model-value="modelValue" />
    </template>

    <template #edit>
      <GeneralSettingsEdit :model-value="draft" @update:model-value="draft = $event" />
    </template>
  </EditableSettingsSection>
</template>
