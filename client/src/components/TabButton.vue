<template>
  <button type="button" @click="$emit('click')" :class="{ active: isActive }" class="tab-button">
    <span class="label">{{ label }}</span>
    <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
      {{ countAll }}
      <span class="visually-hidden">непрочитанные сообщения</span>
    </span>
  </button>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from "vue";
import { useNotificationStore } from "@/stores/notificationStore";

const notifStore = useNotificationStore();

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  countAll: {
    type: Number,
    default: 0,
  },
  isActive: {
    type: Boolean,
    default: false,
  },
  tabNumber: {
    type: Number,
    default: 0,
  },
});

const emit = defineEmits(["click"]);
</script>

<style lang="scss" scoped>
.tab-button {
  background-color: aqua;
  position: relative;
}

.active {
  background-color: rgb(0, 255, 98);
}
</style>
