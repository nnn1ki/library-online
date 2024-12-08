<template>
    <footer class="footer">
      <!-- Контент футера -->
      <div class="footer-content">
        <p>&copy; 2024 Your Company. All rights reserved.</p>
        <nav>
          <ul class="footer-menu">
            <li><a href="/privacy-policy">Privacy Policy</a></li>
            <li><a href="/terms-of-service">Terms of Service</a></li>
            <li><a href="/contact">Contact</a></li>
          </ul>
        </nav>
      </div>
  
      <!-- Место для дополнительных компонентов -->
      <div class="footer-extra">
        <slot></slot> <!-- Слот для добавления пользовательских компонентов -->
      </div>
    </footer>
  </template>
  
  <script>
  export default {
    name: 'Footer',
  }
  </script>
  
  <style scoped>
  /* Основные стили для футера */
  .footer {
    background-color: #333;
    color: #fff;
    padding: 16px 32px;
    width: 100%;
    text-align: center;
  }
  
  .footer-content {
    display: flex;
    justify-content: space-between;
    margin-bottom: 16px;
  }
  
  .footer-menu {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    gap: 16px;
  }
  
  .footer-menu li a {
    color: #fff;
    text-decoration: none;
    transition: color 0.3s;
  }
  
  .footer-menu li a:hover {
    color: #00bcd4;
  }
  
  .footer-extra {
    display: flex;
    justify-content: center;
    width: 100%;
    padding: 10px 0;
  }
  
  .footer p {
    margin: 0;
    font-size: 14px;
  }
  </style>