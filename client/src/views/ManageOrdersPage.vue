<template>
  <div class="container">
    {{ tabs[0].data }} <br>
    ============================ <br>
    {{ tabs[1].data }} <br>
    ============================ <br>
    {{ tabs[2].data }} <br>
    ============================ <br>
  </div>
</template>

<script setup lang="ts">

import { ref, computed, onMounted, onUnmounted } from 'vue';
import OrderList from '@/components/OrderList.vue';

import {
  fetchNewOrders,
  fetchProcessingOrders,
  fetchReadyOrders,
} from '@/api/order';

import type { UserOrder } from '@/api/types';

interface TabConfig {
  label: string;
  fetchFn: () => Promise<UserOrder[]>;
  interval: number;
  data: UserOrder[];
  timerId?: number;
}

const tabs = ref<TabConfig[]>([
  { 
    label: 'Новые',
    fetchFn: fetchNewOrders,
    interval: 5000, 
    data: []
  },
  {
    label: 'В работе',
    fetchFn: fetchProcessingOrders,
    interval: 10000, 
    data: []
  },
  {
    label: 'Готовы',
    fetchFn: fetchReadyOrders,
    interval: 10000, 
    data: []
  }
]);

const startAllIntervals = () => {
  tabs.value.forEach((tab, index) => {
    tab.timerId = window.setInterval(async () => {
      if (document.visibilityState === 'visible') {
        try {
          const data = await tab.fetchFn();
          console.log(`Обновли влкадку ${tab.label}:`);
          tabs.value[index].data = data;
        } catch (error) {
          console.error(`Ошибка обновления вкладки ${tab.label}:`, error);
        }
      }
    }, tab.interval);
    
    tab.fetchFn().then(data => tabs.value[index].data = data);
  });
};

const clearAllIntervals = () => {
  tabs.value.forEach(tab => {
    if (tab.timerId) {
      clearInterval(tab.timerId);
    }
  });
};

onMounted(async () => {
  startAllIntervals();
});
onUnmounted(()=>{
  clearAllIntervals();
});

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'hidden') {
    clearAllIntervals();
  } else {
    startAllIntervals();
  }
});


</script>