<template>
    <div>
      <!-- Контент, который не будет печататься -->
      
      <div id="printMe">
        <!-- Контент для печати -->
        <h1>Печатаемый заголовок</h1>
        <p>Этот контент будет напечатан.</p>
      </div>
      
      <button @click="print">Печать</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      print() {
        this.$htmlToPaper('printMe');
      }
    }
  }
  </script>