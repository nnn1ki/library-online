import axios from "axios";
import type { ProfileInfo } from "@/api/types";

export async function profileInfo(): Promise<ProfileInfo> {
    try{
      const { data } = await axios.get("/api/profile/self-info/");
      console.log("/api/profile/self-info/", data);
      return data;
    }catch (error) {
      console.error("Ошибка при получении информации о профиле", error);
      throw error;
    }
}
