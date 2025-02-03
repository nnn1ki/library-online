<template>
  <div class="container">
    <div v-if="orderStore.selectedBooks.length > 0">
      <strong>
        Продолжить оформление заказа
      </strong>
      <CurrenOrderCard :order="orderStore.selectedBooks"/>
    </div>
    <div v-for="(order, i) in orders" :key="order.id" class="row">
      <order-card :order="order" :num="i + 1" />
    </div>
    <div v-if="loading">
      <loadingModal/>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";

import { ordersList } from "@/api/order";
import { type Order } from "@/api/types";
import { useOrderStore } from "@/stores/orderStore";
import OrderCard from "@/components/OrderCard.vue";
import loadingModal from "@/components/loadingModal.vue";
import CurrenOrderCard from "@/components/CurrenOrderCard.vue";
const orders = ref<Order[]>([]);
const loading = ref(false)
const orderStore = useOrderStore();
onMounted(async () => {
  loading.value = true;
  orders.value = await ordersList();
  loading.value = false;
});

</script>

<style scoped>
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