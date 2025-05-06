<template>
  <div class="container">
    <div v-if="orderStore.selectedBooks.length > 0">
      <CurrentOrderCard :order="orderStore.selectedBooks" />
    </div>
    <div v-for="order in orders" :key="order.id">
      <OrderCard :order="order" :num="order.id" @cancel="openCancelModal" />
    </div>
    <LoadingModal v-model="loading" />
  </div>
  <NotAllowedBanner v-model="notAllowedModalOpen" />
  <ConfirmationModal
    v-model="confirmationModalOpen"
    title="Отмена заказа"
    text="Вы точно хотите отменить заказ?"
    @confirm="handleConfirmCancel"
  />
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";

import { ordersList } from "@lib/shared/api/order";
import { type Order } from "@lib/shared/api/types";
import { useOrderStore } from "@/stores/orderStore";
import { useAuthStore } from "@/stores/auth";
import OrderCard from "@/layouts/OrderCard.vue";
import LoadingModal from "@lib/shared/components/LoadingModal.vue";
import CurrentOrderCard from "@/layouts/CurrentOrderCard.vue";
import NotAllowedBanner from "@/layouts/NotAllowedBanner.vue";
import ConfirmationModal from "@lib/shared/components/ConfirmationModal.vue";
import { useAuthentication } from "@/composables/auth";
import { useRouter } from "vue-router";

const orders = ref<Order[]>([]);
const loading = ref(false);
const orderStore = useOrderStore();
const authStore = useAuthStore();
const notAllowedModalOpen = ref(false);
const confirmationModalOpen = ref(false);
const cancelOrderId = ref<number | null>();

const router = useRouter();

onMounted(async () => {
  await fetchOrders();
});

const fetchOrders = async () => {
  try {
    if (authStore.isAuthenticated) {
      loading.value = true;
      await fetchOrderList();
    } else {
      notAllowedModalOpen.value = true;
    }
  } catch (error) {
    console.error("Error fetching orders:", error);
  } finally {
    loading.value = false;
  }
};

useAuthentication((isAuthenticated) => {
  if (!isAuthenticated) {
    router.push("/");
  }
});

async function fetchOrderList() {
  orders.value = (await ordersList()).reverse();
}

const handleConfirmCancel = async () => {
  console.log(cancelOrderId.value);
  if (cancelOrderId.value !== null && cancelOrderId.value !== undefined) {
    orderStore.handleDeleteOrder(cancelOrderId.value);
  }
  await fetchOrders();
};

const openCancelModal = (orderId: number) => {
  cancelOrderId.value = orderId;
  confirmationModalOpen.value = true;
};
</script>

<style scoped lang="scss"></style>
