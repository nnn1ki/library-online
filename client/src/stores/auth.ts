import { useLocalStorage } from "@vueuse/core";
import { defineStore } from "pinia";
import { jwtDecode } from "jwt-decode";
import axios from "axios";

export const useAuthStore = defineStore("auth", () => {
  type Token = string | undefined;
  type Tokens = {
    access: string;
    refresh: string;
  };

  function isTokenValid(token: Token): boolean {
    if (token === undefined) {
      return false;
    } else {
      const decoded = jwtDecode(token);
      return Date.now() < decoded.exp! * 1000;
    }
  }

  const access = useLocalStorage<Token>("accessToken", undefined);
  const refresh = useLocalStorage<Token>("refreshToken", undefined);

  async function refreshTokens() {
    const simpleAxios = axios.create();
    const { data } = await simpleAxios.post<Tokens>("/api/auth/refresh/", {
      refresh: refresh.value,
    });

    access.value = data.access;
    refresh.value = data.refresh;
  }

  async function updateTokens(): Promise<boolean> {
    if (!isTokenValid(refresh.value)) {
      refresh.value = undefined;
      access.value = undefined;
      return false;
    } else if (!isTokenValid(access.value)) {
      await refreshTokens();
    }
    return true;
  }

  // TODO: полноценная авторизация
  async function login(username: string, password: string): Promise<boolean> {
    try {
      const simpleAxios = axios.create();
      const { data } = await simpleAxios.post<Tokens>("/api/auth/login/", {
        username: username,
        password: password,
      });
      refresh.value = data.refresh;
      access.value = data.access;
      return true;
    } catch (_) {
      return false;
    }
  }

  async function logout() {
    const refreshCopy = refresh.value;
    refresh.value = undefined;
    access.value = undefined;

    const simpleAxios = axios.create();
    await simpleAxios.post("/api/auth/logout/", {
      refresh: refreshCopy,
    });
  }

  // TODO: возвращать currentUser
  return {
    access,
    refresh,
    updateTokens,
    login,
    logout,
  };
});
