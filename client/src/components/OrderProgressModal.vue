<template>
    <ModalDialog v-model="open">
        <div class="order-modal">
            <div class="modal-header">
                <h3>Оформление заказа</h3>
            </div>

            <div class="steps-container">
                <div v-for="(step, index) in steps" :key="index" class="step-item" :class="{
                    active: currentStep === index,
                    completed: currentStep > index,
                    error: step.error
                }">
                    <div class="step-indicator">
                        <span v-if="currentStep > index">✓</span>
                        <span v-else>{{ index + 1 }}</span>
                    </div>
                    <div class="step-content">
                        <div class="step-title">{{ step.title }}</div>
                        <div v-if="step.error" class="step-error">{{ step.error }}</div>
                    </div>
                </div>
            </div>

            <div v-if="isSuccess" class="result-message success">
                <h4>✅ Заказ успешно оформлен!</h4>
                <p v-if="orderId">
                    Номер вашего заказа:
                    <strong>{{ orderId }}</strong>
                </p>
            </div>

            <div v-if="isError" class="result-message error">
                <h4>❌ Ошибка оформления заказа</h4>
                <p>{{ errorMessage }}</p>
            </div>
        </div>
    </ModalDialog>
</template>

<script setup lang="ts">
import ModalDialog from "@/components/ModalDialog.vue";
const open = defineModel<boolean>({ required: true });
defineProps({
    currentStep: Number,
    steps: Array as () => Array<{ title: string; error: string | null }>,
    isSuccess: Boolean,
    isError: Boolean,
    orderId: String,
    errorMessage: String
});
</script>


<style lang="scss" scoped>
.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.step-item {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    color: var(--color-text-600);
}

.step-item.active {
    color: var(--color-text-900);
    font-weight: bold;
}

.step-item.completed {
    color: var(--color-status-done);
}

.step-item.error .step-title {
    color: var(--color-status-error);
}

.step-indicator {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: var(--color-background-200);
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 10px;
    flex-shrink: 0;
    color: var(--color-text-500);
}

.step-item.active .step-indicator {
    background: var(--color-status-new);
    color: var(--color-background-50);
}

.step-item.completed .step-indicator {
    background: var(--color-status-done);
    color: var(--color-background-100);
}

.step-item.error .step-indicator {
    background: var(--color-status-error);
    color: var(--color-background-100);
}

.step-error {
    color: var(--color-status-error);
    font-size: 0.9em;
    margin-top: 5px;
}

.result-message {
    text-align: center;
    margin-top: 20px;
    color: var(--color-text-700);
}

.result-message.success {
    color: var(--color-status-done);
}

.result-message.error {
    color: var(--color-status-error);
}

@media (max-width: 600px) {
    .step-content {
        font-size: 0.9em;
    }
}
</style>
