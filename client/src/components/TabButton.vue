<template>
    <button type="button" @click="$emit('click')" :class="{ 'active': isActive }" class="tab-button">
        <span class="label">{{ label }}</span>
        <span>
            Всего {{ countAll }}
        </span>
    </button>
</template>

<script setup lang="ts">
import { computed } from "vue" 
import { useNotificationStore } from '@/stores/notificationStore';
const notifStore = useNotificationStore();
defineProps({
    label: {
        type: String,
        required: true
    },
    countAll: {
        type: Number,
        default: 0
    },
    isActive: {
        type: Boolean,
        default: false
    },
    tabNumber: {
        type: Number,
        default: 0
    }
});

defineEmits(['click']);
</script>


<style lang="scss" scoped>
.tab-button {
    background-color: aqua;
}

.active {
    background-color: rgb(0, 255, 98);
}
</style>