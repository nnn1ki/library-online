import { api } from "./axios";
import type { 
  ModeratorPaginatedOrders, 
  ModeratorOrdersFilters,
  Order
} from "./types";

export async function getModeratorOrders(
  filters?: ModeratorOrdersFilters
): Promise<ModeratorPaginatedOrders> {
  try {
    const { statuses, ...restFilters } = filters ?? {};
    const { data } = await api.get("/api/moderator/orders/", {
      params: {
        ...restFilters,
        ...(statuses && statuses.length > 0 && {
          'statuses[]': statuses
        })
      },
      paramsSerializer: {
        indexes: null
      }
    });
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка заказов", error);
    throw error;
  }
}

export async function getModeratorOrderDetail(orderId: number): Promise<Order> {
  try {
    const { data } = await api.get(`/api/moderator/orders/${orderId}/`);
    return data;
  } catch (error) {
    console.error(`Ошибка при получении деталей заказа ${orderId}`, error);
    throw error;
  }
}