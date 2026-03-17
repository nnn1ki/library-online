<script setup lang="ts">
import { computed, ref, watch } from "vue";

import EditableSettingsSection from "../shared/EditableSettingsSection.vue";
import BrandingSettingsView from "./BrandingSettingsView.vue";
import BrandingSettingsEdit from "./BrandingSettingsEdit.vue";

const props = defineProps<{
  currentLogoLabel: string;
  saving: boolean;
  syncToken: number;
}>();

const emit = defineEmits<{
  save: [value: File | null];
}>();

const isEditing = ref(false);
const draftFile = ref<File | null>(null);
const pendingSyncToken = ref<number | null>(null);

watch(
  () => props.currentLogoLabel,
  () => {
    if (!props.saving) {
      draftFile.value = null;
      isEditing.value = false;
    }
  },
  { immediate: true }
);

const canSave = computed(() => Boolean(draftFile.value));

watch(
  () => props.syncToken,
  (value) => {
    if (pendingSyncToken.value === null || value === pendingSyncToken.value) return;
    draftFile.value = null;
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
  draftFile.value = null;
  isEditing.value = true;
}

function cancelEditing() {
  draftFile.value = null;
  isEditing.value = false;
  pendingSyncToken.value = null;
}

function saveChanges() {
  pendingSyncToken.value = props.syncToken;
  emit("save", draftFile.value);
}
</script>

<template>
  <EditableSettingsSection
    kicker="Логотип"
    :can-save="canSave"
    :is-editing="isEditing"
    :is-saving="saving"
    @cancel="cancelEditing"
    @edit="startEditing"
    @save="saveChanges"
  >
    <template #view>
      <BrandingSettingsView :current-logo-label="currentLogoLabel" />
    </template>

    <template #edit>
      <BrandingSettingsEdit @update:file="draftFile = $event" />
    </template>
  </EditableSettingsSection>
</template>
