<template>
  <div class="instructions-page container">
    <h1>Как использовать наш сервис</h1>

    <!-- Шаги инструкции -->
    <div class="row row-cols-1 row-cols-md-2 g-4">
      <div class="col" v-for="(step, index) in steps" :key="index">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h2 class="card-title text-primary">{{ step.title }}</h2>
            <p class="card-text">{{ step.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Важная информация -->
    <div class="important-info bg-light p-4 mt-5 rounded border">
      <h3 class="text-center">Свяжитесь с нами</h3>
      <p class="text-center">
        Если у вас возникли вопросы, пожалуйста, свяжитесь с нашей службой поддержки через email:
        <a href="mailto:support@yourservice.com">domrachev@conferoom.site</a>.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
const steps = [
  {
    title: "Шаг 1: Регистрация",
    description:
      "Для начала необходимо зарегистрироваться на сайте. Перейдите на страницу 'Регистрация', введите свои данные и подтвердите регистрацию через email.",
  },
  {
    title: "Шаг 2: Выбор книг",
    description:
      "Вы можете выбрать книги через каталог, который находится на главной странице. Используйте фильтры поиска, чтобы ускорить процесс выбора нужных книг.",
  },
  {
    title: "Шаг 3: Добавление в корзину",
    description:
      "Нажмите на кнопку 'Добавить в корзину' рядом с книгой, чтобы добавить её в вашу корзину. Вы можете выбрать несколько книг для оформления заказа.",
  },
  {
    title: "Шаг 4: Оформление заказа",
    description:
      "Перейдите в корзину и нажмите 'Оформить заказ'. Введите ваш email для получения уведомлений о статусе заказа, и подтвердите ваш выбор.",
  },
  {
    title: "Шаг 5: Получение книг",
    description:
      "После оформления заказа, ваши книги будут готовы в течение 1-2 дней. Мы уведомим вас, как только заказ будет готов.",
  },
];
</script>

<style scoped lang="scss">
.instructions-page {
  padding-top: 20px;
}

h1 {
  text-align: center;
}

.card-title {
  font-size: 1.5rem;
}

.card-text {
  font-size: 1rem;
  color: #555;
}

.important-info {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #e7e7e7;
}

.important-info a {
  color: #007bff;
  text-decoration: none;
}

.important-info a:hover {
  text-decoration: underline;
}
</style>
