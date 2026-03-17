<script setup lang="ts">
import { computed, ref, watch } from "vue";

import type { LibrarySettings } from "@core/api/types";
import EditableSettingsSection from "../shared/EditableSettingsSection.vue";
import StaffDigestSettingsView from "./StaffDigestSettingsView.vue";
import StaffDigestSettingsEdit from "./StaffDigestSettingsEdit.vue";

type StaffDigestSettings = Pick<
  LibrarySettings,
  "staff_digest_enabled" | "staff_notification_active_hours" | "staff_digest_stale_order_hours"
>;

const props = defineProps<{
  modelValue: StaffDigestSettings;
  saving: boolean;
  syncToken: number;
}>();

const emit = defineEmits<{
  save: [value: StaffDigestSettings];
}>();

const isEditing = ref(false);
const pendingSyncToken = ref<number | null>(null);
const draft = ref<StaffDigestSettings>({ ...props.modelValue });

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
    kicker="Уведомления сотрудникам"
    :can-save="canSave"
    :is-editing="isEditing"
    :is-saving="saving"
    @cancel="cancelEditing"
    @edit="startEditing"
    @save="saveChanges"
  >
    <template #view>
      <StaffDigestSettingsView :model-value="modelValue" />
    </template>

    <template #edit>
      <StaffDigestSettingsEdit :model-value="draft" @update:model-value="draft = $event" />
    </template>
  </EditableSettingsSection>
</template>
