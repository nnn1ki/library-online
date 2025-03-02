<template>
  <div class="container">
    <div v-if="orderStore.selectedBooks.length > 0">
      <CurrentOrderCard :order="orderStore.selectedBooks" />
    </div>
    <div v-for="order in orders" :key="order.id" class="row">
      <OrderCard :order="order" :num="order.id" @cancel="openCancelModal" />
    </div>
    <LoadingModal v-if="loading" />
  </div>
  <NotAllowedBanner v-model="notAllowedModalOpen" />
  <ConfirmationModal v-model="confirmationModalOpen" title="Отмена заказа" text="Вы точно хотите отменить заказ?"
    @confirm="handleConfirmCancel" />
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";

import { ordersList } from "@/api/order";
import { type Order } from "@/api/types";
import { useOrderStore } from "@/stores/orderStore";
import { useAuthStore } from "@/stores/auth";
import OrderCard from "@/components/OrderCard.vue";
import LoadingModal from "@/components/LoadingModal.vue";
import CurrentOrderCard from "@/components/CurrentOrderCard.vue";
import NotAllowedBanner from "@/components/NotAllowedBanner.vue";
import ConfirmationModal from "@/components/ConfirmationModal.vue";
const orders = ref<Order[]>([]);
const loading = ref(false);
const orderStore = useOrderStore();
const authStore = useAuthStore();
const notAllowedModalOpen = ref(false);
const confirmationModalOpen = ref(false);
const cancelOrderId = ref<number | null>();

onMounted(async () => {
  await fetchOrders();
});

const fetchOrders = (async () => {
  try {
    if (authStore.isAuthenticated) {
      loading.value = true;
      await fetchOrderList();
    }
    else {
      notAllowedModalOpen.value = true;
    }
  } catch (error) {
    console.error('Error fetching orders:', error);
  } finally {
    loading.value = false;
  }
})

// todo reactivity
// windowOrders -> no auth -> no orders -> go login
// windowLogin -> login
// windowOrders -> fetchOrders
watch(() => authStore.isAuthenticated, async (newVal) => {
  if (newVal) {
    window.location.reload()
  }
});

async function fetchOrderList() {
  orders.value = (await ordersList()).reverse();
}

const handleConfirmCancel = (async () => {
  console.log(cancelOrderId.value);
  if (cancelOrderId.value !== null && cancelOrderId.value !== undefined) {
    orderStore.handleDeleteOrder(cancelOrderId.value);
  }
  await fetchOrders();
});

const openCancelModal = (orderId: number) => {
  cancelOrderId.value = orderId;
  confirmationModalOpen.value = true;
};
</script>

<style scoped lang="scss">
.order-summary {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.order-summary h2 {
  margin-bottom: 20px;
  font-size: 1.8rem;
}

.order-info p {
  margin: 10px 0;
  font-size: 1.1rem;
}

.email-input {
  margin: 20px 0;
}

.email-input input {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.book-list ul {
  list-style: none;
  padding-left: 0;
}

.book-list li {
  margin-bottom: 5px;
}

.order-button {
  margin-top: 20px;
}

.order-button button {
  width: 100%;
  padding: 12px;
  font-size: 1.1rem;
  border-radius: 8px;
}
</style>
