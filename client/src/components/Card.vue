<template>
  <div class="card shadow-sm border-0">
    <!-- Картинка -->
    <img :src="imageUrl || 'https://via.placeholder.com/250x200'" class="card-img-top" :alt="title" />

    <div class="card-body">
      <!-- Заголовок книги и автор -->
      <h5 class="card-title">{{ title }}</h5>
      <h6 class="card-subtitle text-muted">{{ author }}</h6>

      <div class="d-flex justify-content-between align-items-center">
        <!-- Кнопка добавления в корзину -->
        <button 
          class="btn btn-info btn-sm" 
          type="button" 
          @click="handleAddToBasket"
          :disabled="isInBasket"
        >
          <i class="bi bi-cart3"></i> В Корзину
        </button>

        <!-- Кнопка для подробного описания -->
        <button 
          class="btn btn-primary btn-sm mt-2" 
          type="button" 
          @click="openDetailsModal"
        >Подробнее</button>
      </div>
    </div>
  </div>

  <!-- модальное окно книги -->
  <div class="modal" tabindex="-1" :class="{ show: isModalVisible }">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Подробнее о книге</h5>
          <button type="button" class="btn-close" @click="closeDetailsModal"></button>
        </div>
        <div class="modal-body d-flex">
          <!-- Левая часть: картинка -->
          <div class="book-image">
            <img :src="selectedBook?.imageUrl || 'https://via.placeholder.com/250x200'" alt="Книга" />
          </div>
          <!-- Правая часть: информация -->
          <div class="book-details ms-3">
            <h5>{{ selectedBook?.title }}</h5>
            <h6 class="text-muted">Автор: {{ selectedBook?.author }}</h6>
            <p>{{ selectedBook?.description }}</p>
            <button 
              class="btn btn-info btn-sm" 
              type="button" 
              @click="handleAddToBasket"
              :disabled="isInBasket"
            >
              <i class="bi bi-cart3"></i> В Корзину
            </button>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeDetailsModal">Закрыть</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { useToast } from 'vue-toastification'; //хук для уведомлений
  import { ref } from 'vue';
  const toast = useToast();

  const props = defineProps({
    title: {
      type: String,
      required: true
    },
    author: {
      type: String,
      required: true
    },
    imageUrl: {
      type: String,
      default: 'https://via.placeholder.com/250x200'
    },
    quantity: {
      type: Number,
      required: true
    },
    addToBasket: {
      type: Function,
      required: true
    },
    isInBasket: {
      type: Boolean,
      required: true
    }
  })

  // Определение переменных для модального окна
  const isModalVisible = ref(false);  // Видимость модального окна
  const selectedBook = ref(null); // Книга для отображения в модальном окне

  // Открытие модального окна
  const openDetailsModal = () => {
    console.log('Opening modal for:', props.title);
    selectedBook.value = {
      title: props.title,
      author: props.author,
      description: 'огромная сага, с равной глубиной рассказывающая о событиях различного масштаба: от частной жизни нескольких семей и конкретных сражений 1812 года до движения народов и истории вообще.'  // Вы можете добавить описание для каждой книги
    };
    isModalVisible.value = true;
  };

  // Закрытие модального окна
  const closeDetailsModal = () => {
    isModalVisible.value = false;
    selectedBook.value = null;
  };

  const handleAddToBasket = () => {
    toast.success(props.title + ' добавлен(a) в корзину');
    props.addToBasket({ title: props.title, author: props.author, imageUrl: props.imageUrl, quantity: props.quantity });
  }
</script>

<style scoped>
.modal {
  display: block;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Полупрозрачный фон */
  z-index: 1050; /* Убедитесь, что модальное окно поверх всего */
  visibility: hidden; /* Скрыто по умолчанию */
}

.modal.show {
  visibility: visible;
}

.modal-dialog {
  position: relative;
  margin: 10% auto;
  max-width: 1000px;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
}

.modal-header .btn-close {
  background: none;
  border: none;
}

.modal-footer {
  text-align: right;
}


.card {
  width: 100%;
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
