<template>
    <button type="button" @click="$emit('click')" :class="{ 'active': isActive }" class="tab-button">
        <span class="label">{{ label }}</span>
        <span>
            Всего {{ countAll }}
        </span>
        <span v-if="!isActive && countNew > 0" class="badge">
            Новые {{ countNew }} <br>
        </span>
    </button>
</template>

<script setup lang="ts">
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
    countNew: {
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