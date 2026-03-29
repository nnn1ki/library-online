<script setup lang="ts">
import { computed } from "vue";

import type { StaffNotificationRecipient } from "@core/api/types";

const props = defineProps<{
  recipients: StaffNotificationRecipient[];
  loading?: boolean;
}>();

const alwaysCount = computed(
  () =>
    props.recipients.filter((recipient) => recipient.staff_notification_mode === "always").length
);
const disabledCount = computed(
  () =>
    props.recipients.filter((recipient) => recipient.staff_notification_mode === "disabled").length
);
</script>

<template>
  <div class="summary-inline">
    <span
      >Сотрудников: <strong>{{ loading ? "..." : recipients.length }}</strong></span
    >
    <span
      >Всегда: <strong>{{ loading ? "..." : alwaysCount }}</strong></span
    >
    <span
      >Отключены: <strong>{{ loading ? "..." : disabledCount }}</strong></span
    >
  </div>
</template>

<style scoped lang="scss">
.summary-inline {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem 1.25rem;
  padding: 0.85rem 1rem;
  border-radius: 0.95rem;
  border: 1px solid var(--color-text-200);
  background: var(--color-background-100);
  color: var(--color-text-600);
  font-size: var(--text-sm);
}

.summary-inline strong {
  color: var(--color-text-900);
}

@media (max-width: 720px) {
  .summary-inline {
    flex-direction: column;
    gap: 0.35rem;
  }
}
</style>
