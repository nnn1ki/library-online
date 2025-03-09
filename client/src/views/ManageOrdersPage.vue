<template>
  <div class="container">
    <div class="tab-buttons">
      <button type="button" @click="currentTab = tabsNumbers.new">
        Новые
      </button>
      <button type="button" @click="currentTab = tabsNumbers.processing">
        В работе
      </button>
      <button type="button" @click="currentTab = tabsNumbers.ready">
        Готовые к выдаче
      </button>
    </div>
    <OrderList :orders="currentData"/>
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

const currentTab = ref(0)

const tabsNumbers = {
  new: 0,
  processing: 1,
  ready: 2,
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

const currentData = computed<UserOrder[]>((): UserOrder[] => {
  switch (currentTab.value) {
    case tabsNumbers.new:
      return tabs.value[tabsNumbers.new].data
    case tabsNumbers.processing:
      return tabs.value[tabsNumbers.processing].data
    case tabsNumbers.ready:
      return tabs.value[tabsNumbers.ready].data
    default:
      return []
  }
})

onMounted(async () => {
  startAllIntervals();
});
onUnmounted(() => {
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


<style lang="scss" scoped>
.tab-buttons {
  display: felx;
  flex-direction: row;
  justify-content: space-between;
}
</style>