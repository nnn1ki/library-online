<script setup lang="ts">
import { computed, ref, watch } from "vue";

import type { LibrarySettings } from "@core/api/types";
import EditableSettingsSection from "../shared/EditableSettingsSection.vue";
import ReaderNotificationSettingsView from "./ReaderNotificationSettingsView.vue";
import ReaderNotificationSettingsEdit from "./ReaderNotificationSettingsEdit.vue";

type ReaderNotificationSettings = Pick<
  LibrarySettings,
  "reader_status_notifications_enabled" | "reader_notification_statuses"
>;

const props = defineProps<{
  modelValue: ReaderNotificationSettings;
  saving: boolean;
  syncToken: number;
}>();

const emit = defineEmits<{
  save: [value: ReaderNotificationSettings];
}>();

const isEditing = ref(false);
const pendingSyncToken = ref<number | null>(null);
const draft = ref<ReaderNotificationSettings>({
  ...props.modelValue,
  reader_notification_statuses: [...props.modelValue.reader_notification_statuses],
});

watch(
  () => props.modelValue,
  (value) => {
    draft.value = {
      ...value,
      reader_notification_statuses: [...value.reader_notification_statuses],
    };
    if (!props.saving) isEditing.value = false;
  },
  { deep: true, immediate: true }
);

const canSave = computed(() => JSON.stringify(draft.value) !== JSON.stringify(props.modelValue));

watch(
  () => props.syncToken,
  (value) => {
    if (pendingSyncToken.value === null || value === pendingSyncToken.value) return;
    draft.value = {
      ...props.modelValue,
      reader_notification_statuses: [...props.modelValue.reader_notification_statuses],
    };
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
  draft.value = {
    ...props.modelValue,
    reader_notification_statuses: [...props.modelValue.reader_notification_statuses],
  };
  isEditing.value = true;
}

function cancelEditing() {
  draft.value = {
    ...props.modelValue,
    reader_notification_statuses: [...props.modelValue.reader_notification_statuses],
  };
  isEditing.value = false;
  pendingSyncToken.value = null;
}

function saveChanges() {
  pendingSyncToken.value = props.syncToken;
  emit("save", {
    ...draft.value,
    reader_notification_statuses: [...draft.value.reader_notification_statuses],
  });
}
</script>

<template>
  <EditableSettingsSection
    kicker="Уведомления читателю"
    :can-save="canSave"
    :is-editing="isEditing"
    :is-saving="saving"
    @cancel="cancelEditing"
    @edit="startEditing"
    @save="saveChanges"
  >
    <template #view>
      <ReaderNotificationSettingsView :model-value="modelValue" />
    </template>

    <template #edit>
      <ReaderNotificationSettingsEdit :model-value="draft" @update:model-value="draft = $event" />
    </template>
  </EditableSettingsSection>
</template>
