<script setup lang="ts">
import { computed, ref, watch } from "vue";

import type {
  LibrarySettings,
  StaffDigestScheduleOverrides,
  StaffDigestWeekSchedule,
} from "@core/api/types";
import EditableSettingsSection from "../shared/EditableSettingsSection.vue";
import WorkScheduleSettingsView from "./WorkScheduleSettingsView.vue";
import WorkScheduleSettingsEdit from "./WorkScheduleSettingsEdit.vue";

type WorkScheduleSettings = Pick<
  LibrarySettings,
  "holidays" | "staff_digest_week_schedule" | "staff_digest_schedule_overrides"
>;

function cloneWeekSchedule(schedule: StaffDigestWeekSchedule): StaffDigestWeekSchedule {
  return Object.fromEntries(
    Object.entries(schedule).map(([dayKey, value]) => [dayKey, { ...value }])
  ) as StaffDigestWeekSchedule;
}

function cloneOverrides(overrides: StaffDigestScheduleOverrides): StaffDigestScheduleOverrides {
  return Object.fromEntries(
    Object.entries(overrides).map(([dateKey, value]) => [dateKey, { ...value }])
  );
}

function cloneModelValue(value: WorkScheduleSettings): WorkScheduleSettings {
  return {
    holidays: [...value.holidays],
    staff_digest_week_schedule: cloneWeekSchedule(value.staff_digest_week_schedule),
    staff_digest_schedule_overrides: cloneOverrides(value.staff_digest_schedule_overrides),
  };
}

const props = defineProps<{
  modelValue: WorkScheduleSettings;
  saving: boolean;
  syncToken: number;
}>();

const emit = defineEmits<{
  save: [value: WorkScheduleSettings];
}>();

const isEditing = ref(false);
const pendingSyncToken = ref<number | null>(null);
const draft = ref<WorkScheduleSettings>(cloneModelValue(props.modelValue));

watch(
  () => props.modelValue,
  (value) => {
    draft.value = cloneModelValue(value);
    if (!props.saving) isEditing.value = false;
  },
  { deep: true, immediate: true }
);

const canSave = computed(() => JSON.stringify(draft.value) !== JSON.stringify(props.modelValue));

watch(
  () => props.syncToken,
  (value) => {
    if (pendingSyncToken.value === null || value === pendingSyncToken.value) return;
    draft.value = cloneModelValue(props.modelValue);
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
  draft.value = cloneModelValue(props.modelValue);
  isEditing.value = true;
}

function cancelEditing() {
  draft.value = cloneModelValue(props.modelValue);
  isEditing.value = false;
  pendingSyncToken.value = null;
}

function saveChanges() {
  pendingSyncToken.value = props.syncToken;
  emit("save", cloneModelValue(draft.value));
}
</script>

<template>
  <EditableSettingsSection
    kicker="График работы"
    :can-save="canSave"
    :is-editing="isEditing"
    :is-saving="saving"
    @cancel="cancelEditing"
    @edit="startEditing"
    @save="saveChanges"
  >
    <template #view>
      <WorkScheduleSettingsView :model-value="modelValue" />
    </template>

    <template #edit>
      <WorkScheduleSettingsEdit :model-value="draft" @update:model-value="draft = $event" />
    </template>
  </EditableSettingsSection>
</template>
