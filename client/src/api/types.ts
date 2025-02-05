export const groups = {
  Reader: "Читатель",
  Librarian: "Библиотекарь",
} as const;
export type Group = keyof typeof groups;

export type ProfileInfo = {
  username: string;
  first_name: string;
  last_name: string;
  groups: Group[];
};

export type Library = {
  id: number;
  description: string;
  address: string;
};

export type Scenario = {
  prefix: string;
  description: string | null;
};

export type BookLink = {
  url: string;
  description: string | null;
};

export type Book = {
  id: string;
  library: number;
  description: string;
  year: number;
  copies: number;
  can_be_ordered: boolean;
  links: BookLink[];
  author: string[];
  collective: string[];
  title: string[];
  isbn: string[];
  language: string[];
  country: string[];
  city: string[];
  publisher: string[];
  subject: string[];
  keyword: string[];
  cover: string | null;
  brief: string | null;
  created: string | null;
};

export const orderStatuses = {
  new: "Новый",
  processing: "Собирается",
  ready: "Готов к выдаче",
  done: "Выполнен",
  cancelled: "Отменен",
  error: "Ошибка",
  archived: "Заархивирован",
} as const;
export type OrderStatusEnum = keyof typeof orderStatuses;

export type OrderStatus = {
  status: OrderStatusEnum;
  date: string;
  description: string;
};

export const orderBookStatuses = {
  ordered: "Заказана",
  handed: "Выдана",
  returned: "Возвращена",
  cancelled: "Заказ отменен",
} as const;
export type OrderBookStatus = keyof typeof orderBookStatuses;

export type OrderBook = {
  id: number;
  book: Book;
  status: OrderBookStatus;
};

export type Order = {
  id: number;
  books: OrderBook[];
  statuses: OrderStatus[];
  library: Library;
};

export type BorrowedBook = {
  id: number;
  book: Book;
  order: number;
};
