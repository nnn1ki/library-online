import { addBasketBook, deleteBasketBook, getBasketBooks, replaceBasketBooks } from "@/api/basket";
import type { Book } from "@/api/types";
import { useAuthentication } from "@/composables/auth";
import { useLocalStorage } from "@vueuse/core";
import { defineStore, storeToRefs } from "pinia";
import { ref } from "vue";
import { useToast } from "vue-toastification";
import { useAuthStore } from "./auth";

export const useBasketStore = defineStore("basket", () => {
  const toast = useToast();
  const authStore = useAuthStore();

  const { isAuthenticated } = storeToRefs(authStore);
  const localBooks = useLocalStorage<Book[]>("basketBooks", []);
  const books = ref<Book[]>([]);;

  async function updateBooks() {
    if (isAuthenticated.value) {
      books.value = await getBasketBooks();
    } else {
      books.value = localBooks.value;
    }
  }

  async function addBook(book: Book) {
    if (isAuthenticated.value) {
      await addBasketBook(book.id);
    } else {
      if (localBooks.value.filter((b) => b.id === book.id).length === 0) { 
        localBooks.value.push(book);
      }
    }

    toast.success(book.description + " добавлен(a) в корзину");
    updateBooks();
  }

  async function removeBook(book: Book) {
    if (isAuthenticated.value) {
      await deleteBasketBook(book.id);
    } else {
      localBooks.value = localBooks.value.filter((b) => b.id !== book.id);
    }
    updateBooks();
  }

  async function clearBooks() {
    if (isAuthenticated.value) {
      await replaceBasketBooks([])
    } else {
      localBooks.value = [];
    }
    updateBooks();
  }

  useAuthentication(() => {
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
