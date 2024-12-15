<script setup lang="ts">
</script>

<template>
  <div class="app">    
    <Header></Header>

    <main>
      <div>
        <router-view />
      </div>
    </main>

    
  </div>
  <Footer/>
</template>


<script>
  import Button from './components/Button.vue';
  import Header from './components/Header.vue';
  import Footer from './components/Footer.vue';



  export default {
    name: 'App', 
    components: {
      Button, //регистрируем компонент
      Header,
      Footer,
    },
    methods: {
      // handleClick() {
      //   console.log("Кнопка нажата!")
      // }
    }

  }

</script>
  <style>
  /* Корневой контейнер для всей страницы */
  .app {
    display: flex;
    flex-direction: column;
    min-height: 100vh; /* Обеспечивает, чтобы футер всегда был внизу страницы */
  }

  main {
    flex: 1; /* Это заставляет основной контент занять все доступное пространство */
    padding: 20px;
  }


</style>