import axios from "axios";
import type { Book } from "./types";

export async function searchBooks(
  expression: string,
  library?: number
): Promise<Book[]> {
  try {
    const { data } = await axios.get("/api/book/", {
      params: {
        expression: expression,
        library: library,
      }
    });
    console.log("/api/book/", data);
    return data;
  } catch (error) {
    console.error("Ошибка при получении списка книг", error);
    throw error;
  }
}
