<script setup lang="ts">
import { onBeforeMount, onBeforeUnmount, ref, watch } from "vue";

import { getStaffNotificationRecipients, updateStaffNotificationMode } from "@core/api/staff";
import type { StaffNotificationMode, StaffNotificationRecipient } from "@core/api/types";
import EditableSettingsSection from "../shared/EditableSettingsSection.vue";
import StaffRecipientsSettingsView from "./StaffRecipientsSettingsView.vue";
import StaffRecipientsSettingsEdit from "./StaffRecipientsSettingsEdit.vue";

const recipients = ref<StaffNotificationRecipient[]>([]);
const searchQuery = ref("");
const loading = ref(false);
const updatingIds = ref<number[]>([]);
const errorMessage = ref<string | null>(null);

let searchTimer: ReturnType<typeof setTimeout> | null = null;

onBeforeMount(async () => {
  await loadRecipients();
});

onBeforeUnmount(() => {
  if (searchTimer) clearTimeout(searchTimer);
});

watch(searchQuery, (value) => {
  if (searchTimer) clearTimeout(searchTimer);

  searchTimer = setTimeout(() => {
    loadRecipients(value);
  }, 300);
});

async function loadRecipients(query = searchQuery.value) {
  loading.value = true;
  errorMessage.value = null;

  try {
    recipients.value = await getStaffNotificationRecipients(query.trim());
  } catch (error) {
    console.error("Не удалось загрузить сотрудников для рассылки", error);
    errorMessage.value = "Не удалось загрузить список сотрудников. Попробуйте обновить страницу.";
  } finally {
    loading.value = false;
  }
}

async function handleModeUpdate(payload: { profileId: number; mode: StaffNotificationMode }) {
  if (updatingIds.value.includes(payload.profileId)) return;

  updatingIds.value = [...updatingIds.value, payload.profileId];

  try {
    const updatedRecipient = await updateStaffNotificationMode(payload.profileId, payload.mode);
    recipients.value = recipients.value.map((recipient) =>
      recipient.id === updatedRecipient.id ? updatedRecipient : recipient
    );
    errorMessage.value = null;
  } catch (error) {
    console.error("Не удалось обновить режим уведомлений сотрудника", error);
    errorMessage.value = "Не удалось обновить режим уведомлений. Попробуйте еще раз.";
  } finally {
    updatingIds.value = updatingIds.value.filter((id) => id !== payload.profileId);
  }
}
</script>

<template>
  <EditableSettingsSection kicker="Получатели сводки" :is-editing="true" :show-edit-button="false">
    <template #edit>
      <div class="block-stack">
        <StaffRecipientsSettingsView :loading="loading" :recipients="recipients" />
        <StaffRecipientsSettingsEdit
          v-model:search-query="searchQuery"
          :error-message="errorMessage"
          :loading="loading"
          :recipients="recipients"
          :updating-ids="updatingIds"
          @update-mode="handleModeUpdate"
        />
      </div>
    </template>
  </EditableSettingsSection>
</template>

<style scoped lang="scss">
.block-stack {
  display: grid;
  gap: 1rem;
}
</style>
