import axios from "axios";
import type { Book } from "./types";

const options = {method: 'GET', url: '/api/book/announce/'};

export async function announcesList(): Promise<Book[]> {
    try{
      const { data } = await axios.request(options);
      console.log("/api/book/announce/", data);
      return data;
    }catch (error) {
      console.error("Ошибка при поиске новинок", error);
      throw error;
    }
}