export const groups = {
  Reader: "Читатель",
  Librarian: "Библиотекарь",
} as const;
export type Group = keyof typeof groups;

export type ProfileInfo = {
  username: string;
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
  description: string;
};

export type Book = {
  id: string;
  description: string;
  year: number;
  cover: string | null;
  links: BookLink[];
  library: number;
  copies: number;
  can_be_ordered: boolean;
};

export const statuses = {
  new: "Новый",
  processing: "Собирается",
  ready: "Готов к выдаче",
  done: "Выполнен",
  cancelled: "Отменен",
  error: "Ошибка",
  archived: "Заархивирован",
} as const;
export type Status = keyof typeof statuses;

export type OrderStatus = {
  status: Status;
  date: string;
  description: string;
};

export type OrderBook = {
  id: number;
  book: Book;
  handed: boolean;
  returned: boolean;
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
