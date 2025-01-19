import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { watch } from "vue";

export function useAuthentication(hook: (isAuthenticated: boolean) => void) {
  const authStore = useAuthStore();
  const { refresh } = storeToRefs(authStore);

  watch(
    refresh,
    () => {
      hook(refresh.value !== undefined);
    },
    {
      immediate: true,
    },
  );
}