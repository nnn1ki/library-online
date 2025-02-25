import { useLocalStorage } from "@vueuse/core";
import { defineStore } from "pinia";
import { onMounted } from "vue";

export const useThemeStore = defineStore("theme", () => {
  type Theme = "system" | "light" | "dark";
  const theme = useLocalStorage<Theme>("theme", "system");

  function updateThemeAttribute() {
    const root = document.documentElement;
    if (theme.value == "system") {
      delete root.dataset.theme;
    } else {
      root.dataset.theme = theme.value;
    }
  }

  function setTheme(newTheme: Theme) {
    theme.value = newTheme;
    updateThemeAttribute();
  }

  onMounted(() => {
    updateThemeAttribute();
  });

  return {
    theme,
    setTheme,
  };
});
