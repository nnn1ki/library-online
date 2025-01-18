import type { Book } from "@/api/types";
import { useLocalStorage } from "@vueuse/core";
import { defineStore } from "pinia";

// TODO: useAuthStore. Если авторизованы, используем api
export const useBasketStore = defineStore("basket", () => {
  const books = useLocalStorage<Book[]>("basketBooks", []);

  async function loadBooks(): Promise<Book[]> {
    return books.value;
  }

  async function addBook(book: Book) {
    if (books.value.filter((b) => b.id === book.id).length === 0) { 
      books.value.push(book);
    }
  }

  async function removeBook(book: Book) {
    books.value = books.value.filter((b) => b.id !== book.id);
  }

  async function clearBooks() {
    books.value = [];
  }

  return {
    loadBooks,
    addBook,
    removeBook,
    clearBooks
  }
});
