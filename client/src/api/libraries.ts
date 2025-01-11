import axios from "axios";
import type { Library } from "./types";

const options = {method: 'GET', url: '/api/library/'};

export async function librariesList(): Promise<Library[]> {
    try{
      const { data } = await axios.request(options);
      console.log("/api/library/", data);
      return data;
    }catch (error) {
      console.error("Ошибка при получении списка библиотек", error);
      throw error;
    }
}

