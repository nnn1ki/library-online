<template>
    <!-- <button :class="['btn', `btn-${type}`, className]" :style="customStyle" @click="handleClick"> -->
    <button>
      <slot></slot> <!-- Используем слот для текста внутри кнопки -->
    </button>
  </template>
  
  <script>
  export default {
    name: 'Button',
    props: {
      type: {
        type: String,
        default: 'primary',
      },
      className: {
        type: String,
        default: '',
      },
      customStyle: {
        type: Object,
        default: () => ({}),
      },
      onClick: {
        type: Function,
        default: () => {},
      },
    },
    methods: {
      handleClick(event) {
        this.onClick(event); // Вызываем переданное событие
      },
    },
  };
  </script>
  
  <style scoped>
  .btn {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
  }
  
  .btn-primary {
    background-color: #007bff;
    color: white;
  }
  
  .btn-secondary {
    background-color: #6c757d;
    color: white;
  }
  
  .btn-danger {
    background-color: #dc3545;
    color: white;
  }
  </style>