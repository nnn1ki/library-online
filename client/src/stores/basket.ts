import type { Book } from "@/api/types";
import { useLocalStorage } from "@vueuse/core";
import { defineStore } from "pinia";
import { onMounted } from "vue";
import { useToast } from "vue-toastification";

// TODO: useAuthStore. Если авторизованы, используем api
export const useBasketStore = defineStore("basket", () => {
  const toast = useToast();
  const books = useLocalStorage<Book[]>("basketBooks", []);

  async function updateBooks() {}

  async function addBook(book: Book) {
    if (books.value.filter((b) => b.id === book.id).length === 0) { 
      books.value.push(book);
    }
    toast.success(book.description + " добавлен(a) в корзину");
    updateBooks();
  }

  async function removeBook(book: Book) {
    books.value = books.value.filter((b) => b.id !== book.id);
    updateBooks();
  }

  async function clearBooks() {
    books.value = [];
    updateBooks();
  }

  onMounted(() => {
    updateBooks();
  });

  return {
    books,
    updateBooks,
    addBook,
    removeBook,
    clearBooks
  }
});
