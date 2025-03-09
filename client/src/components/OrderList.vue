<template>
      <div v-for="order in orders" :key="order.id" class="order">
        <h3>Заказ #{{ order.id }}</h3>
        <p>Пользователь: {{ order.user.username }}</p>
      </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import type { UserOrder } from "@/api/types"
  const props = defineProps<{
    orders: UserOrder[]
  }>();    
  </script>
