import axios from "axios";
import type {
  BorrowedBook,
  Order,
  UserOrder,
  OrderStatusEnum,
  OrderCheckingInfo,
} from "@/api/types";

export async function updateOrderStatus(
  orderId: number,
  newStatus: OrderStatusEnum,
  description?: string
) {
  const statusUpdate = {
    description: description,
    status: newStatus,
    date: new Date().toISOString(),
  };

  try {
    const orderData = await getOrder(orderId);
    const currentOrder: Order = orderData;
    console.log(currentOrder);

    const updatedStatuses = [...currentOrder.statuses, statusUpdate];
    console.log(updatedStatuses);

    await axios.put(`/api/staff/order/${orderId}/`, { status: statusUpdate, books: [] });
    console.log(`Статус заказа ${orderId} добавлен: "${newStatus}"`);
  } catch (error) {
    console.error("Ошибка при обновлении статуса заказа", error);
    throw error;
  }
}

export async function ordersList(): Promise<Order[]> {
  try {
    const { data } = await axios.get("/api/order/");
    console.log("/api/order/", data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка заказов", error);
    throw error;
  }
}

export async function fetchNewOrders(): Promise<UserOrder[]> {
  try {
    const response = await axios.get("/api/staff/order/?status=new");
    console.log("Ответ сервера:", response);
    return response.data;
  } catch (error: unknown) {
    console.error(
      "Ошибка при получении новых заказов:",
      error instanceof Error ? error.message : String(error)
    );
    throw error;
  }
}

export async function fetchProcessingOrders(): Promise<UserOrder[]> {
  try {
    const response = await axios.get("/api/staff/order/?status=processing");
    return response.data;
  } catch (error) {
    console.error("Ошибка при получении заказов в процессе:", error);
    throw error;
  }
}

export async function fetchReadyOrders(): Promise<UserOrder[]> {
  try {
    const response = await axios.get("/api/staff/order/?status=ready");
    return response.data;
  } catch (error) {
    console.error("Ошибка при получении готовых заказов:", error);
    throw error;
  }
}

export async function fetchArchiveOrders(): Promise<UserOrder[]> {
  try {
    const response = await axios.get("/api/staff/order/?status=done");
    return response.data;
  } catch (error) {
    console.error("Ошибка при получении готовых заказов:", error);
    throw error;
  }
}

export async function getOrder(orderId: number): Promise<Order> {
  try {
    const { data } = await axios.get(`/api/order/${orderId}/`);
    console.log(`/api/order/${orderId}`, data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении заказа", error);
    throw error;
  }
}

export async function checkOrder(orderId: number): Promise<OrderCheckingInfo> {
  try {
    const { data } = await axios.get(`/api/staff/order/check/${orderId}/`);
    console.log(`/api/order/${orderId}`, data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении заказа", error);
    throw error;
  }
}

export async function getOrderStaff(orderId: number): Promise<Order> {
  try {
    const { data } = await axios.get(`/api/staff/order/${orderId}/`);
    console.log(`/api/staff/order/${orderId}`, data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении заказа", error);
    throw error;
  }
}

export async function createOrder(libraryId: number, bookIds: string[], borrowedBookIds: number[]) {
  try {
    await axios.post("/api/order/", {
      library: libraryId,
      books: bookIds,
      borrowed: borrowedBookIds,
    });
  } catch (error) {
    console.error("Ошибка при создании заказа", error);
    throw error;
  }
}

export async function editOrder(
  orderId: number,
  libraryId: number,
  bookIds: number[],
  borrowedBookIds: number[]
) {
  try {
    await axios.put(`/api/order/${orderId}/`, {
      library: libraryId,
      books: bookIds,
      borrowed: borrowedBookIds,
    });
  } catch (error) {
    console.error("Ошибка при редактировании заказа", error);
    throw error;
  }
}

export async function deleteOrder(orderId: number) {
  try {
    await axios.delete(`/api/order/${orderId}/`);
  } catch (error) {
    console.error("Ошибка при удалении заказа", error);
    throw error;
  }
}

export async function borrowedList(): Promise<BorrowedBook[]> {
  try {
    const { data } = await axios.get("/api/borrowed/");
    console.log("/api/borrowed/", data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка взятых книг", error);
    throw error;
  }
}
