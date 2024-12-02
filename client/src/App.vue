<script setup lang="ts">
</script>

<template>
  <div>
    <header>
      <nav class="navbar sticky-top navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid navbar-mine">
          <a class="navbar-brand" href="/">ИрНИТУ</a>
          <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNavDropdown"
            aria-controls="navbarNavDropdown"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNavDropdown">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <router-link class="nav-link" to="/basket">
                  <button class="btn btn-outline-info" type="button">
                    <i class="bi bi-cart3"></i>
                  </button>
                </router-link>
              </li>
              <li>
                <router-link class="nav-link" to="/users">
                  <button class="btn btn-outline-info" type="button">
                    <i class="bi bi-person-fill"></i>
                  </button>
                </router-link>
              </li>
              <li>
                <router-link class="nav-link" to="/note">
                  <button class="btn btn-outline-info" type="button">
                    <i class="bi bi-journal-bookmark-fill"></i>
                  </button>
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>

    <main>
      <div>
        <router-view />
      </div>
    </main>

    <footer>
      <div>
        <p>
          ИРНИТУ | Координаты | Обратная связь | Электронный каталог | Режим
          работы | Правила пользования
        </p>
        <p>
          © ИРНИТУ, 2024. Все права защищены. Перепечатка возможна только с
          письменного разрешения НТБ ИРНИТУ.
        </p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.nav-item {
  align-content: center;
}

body {
  background: #ededed;
  min-height: 100vh;
  position: relative;
}

header {
  background: #ededed;
}

main {
  background: #fff;
}

footer {
  background: #ededed;
  position: fixed;
  bottom: 0;
  width: 100%;
  text-align: center;
}
</style>