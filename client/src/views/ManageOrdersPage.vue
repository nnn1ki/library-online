<template>
  <div class="container">
    <div class="tab-buttons">
      <TabButton label="Новые" :count-new="tabs[tabsNumbers.new].newOrdersCnt" :count-all="newOrdersCount"
        :is-active="currentTab === tabsNumbers.new" @click="currentTab = tabsNumbers.new" />
      <TabButton label="В работе" :count-new="tabs[tabsNumbers.processing].newOrdersCnt"
        :count-all="processingOrdersCount" :is-active="currentTab === tabsNumbers.processing"
        @click="currentTab = tabsNumbers.processing" />
      <TabButton label="Готовые к выдаче" :count-new="tabs[tabsNumbers.ready].newOrdersCnt"
        :count-all="readyOrdersCount" :is-active="currentTab === tabsNumbers.ready"
        @click="currentTab = tabsNumbers.ready" />
    </div>
    <OrderList :orders="currentData" />
  </div>
</template>

<script setup lang="ts">

import { ref, computed, onMounted, onUnmounted } from 'vue';
import OrderList from '@/components/OrderList.vue';
import TabButton from '@/components/TabButton.vue';
import { useToast } from "vue-toastification";

import {
  fetchNewOrders,
  fetchProcessingOrders,
  fetchReadyOrders,
} from '@/api/order';

import type { UserOrder } from '@/api/types';

const toast = useToast();

interface TabConfig {
  label: string;
  fetchFn: () => Promise<UserOrder[]>;
  interval: number;
  data: UserOrder[];
  newOrdersCnt: number,
  timerId?: number;
}


const tabsNumbers = {
  new: 0,
  processing: 1,
  ready: 2,
}

const currentTab = ref(tabsNumbers.new)

const tabs = ref<TabConfig[]>([
  {
    label: 'Новые',
    fetchFn: fetchNewOrders,
    interval: 5000,
    newOrdersCnt: 0,
    data: []
  },
  {
    label: 'В работе',
    fetchFn: fetchProcessingOrders,
    interval: 10000,
    newOrdersCnt: 0,
    data: []
  },
  {
    label: 'Готовы',
    fetchFn: fetchReadyOrders,
    interval: 10000,
    newOrdersCnt: 0,
    data: []
  }
]);

const newOrdersCount = computed(() => tabs.value[tabsNumbers.new].data.length);
const processingOrdersCount = computed(() => tabs.value[tabsNumbers.processing].data.length);
const readyOrdersCount = computed(() => tabs.value[tabsNumbers.ready].data.length);


const startAllIntervals = () => {
  tabs.value.forEach((tab, index) => {
    const existingIds = new Set<number>();

    const processNewOrders = (newData: UserOrder[]) => {
      const newOrders = newData.filter(order => !existingIds.has(order.id));

      existingIds.clear();
      newData.forEach(order => existingIds.add(order.id));

      if (newOrders.length > 0) {
        tabs.value[index].newOrdersCnt = newOrders.length;
        showNotifications(newOrders);
      } else {
        tabs.value[index].newOrdersCnt = 0;
      }
    };
    tab.timerId = window.setInterval(async () => {
      if (document.visibilityState === 'visible') {
        try {
          const data = await tab.fetchFn();
          console.log(`Обновли влкадку ${tab.label}:`);
          processNewOrders(data);
          tabs.value[index].data = data;
        } catch (error) {
          console.error(`Ошибка обновления вкладки ${tab.label}:`, error);
        }
      }
    }, tab.interval);

    tab.fetchFn().then(data => tabs.value[index].data = data);
  });
};

const showNotifications = (orders: UserOrder[]) => {
  orders.forEach(order => {
    toast.success(order.id.toString());
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