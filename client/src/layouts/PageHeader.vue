<template>
  <header>
    <nav class="container">
      <div class="flex flex-row items-center">
        <RouterLink to="/" class="logo-link" active-class="active">
          <span>НТБ ИРНИТУ</span>
          <!-- <img :src="Logo" alt="НТБ ИРНИТУ" class="logo"/> -->
        </RouterLink>

        <div class="nav-links">
          <RouterLink
            v-for="[index, link] in links.entries()"
            v-bind:key="index"
            :to="link.to"
            class="nav-link"
            active-class="active"
            >{{ link.name }}</RouterLink
          >

          <!-- TODO: свитчер -->
          <div>
            <StyledButton style="margin-right: 2px" @click="themeStore.setTheme('light')"
              >Светлая</StyledButton
            >
            <StyledButton style="margin-right: 2px" @click="themeStore.setTheme('system')"
              >Системная</StyledButton
            >
            <StyledButton @click="themeStore.setTheme('dark')">Темная</StyledButton>
          </div>
        </div>
      </div>

      <button class="expand-button" @click="mobileMenuOpen = !mobileMenuOpen">
        <Bars3Icon class="expand-icon nav-link" aria-hidden="true" />
      </button>
    </nav>
    <div class="mobile-menu" :class="{ open: mobileMenuOpen }">
      <RouterLink
        v-for="[index, link] in links.entries()"
        v-bind:key="index"
        :to="link.to"
        class="nav-link"
        active-class="active"
        >{{ link.name }}</RouterLink
      >

      <div>
        <button @click="themeStore.setTheme('light')">Светлая</button>
        <button @click="themeStore.setTheme('system')">Системная</button>
        <button @click="themeStore.setTheme('dark')">Темная</button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
// import Logo from "@/assets/ntb-logo.png";
import { useAuthStore } from "@/stores/auth";
import { useThemeStore } from "@/stores/theme";
import { storeToRefs } from "pinia";
import { computed, ref } from "vue";
import { Bars3Icon } from "@heroicons/vue/24/outline";
import StyledButton from "@/components/StyledButton.vue";

const authStore = useAuthStore();
const { isAuthenticated } = storeToRefs(authStore);

const themeStore = useThemeStore();

const links = computed(() =>
  [
    {
      to: "/profile",
      name: isAuthenticated.value ? "Профиль" : "Вход",
    },
    {
      to: "/basket",
      name: "Корзина",
    },
    {
      to: "/orders",
      name: "Заказы",
      hide: !isAuthenticated.value,
    },
    {
      to: "/note",
      name: "О проекте",
    },
  ].filter((x) => !x.hide)
);

const mobileMenuOpen = ref(false);
</script>

<style scoped lang="scss">
@use "@/styles/breakpoints.scss" as *;

header {
  padding-top: 1.25rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid;
  border-color: var(--color-background-100);

  padding-left: 1rem;
  padding-right: 1rem;
  @include media-lg {
    padding-left: 0;
    padding-right: 0;
  }
}

nav {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

.logo-link {
  margin-right: 4rem;
  font-weight: 700;
  text-decoration: none;
  color: var(--color-primary-700);

  &:hover {
    color: var(--color-primary-600);
  }

  &.active {
    color: var(--color-primary-600);
  }
}

// .logo {
//   height: 40px;
// }

.nav-links {
  flex-direction: row;
  align-items: center;
  column-gap: 1rem;

  display: none;
  @include media-lg {
    display: flex;
  }
}

.nav-link {
  text-decoration: none;
  font-weight: 600;
  color: var(--color-text-700);

  &:hover {
    color: var(--color-text-500);
  }

  &.active {
    color: var(--color-text-500);
  }
}

.expand-button {
  background: none;
  border: none;
  cursor: pointer;

  display: block;
  @include media-lg {
    display: none;
  }
}

.expand-icon {
  width: 1.5rem;
  height: 1.5rem;
}

.mobile-menu {
  flex-direction: column;
  row-gap: 0.5rem;
  padding-top: 1rem;

  display: none;
  &.open {
    display: flex;
  }

  @include media-lg {
    &.open {
      display: none;
    }
  }
}
</style>
