import axios from "axios";
import type { Scenario } from "./types";

const options = {method: 'GET', url: '/api/scenario/'};

export async function scenariosList(): Promise<Scenario[]> {
    try{
      const { data } = await axios.request(options);
      console.log("/api/scenario/", data);
      return data;
    }catch (error) {
      console.error("Ошибка при получении списка сценариев поиска", error);
      throw error;
    }
}

