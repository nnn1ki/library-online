<template>
  <footer class="footer bg-dark text-white py-4">
    <!-- Контент футера -->
    <div class="container">
      <div class="row">
        <div class="col-12 col-md-6 mb-3 mb-md-0">
          <p>&copy; 2024 Your Company. All rights reserved.</p>
        </div>

        <!-- Ссылки на страницы -->
        <div class="col-12 col-md-6">
          <nav>
            <ul
              class="footer-menu list-unstyled d-flex justify-content-center justify-content-md-end mb-0"
            >
              <li class="ms-3">
                <a href="/privacy-policy" class="text-white text-decoration-none">Privacy Policy</a>
              </li>
              <li class="ms-3">
                <a href="/terms-of-service" class="text-white text-decoration-none"
                  >Terms of Service</a
                >
              </li>
              <li class="ms-3">
                <a href="/contact" class="text-white text-decoration-none">Contact</a>
              </li>
            </ul>
          </nav>
        </div>
      </div>

      <!-- Место для дополнительных компонентов -->
      <div class="footer-extra mt-4 text-center">
        <slot></slot>
        <!-- Слот для добавления пользовательских компонентов -->
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts"></script>

<style scoped>
.footer {
  background-color: #333;
  color: #fff;
  text-align: center;
}

.footer-menu li a {
  transition: color 0.3s;
}

.footer-menu li a:hover {
  color: #00bcd4;
}

.footer-extra {
  padding: 10px 0;
}

.footer p {
  font-size: 14px;
}
</style>
