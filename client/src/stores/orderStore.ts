import { useRouter } from "vue-router";
import { useLocalStorage } from "@vueuse/core";
import { defineStore, storeToRefs } from "pinia";
import { ref, nextTick } from "vue";
import { useToast } from "vue-toastification";

import { ordersList, createOrder, deleteOrder } from "@/api/order";
import { getBook } from "@/api/books";
import { deleteBasketBook } from "@/api/basket";
import type { Book, Order, BorrowedBook, OrderStatusEnum } from "@/api/types";

import { useAuthStore } from "./auth";
import { useBasketStore } from "@/stores/basket";

export const useOrderStore = defineStore("orderStore", () => {
  const toast = useToast();
  const authStore = useAuthStore();
  const { isAuthenticated } = storeToRefs(authStore);
  const basketStore = useBasketStore();

  const router = useRouter();
  const selectedBooks = useLocalStorage<Book[]>("selectedBooksToOrder", []);
  const selectedBorrowedBooks = ref<number[]>([]);
  const borrowedBooks = ref<BorrowedBook[]>([]);
  const userOrders = ref<Order[]>([]);
  const allowedStatusesToCountOrderedBooks: OrderStatusEnum[] = [
    "new",
    "processing",
    "ready",
    "done",
  ];

  async function handleCreateOrder() {
    if (!isAuthenticated.value) {
      toast.error("Необходимо зарегистрироваться");
      return;
    }

    toast.info("Проверяем все ли книги, можно заказать");
    userOrders.value = await ordersList();
    const canBeOrdered = await checkCanBeOrdered();
    if (!canBeOrdered) return;

    toast.info("Проверяем сколько у вас книг на руках и в заказах");
    const isValid = await validateOrder();

    if (!isValid) {
      toast.error(
        "У вас много заказанных книг и книг на руках, больше заказывать нельзя. Нужно вернуть часть книг в библиотеку."
      );
      return;
    }

    const bookIds = selectedBooks.value.map((book) => book.id);

    try {
      await createOrder(selectedBooks.value[0].library, bookIds, selectedBorrowedBooks.value);

      await clearBasket(bookIds);
      selectedBooks.value = [];
      await basketStore.updateBooks();
      toast.success("Заказ принят");
      await nextTick();
    } catch {
      toast.error("Что то не так");
    }
    router.push({ name: "Home" });
  }

  async function handleDeleteOrder(orderId: number) {
    try {
      await deleteOrder(orderId);
      toast.info("Ваш заказ отменен");
    } catch {
      toast.error("Что то пошло не так...");
    }
  }

  async function validateOrder(): Promise<boolean> {
    const librarySet = new Set(selectedBooks.value.map((book) => book.library));
    const orderedBooksCount = booksOrdered();
    const totalItems =
      borrowedBooks.value.length -
      selectedBorrowedBooks.value.length +
      selectedBooks.value.length +
      orderedBooksCount;
    return totalItems > 0 && totalItems <= 7 && librarySet.size === 1;
  }

  // проверка сколько книг в заказах
  function booksOrdered(): number {
    const countOfBooksPreviousOrders = userOrders.value.reduce((total, order) => {
      const lastStatus = order.statuses[order.statuses.length - 1];
      if (lastStatus && allowedStatusesToCountOrderedBooks.includes(lastStatus.status)) {
        const validBooks = order.books.filter((book) => book.status === "ordered");

        return total + validBooks.length;
      }
      return total;
    }, 0);
    return countOfBooksPreviousOrders;
  }

  async function checkCanBeOrdered(): Promise<boolean> {
    let allCanBeOrdered = true;
    for (const book of selectedBooks.value) {
      try {
        const fetchedBook = await getBook(book.id);
        if (!fetchedBook.can_be_ordered || bookInOrders(book.id)) {
          allCanBeOrdered = false;
          toast.error(`Нельзя заказать книгу "${book.title}",\nона будет удалена из заказа`);
          selectedBooks.value = selectedBooks.value.filter((b) => b.id !== book.id);
        }
      } catch {
        toast.error(`Ошибка при проверке книги "${book.title}"`);

        allCanBeOrdered = false;
      }
    }
    return allCanBeOrdered;
  }

  function bookInOrders(targetBookId: string): boolean {
    return userOrders.value.some((order) => {
      const lastStatus = order.statuses[order.statuses.length - 1];
      if (lastStatus && allowedStatusesToCountOrderedBooks.includes(lastStatus.status)) {
        order.books.some((orderBook) => orderBook.book.id === targetBookId);
      }
    });
  }

  async function clearBasket(selectedIds: string[]) {
    for (const id of selectedIds) {
      console.log(id);
      await deleteBasketBook(id).catch(() => console.log("Ошибка при удалении элемента корзины"));
    }
  }

  return {
    handleCreateOrder,
    selectedBooks,
    selectedBorrowedBooks,
    borrowedBooks,
    handleDeleteOrder,
  };
});
