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
      <li class="nav-item">
        <a
          class="nav-link"
          :class="{ active: currentTab === tabsNumbers.archive }"
          @click="currentTab = tabsNumbers.archive"
          href="#"
        >
          Архив <span class="badge bg-danger">{{ readyOrdersCount }}</span>
        </a>
      </li>
    </ul>
    <OrderList @get-order="fetchOrder" :orders="currentData" />
    <ModalOrderDetails
      v-if="selectedOrder"
      :order="selectedOrder"
      @close="selectedOrder = null"
      @next-order-status="handleUpdateOrderStatus"
    />
    <LoadingModal v-model="isLoading" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import OrderList from "@/components/OrderList.vue";
import ModalOrderDetails from "@/components/ModalOrderDetails.vue";
import LoadingModal from "@/components/LoadingModal.vue";
import { useToast } from "vue-toastification";
import { useNotificationStore } from "@/stores/notificationStore";
import {
  fetchNewOrders,
  fetchProcessingOrders,
  fetchReadyOrders,
  fetchArchiveOrders,
} from "@/api/order";
import type { UserOrder, Order, OrderStatusEnum } from "@/api/types";
import { getOrderStaff, updateOrderStatus } from "@/api/order";
import { RefSymbol } from "@vue/reactivity";
const toast = useToast();
const notifStore = useNotificationStore();
const isLoading = ref(false);
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
  archive: 3,
};

const currentTab = ref(tabsNumbers.new);

const tabs = ref<TabConfig[]>([
  {
    label: "Новые",
    fetchFn: fetchNewOrders,
    interval: 500000,
    data: [],
  },
  {
    label: "В работе",
    fetchFn: fetchProcessingOrders,
    interval: 1000000,
    data: [],
  },
  {
    label: "Готовые",
    fetchFn: fetchReadyOrders,
    interval: 1000000,
    data: [],
  },
  {
    label: "Архив",
    fetchFn: fetchArchiveOrders,
    interval: 1000000,
    data: [],
  },
]);

const newOrdersCount = computed(() => tabs.value[tabsNumbers.new].data.length);
const processingOrdersCount = computed(() => tabs.value[tabsNumbers.processing].data.length);
const readyOrdersCount = computed(() => tabs.value[tabsNumbers.ready].data.length);
const archiveOrdersCount = computed(() => tabs.value[tabsNumbers.archive].data.length);
const selectedOrder = ref<Order | null>(null);

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

const fetchOrder = async (orderId: number) => {
  isLoading.value = true;
  selectedOrder.value = await getOrderStaff(orderId);
  isLoading.value = false;
};

async function handleUpdateOrderStatus(orderId: number, newStatus: OrderStatusEnum) {
  const description = "Временное описание";
  try {
    await updateOrderStatus(orderId, newStatus, description);
  } catch (error) {
    console.error("Ошибка при обновлении статуса заказа", error);
  }
}

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
