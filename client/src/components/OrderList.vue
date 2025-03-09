<template>
    <div v-if="loading">Загрузка...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else class="orders">
      <div v-for="order in orders" :key="order.id" class="order">
        <h3>Заказ #{{ order.id }}</h3>
        <p>Статус: {{ currentStatus(order) }}</p>
        <p>Пользователь: {{ order.user.username }}</p>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import type { UserOrder } from '@/api/types';
  
  const props = defineProps<{
    fetchFunction: () => Promise<UserOrder[]>;
  }>();
  
  const orders = ref<UserOrder[]>([]);
  const loading = ref(true);
  const error = ref<string | null>(null);
  
  const currentStatus = (order: UserOrder) => 
    order.statuses.slice(-1)[0].status;
  
  onMounted(async () => {
    try {
      orders.value = await props.fetchFunction();
    } catch (err) {
      console.log("Ошибка загрузки")
    } finally {
      loading.value = false;
    }
  });
  </script>