<template>
  <div class="container">
    <ul class="nav nav-tabs">
      <li class="nav-item">
        <a
          class="nav-link"
          :class="{ active: currentTab === tabsNumbers.new }"
          @click="currentTab = tabsNumbers.new"
          href="#"
        >
          Новые <span class="badge bg-danger">{{ newOrdersCount }}</span>
        </a>
      </li>
      <li class="nav-item">
        <a
          class="nav-link"
          :class="{ active: currentTab === tabsNumbers.processing }"
          @click="currentTab = tabsNumbers.processing"
          href="#"
        >
          В работе <span class="badge bg-danger">{{ processingOrdersCount }}</span>
        </a>
      </li>
      <li class="nav-item">
        <a
          class="nav-link"
          :class="{ active: currentTab === tabsNumbers.ready }"
          @click="currentTab = tabsNumbers.ready"
          href="#"
        >
          Готовые к выдаче <span class="badge bg-danger">{{ readyOrdersCount }}</span>
        </a>
      </li>
    </ul>
    <OrderList :orders="currentData" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import OrderList from "@/components/OrderList.vue";
import { useToast } from "vue-toastification";
import { useNotificationStore } from "@/stores/notificationStore";
import { fetchNewOrders, fetchProcessingOrders, fetchReadyOrders } from "@/api/order";
import type { UserOrder } from "@/api/types";

const toast = useToast();
const notifStore = useNotificationStore();

interface TabConfig {
  label: string;
  fetchFn: () => Promise<UserOrder[]>;
  interval: number;
  data: UserOrder[];
  timerId?: number;
}

const tabsNumbers = {
  new: 0,
  processing: 1,
  ready: 2,
};

const currentTab = ref(tabsNumbers.new);
const tabs = ref<TabConfig[]>([
  {
    label: "Новые",
    fetchFn: fetchNewOrders,
    interval: 5000,
    data: [],
  },
  {
    label: "В работе",
    fetchFn: fetchProcessingOrders,
    interval: 10000,
    data: [],
  },
  {
    label: "Готовы",
    fetchFn: fetchReadyOrders,
    interval: 10000,
    data: [],
  },
]);

const newOrdersCount = computed(() => tabs.value[tabsNumbers.new].data.length);
const processingOrdersCount = computed(() => tabs.value[tabsNumbers.processing].data.length);
const readyOrdersCount = computed(() => tabs.value[tabsNumbers.ready].data.length);

const startAllIntervals = () => {
  tabs.value.forEach((tab, index) => {
    const processNewOrders = (newData: UserOrder[]): UserOrder[] => {
      const newOrders = newData.filter((order) => !notifStore.loadedOrderIds.has(order.id));
      newData.forEach((order) => {
        notifStore.addToLoadedOrders(order.id);
      });
      return newOrders;
    };

    tab.timerId = window.setInterval(async () => {
      if (document.visibilityState === "visible") {
        try {
          const data = await tab.fetchFn();
          console.log(`Обновление вкладки ${tab.label}:`);
          const newData = processNewOrders(data);
          if (newData.length > 0) {
            showNotifications(newData);
          }

          tabs.value[index].data = data;
          console.log("notifStore.loadedOrderIds", notifStore.loadedOrderIds);
        } catch (error) {
          console.error(`Ошибка обновления вкладки ${tab.label}:`, error);
        }
      }
    }, tab.interval);

    tab.fetchFn().then((data) => {
      tabs.value[index].data = data;
      processNewOrders(tabs.value[index].data);
    });
  });
};

const showNotifications = (orders: UserOrder[]) => {
  orders.forEach((order) => {
    toast.success(order.id.toString());
  });
};

const clearAllIntervals = () => {
  tabs.value.forEach((tab) => {
    if (tab.timerId) {
      clearInterval(tab.timerId);
    }
  });
};

const currentData = computed<UserOrder[]>((): UserOrder[] => {
  switch (currentTab.value) {
    case tabsNumbers.new:
      return tabs.value[tabsNumbers.new].data;
    case tabsNumbers.processing:
      return tabs.value[tabsNumbers.processing].data;
    case tabsNumbers.ready:
      return tabs.value[tabsNumbers.ready].data;
    default:
      return [];
  }
});

onMounted(async () => {
  startAllIntervals();
});

onUnmounted(() => {
  clearAllIntervals();
});

document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "hidden") {
    clearAllIntervals();
  } else {
    startAllIntervals();
  }
});
</script>

<style lang="scss" scoped>
.tab-buttons {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
</style>
