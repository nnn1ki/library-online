import { api } from "./axios";
import type {
  StaffStats,
  PaginatedStaff,
  StaffFilters,
  Order,
  UserOrder,
  StaffNotificationMode,
  StaffNotificationRecipient,
} from "./types";

export async function getStaff(filters?: StaffFilters): Promise<PaginatedStaff> {
  try {
    const { data } = await api.get("/api/staff/", {
      params: filters,
      paramsSerializer: {
        indexes: null,
      },
    });
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка сотрудников", error);
    throw error;
  }
}

export async function getStaffStats(filters?: StaffFilters): Promise<PaginatedStaff> {
  try {
    const { data } = await api.get("/api/staff/stats/", {
      params: filters,
      paramsSerializer: {
        indexes: null,
      },
    });
    return data;
  } catch (error) {
    console.error("Ошибка при получении статистики сотрудников", error);
    throw error;
  }
}

export async function getStaffOrders(staffId: number): Promise<UserOrder[]> {
  try {
    const { data } = await api.get(`/api/staff/${staffId}/orders/`);
    return data;
  } catch (error) {
    console.error(`Ошибка при получении заказов сотрудника ${staffId}`, error);
    throw error;
  }
}

export async function getStaffOrderDetail(staffId: number, orderId: number): Promise<Order> {
  try {
    const { data } = await api.get(`/api/staff/${staffId}/orders/${orderId}/`);
    return data;
  } catch (error) {
    console.error(`Ошибка при получении заказа ${orderId} сотрудника ${staffId}`, error);
    throw error;
  }
}

export async function searchStaff(query: string): Promise<StaffNotificationRecipient[]> {
  return getStaffNotificationRecipients(query);
}

export async function getStaffNotificationRecipients(
  query = ""
): Promise<StaffNotificationRecipient[]> {
  try {
    const { data } = await api.get("/api/staff/notification-recipients/", {
      params: { q: query },
    });
    return data;
  } catch (error) {
    console.error("Ошибка при получении сотрудников для рассылки", error);
    throw error;
  }
}

export async function updateStaffNotificationMode(
  profileId: number,
  staffNotificationMode: StaffNotificationMode
): Promise<StaffNotificationRecipient> {
  try {
    const { data } = await api.patch(`/api/staff/${profileId}/notification-mode/`, {
      staff_notification_mode: staffNotificationMode,
    });
    return data;
  } catch (error) {
    console.error(`Ошибка при обновлении режима уведомлений сотрудника ${profileId}`, error);
    throw error;
  }
}
