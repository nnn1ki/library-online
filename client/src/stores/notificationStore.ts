// stores/orders.ts
import { defineStore } from 'pinia';
import { ref, reactive } from 'vue';

export const useNotificationStore = defineStore('orders', () => {
  const seenOrderIds = reactive(new Set<number>());
  const loadedOrderIds = reactive(new Set<number>());

  const addLoadedOrders = (orders: { id: number }[]) => {
    orders.forEach(order => {
      loadedOrderIds.add(order.id);
    });
  };

  const addToLoadedOrders = (id: number) => {
      loadedOrderIds.add(id);
  };

  const markAsSeen = (orderId: number) => {
    seenOrderIds.add(orderId);
  };

  const getNewOrdersCount = (orders: { id: number }[]) => {
    return orders.filter(order => 
      !seenOrderIds.has(order.id) && loadedOrderIds.has(order.id)
    ).length;
  };

  return { seenOrderIds, loadedOrderIds, addLoadedOrders, markAsSeen, getNewOrdersCount, addToLoadedOrders };
});