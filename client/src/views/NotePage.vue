<template>
  <div class="instructions-page container">
    <h1 class="text-center my-4">Как использовать наш сервис</h1>

    <!-- Шаги инструкции -->
    <div class="steps">
      <div class="step-card">
        <h2>Шаг 1: Регистрация</h2>
        <p>Для начала необходимо зарегистрироваться на сайте. Перейдите на страницу <a href="/users">Регистрация</a>, введите свои данные и подтвердите регистрацию через email.</p>
      </div>

      <div class="step-card">
        <h2>Шаг 2: Выбор книг</h2>
        <p>Вы можете выбрать книги через каталог, который находится на главной странице. Используйте фильтры поиска, чтобы ускорить процесс выбора нужных книг.</p>
      </div>

      <div class="step-card">
        <h2>Шаг 3: Добавление в корзину</h2>
        <p>Нажмите на кнопку "Добавить в корзину" рядом с книгой, чтобы добавить её в вашу корзину. Вы можете выбрать несколько книг для оформления заказа.</p>
      </div>

      <div class="step-card">
        <h2>Шаг 4: Оформление заказа</h2>
        <p>Перейдите в корзину и нажмите "Оформить заказ". Введите ваш email для получения уведомлений о статусе заказа, и подтвердите ваш выбор.</p>
      </div>

      <div class="step-card">
        <h2>Шаг 5: Получение книг</h2>
        <p>После оформления заказа, ваши книги будут готовы в течение 1-2 дней. Мы уведомим вас, как только заказ будет готов.</p>
      </div>
    </div>

    <!-- Важная информация -->
    <div class="important-info mt-5">
      <h3 class="text-center">Свяжитесь с нами</h3>
      <p>Если у вас возникли вопросы, пожалуйста, свяжитесь с нашей службой поддержки через email: <a href="mailto:support@yourservice.com">support@yourservice.com</a>.</p>
    </div>
  </div>
</template>

<style scoped>
.instructions-page {
  padding: 20px;
}

h1 {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

.steps {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 40px;
}

.step-card {
  background-color: #ffffff;
  border: 1px solid #e7e7e7;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.step-card:hover {
  transform: scale(1.05);
}

.step-card h2 {
  font-size: 1.5rem;
  color: #007bff;
}

.step-card p {
  font-size: 1rem;
  color: #555;
}

.important-info {
  margin-top: 60px;
  padding: 20px;
  background-color: #f9f9f9;
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
