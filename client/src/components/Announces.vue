<template>
    <div class="announces-container">
      <div v-if="loading" class="loading">Загрузка...</div>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="announces && announces.length > 0" class="cards">
        <div v-for="(announce, index) in announces" :key="index" class="card">
          <img
            :src="`${baseUrl}${announce.picture}`"
            :alt="`Обложка ${index + 1}`"
            class="card-img"
          />
          <a :href="`${baseUrl}${announce.link}`" target="_blank" class="card-link">
            Подробнее
          </a>
        </div>
      </div>
    </div>
</template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { announcesItems } from '../api/announces';
  
  const announces = ref([]);
  const loading = ref(true);
  const error = ref(null);
  
  const baseUrl = 'https://library.istu.edu';
  
  onMounted(async () => {
    try {
      const data = await announcesItems();
      announces.value = Object.values(data); // Преобразуем объект в массив
      console.log('data', data); 
    } catch (err) {
      error.value = 'Ошибка загрузки данных';
      console.error(err);
    } finally {
      loading.value = false;
    }
  });
  </script>
  
  <style scoped>
  .announces-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
  }
  
  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
  }
  
  .card {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 10px;
    background-color: #fff;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .card-img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin-bottom: 10px;
  }
  
  .card-link {
    color: #007bff;
    text-decoration: none;
    font-weight: bold;
  }
  
  .card-link:hover {
    text-decoration: underline;
  }
  
  .loading {
    font-size: 18px;
    color: #666;
  }
  
  .error {
    font-size: 18px;
    color: red;
  }
  </style>
  