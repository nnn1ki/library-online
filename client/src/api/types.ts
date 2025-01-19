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
