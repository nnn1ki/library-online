<template>
  <header class="header bg-white shadow-sm py-3">
    <div class="container d-flex justify-content-between align-items-center">
      <!-- Логотип -->
      <div class="header-left d-flex align-items-center">
        <img :src="logoSrc" alt="Logo" class="logo me-3" />

        <!-- Навигационное меню -->
        <nav>
          <ul class="nav mb-0">
            <li class="nav-item">
              <router-link to="/" class="nav-link" active-class="active">Главная страница</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/users" class="nav-link" active-class="active">Вход</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/basket" class="nav-link" active-class="active">Корзина</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/note" class="nav-link" active-class="active">О проекте</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/orders" class="nav-link" active-class="active">Заказы</router-link>
            </li>
          </ul>
        </nav>
      </div>

      <!-- Дополнительные компоненты (слот) -->
      <div class="header-right d-flex align-items-center">
        <slot></slot> <!-- Слот для добавления пользовательских компонентов -->
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  props: {
    logoSrc: {
      type: String,
      default: '../../public/favicon.ico',
    },
  },
}
</script>

<style scoped>
/* Основные стили для header */
.header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo {
  height: 40px;
}

.nav .nav-link {
  font-size: 16px;
  transition: color 0.3s;
}

.nav .nav-link:hover {
  color: #00bcd4; /* Цвет активной ссылки */
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}
</style>
