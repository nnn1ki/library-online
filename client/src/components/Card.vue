<template>
    <div class="card">
      <!-- Картинка -->
      <img :src="imageUrl" class="card-img-top" :alt="title" />
  
      <div class="card-body">
        <!-- Заголовок книги и автор -->
        <h5 class="card-title">{{ title }}</h5>
        <h6 class="card-subtitle text-muted">{{ author }}</h6>
  
        <!-- Кнопка добавления в корзину -->
        <button class="btn btn-info" type="button">
          <i class="bi bi-cart3"></i> Купить
        </button>
  
        <!-- Количество книг -->
        <p class="card-text">{{ quantity }} шт.</p>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    title: String,
    author: String,
    imageUrl: String,
    quantity: Number
  })
  </script>
  
  <style scoped>
  .card {
    width: 250px;
    margin-bottom: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.3s ease;
  }
  
  .card:hover {
    transform: scale(1.05);
  }
  
  .card-img-top {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }
  
  .card-body {
    padding: 16px;
  }
  
  .card-title {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 8px;
  }
  
  .card-subtitle {
    font-size: 1rem;
    color: #555;
    margin-bottom: 16px;
  }
  
  .card-text {
    font-size: 1rem;
    color: #888;
  }
  </style>