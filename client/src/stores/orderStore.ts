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

interface ModalStep {
  title: string;
  error: string | null;
}

interface ModalState {
  isOpen: boolean;
  currentStep: number;
  steps: ModalStep[];
  isSuccess: boolean;
  isError: boolean;
  orderId: string | null;
  errorMessage: string | null;
}

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
  const countOfBookInOrder = 5;
  const countOfBookPerPerson = 15;
  const allowedStatusesToCountOrderedBooks: OrderStatusEnum[] = [
    "new",
    "processing",
    "ready",
    "done",
  ];

  const modalState = ref<ModalState>({
    isOpen: false,
    currentStep: 0,
    steps: [
      { title: "Проверка авторизации", error: null },
      { title: "Проверка количества книг", error: null },
      { title: "Проверка возвращаемых книг", error: null },
      { title: "Проверка доступности книг", error: null },
      { title: "Проверка лимитов", error: null },
      { title: "Создание заказа", error: null },
    ],
    isSuccess: false,
    isError: false,
    orderId: null,
    errorMessage: null,
  });


  async function handleCreateOrder() {
    resetModalState();
    modalState.value.isOpen = true;

    try {
      modalState.value.currentStep = 0;
      if (!isAuthenticated.value) {
        modalState.value.steps[0].error = "Требуется авторизация";
        modalState.value.isError = true;
        modalState.value.errorMessage = "Необходимо зарегистрироваться";
        toast.error("Необходимо зарегистрироваться");
        return;
      }

      modalState.value.currentStep = 1;
      if (selectedBooks.value.length > countOfBookInOrder) {
        modalState.value.steps[1].error = `Максимум ${countOfBookInOrder} книг`;
        modalState.value.isError = true;
        modalState.value.errorMessage = "В заказе максимум 5 книг";
        toast.error("В заказе максимум 5 книг");
        return;
      }

      modalState.value.currentStep = 2;
      if (selectedBorrowedBooks.value.length < borrowedBooks.value.length) {
        modalState.value.steps[2].error = "Не все книги отмечены";
        modalState.value.isError = true;
        modalState.value.errorMessage = "Отметьте книги, которые принесете";
        toast.error("Отметьте книги, которые принесете");
        return;
      }

      modalState.value.currentStep = 3;
      userOrders.value = await ordersList();
      const canBeOrdered = await checkCanBeOrdered();
      if (!canBeOrdered) {
        modalState.value.isError = true;
        return;
      }

      modalState.value.currentStep = 4;
      const isValid = await validateOrder();
      if (!isValid) {
        modalState.value.steps[4].error = "Превышены лимиты";
        modalState.value.isError = true;
        modalState.value.errorMessage = 
          "У вас много заказанных книг и книг на руках. Нужно вернуть часть книг.";
        toast.error("У вас много заказанных книг и книг на руках");
        return;
      }

      modalState.value.currentStep = 5;
      const bookIds = selectedBooks.value.map((book) => book.id);
      const order = await createOrder(
        selectedBooks.value[0].library, 
        bookIds, 
        selectedBorrowedBooks.value
      );

      await clearBasket(bookIds);
      clearAll();
      await basketStore.updateBooks();

      modalState.value.isSuccess = true;
      toast.success("Заказ принят");
      
      setTimeout(() => {
        modalState.value.isOpen = false;
        router.push({ name: "Home" });
      }, 3000);

    } catch (error) {
      modalState.value.steps[modalState.value.currentStep].error = "Ошибка сервера";
      modalState.value.isError = true;
      modalState.value.errorMessage = "Что-то пошло не так";
      toast.error("Что-то пошло не так");
    }
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
    return totalItems > 0 && totalItems <= countOfBookPerPerson && librarySet.size === 1;
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
    const isInOrders = userOrders.value.some((order) => {
      const lastStatus = order.statuses.at(-1);
      if (!lastStatus || !allowedStatusesToCountOrderedBooks.includes(lastStatus.status)) {
        return false;
      }
      return order.books.some((bookItem) => bookItem.book.id === targetBookId);
    });

    const isInBorrowed = borrowedBooks.value.some(
      (borrowedBook) => borrowedBook.book.id === targetBookId
    );

    return isInOrders || isInBorrowed;
  }

  async function clearBasket(selectedIds: string[]) {
    for (const id of selectedIds) {
      console.log(id);
      await deleteBasketBook(id).catch(() => console.log("Ошибка при удалении элемента корзины"));
    }
  }

  function addBook(newBook: Book) {
    selectedBooks.value.push(newBook);
  }

  function clearAll() {
    selectedBooks.value = [];
    selectedBorrowedBooks.value = [];
    borrowedBooks.value = [];
    userOrders.value = [];
  }

  function resetModalState() {
    modalState.value = {
      isOpen: false,
      currentStep: 0,
      steps: [
        { title: "Проверка авторизации", error: null },
        { title: "Проверка количества книг", error: null },
        { title: "Проверка возвращаемых книг", error: null },
        { title: "Проверка доступности книг", error: null },
        { title: "Проверка лимитов", error: null },
        { title: "Создание заказа", error: null },
      ],
      isSuccess: false,
      isError: false,
      orderId: null,
      errorMessage: null,
    };
  }

  return {
    handleCreateOrder,
    selectedBooks,
    selectedBorrowedBooks,
    borrowedBooks,
    handleDeleteOrder,
    addBook,
    modalState,
  };
});
