import axios from "axios";
import type { BorrowedBook, Order, PaginatedOrders, ShortOrder } from "@/api/types";

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

export async function fetchNewOrders(): Promise<ShortOrder> {
  try {
    const response = await axios.get("/api/order/new/");
    return response.data;
  } catch (error) {
    console.error("Ошибка при получении новых заказов:", error);
    throw error;
  }
}

export async function fetchProcessingOrders(): Promise<ShortOrder> {
  try {
    const response = await axios.get("/api/order/processing/");
    return response.data;
  } catch (error) {
    console.error("Ошибка при получении заказов в процессе:", error);
    throw error;
  }
}

export async function fetchReadyOrders(): Promise<ShortOrder> {
  try {
    const response = await axios.get("/api/order/ready/");
    return response.data;
  } catch (error) {
    console.error("Ошибка при получении готовых заказов:", error);
    throw error;
  }
}

export async function fetchDoneOrders(page: number = 1): Promise<PaginatedOrders> {
  try {
    const { data } = await axios.get(`/api/order/done/`, {
      params: { page },
    });
    console.log(`/api/order/done/?page=${page}`, data);
    return data;
  } catch (error) {
    console.error(`Ошибка при получении заказов со статусом ${status}`, error);
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
