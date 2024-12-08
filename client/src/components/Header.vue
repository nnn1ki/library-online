<template>
    <header class="header">
        <div class="header-left">
            <img :src="logoSrc" alt="Logo" class="logo" />
        
            <nav class="nav">
                <!-- работает без перезагрузки страницы -->
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
                    <router-link to="/orders" class="nav-link" active-class="active">OrderPage</router-link> 
                </li>

            </nav>
      
        </div>
  
      <!-- Место для дополнительных компонентов -->
      <div class="header-right">
        <slot></slot> <!-- Слот для добавления пользовательских компонентов -->
      </div>
    </header>
  </template>
  


  <!-- настраивать кнопки из другого места -->
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
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 32px;
    background-color: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .header-left {
    display: flex;
    align-items: center;
  }
  
  .logo {
    height: 40px;
    margin-right: 24px;
  }
  
  .nav .menu {
    list-style: none;
    display: flex;
    margin: 0;
    padding: 0;
  }
  
  .nav .menu li {
    margin-right: 16px;
  }
  
  .nav .menu button {
    background: none;
    border: none;
    padding: 8px 16px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
  }
  
  .nav .menu button:hover {
    background-color: #f0f0f0;
  }
  
  .header-right {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  </style>
  