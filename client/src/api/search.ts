import axios from "axios";
import type { Book } from "./types";

const options = { method: "GET", url: "/api/book/" };

export async function searchBooks(
  library: number,
  expression: string
): Promise<Book[]> {
  try {
    const { data } = await axios.request({
      params: {
        library: library,
        expression: expression,
      },
      ...options,
    });
    console.log("/api/book/", data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка книг", error);
    throw error;
  }
}
