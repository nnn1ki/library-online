<script setup lang="ts">
import { computed, ref, watch } from "vue";

import type { LibrarySettings } from "@core/api/types";
import { sendStaffSummary } from "@core/api/settings";
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
const isSendingSummary = ref(false);
const summaryMessage = ref<string | null>(null);

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

async function handleSendSummary() {
  isSendingSummary.value = true;
  summaryMessage.value = null;

  try {
    const result = await sendStaffSummary();
    if (result.reason === "empty") {
      summaryMessage.value = "Сейчас нет заказов для отправки.";
      return;
    }

    if (result.reason === "recipients") {
      summaryMessage.value = "Сводка собрана, но получателей для отправки не нашлось.";
      return;
    }

    summaryMessage.value = `Сводка отправлена: новых ${result.fresh_count}, ожидающих ${result.stale_count}.`;
  } catch (error) {
    console.error("Не удалось отправить сводку сотрудникам", error);
    summaryMessage.value = "Не удалось отправить сводку. Попробуйте еще раз.";
  } finally {
    isSendingSummary.value = false;
  }
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
    <template #actions>
      <button
        class="summary-button"
        :disabled="isSendingSummary || saving"
        type="button"
        @click="handleSendSummary"
      >
        {{ isSendingSummary ? "Отправляем..." : "Отправить" }}
      </button>
    </template>

    <template #view>
      <div class="section-stack">
        <StaffDigestSettingsView :model-value="modelValue" />
        <p v-if="summaryMessage" class="summary-message">{{ summaryMessage }}</p>
      </div>
    </template>

    <template #edit>
      <div class="section-stack">
        <StaffDigestSettingsEdit :model-value="draft" @update:model-value="draft = $event" />
        <p v-if="summaryMessage" class="summary-message">{{ summaryMessage }}</p>
      </div>
    </template>
  </EditableSettingsSection>
</template>

<style scoped lang="scss">
.section-stack {
  display: grid;
  gap: 0.85rem;
}

.summary-button {
  min-height: 2.35rem;
  padding: 0.55rem 0.9rem;
  border: 1px solid var(--color-text-300);
  border-radius: 999px;
  background: var(--color-background-100);
  color: var(--color-text-900);
  font-size: var(--text-sm);
  font-weight: 600;
  cursor: pointer;
}

.summary-button:hover:not(:disabled) {
  background: var(--color-primary-100);
  border-color: var(--color-primary-300);
}

.summary-button:disabled {
  cursor: default;
  opacity: 0.6;
}

.summary-message {
  margin: 0;
  color: var(--color-text-600);
  font-size: var(--text-sm);
  line-height: 1.5;
}
</style>
