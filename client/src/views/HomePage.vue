<script setup>
import { onBeforeMount, ref } from "vue";
import axios from "axios";
import _ from "lodash";
import { createCanvas, loadImage } from "canvas";

// пока так
const books = ref([
  { title: "Война и мир", author: "Лев Толстой", imageUrl: null, quantity: 10 },
  { title: "Преступление и наказание", author: "Федор Достоевский", imageUrl: null, quantity: 8 },
  { title: "Гарри Поттер и философский камень", author: "Джоан Роулинг", imageUrl: null, quantity: 15 },
  { title: "Сто лет одиночества", author: "Габриэль Гарсиа Маркес", imageUrl: null, quantity: 6 },
  { title: "Великий Гэтсби", author: "Фрэнсис Скотт Фицджеральд", imageUrl: null, quantity: 12 },
  { title: "Мастер и Маргарита", author: "Михаил Булгаков", imageUrl: null, quantity: 9 },
  { title: "Гордость и предубеждение", author: "Джейн Остин", imageUrl: null, quantity: 7 },
  { title: "Властелин колец", author: "Джон Рональд Руэл Толкин", imageUrl: null, quantity: 11 }
]);


//todo - вынести работу с картинками в другое место (в компонент карточки и\или поменять его работу) 
onBeforeMount(async () => {
  for (const book of books.value) {
    book.imageUrl = await generateBookImage(book.title, book.author);
  }
});

async function generateBookImage(title, author) {
  const height = 700;
  const width = height * (3 / 4);
  const canvas = createCanvas(width, height);
  const ctx = canvas.getContext("2d");

  // Заливка белым фоном
  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Рисование текста
  ctx.font = "24px Arial";
  ctx.fillStyle = "black";
  ctx.textAlign = "center";
  ctx.fillText(title, canvas.width / 2, canvas.height / 2 - 20);
  ctx.fillText(author, canvas.width / 2, canvas.height / 2 + 20);

  return canvas.toDataURL("image/png");
}
</script>

<template>
  <div class="container-fluid">
    
    <!-- поиск -->
    <SearchFilter/>

    <!-- вывод карточек книг -->
    <!-- сделать условное выделение от количесва книг в доступе -->
    <div class="books-grid"> 
      <Card
        v-for="book in books"
        :key="book.title"
        :title="book.title"
        :author="book.author"
        :imageUrl="book.imageUrl"
        :quantity="book.quantity"
      />
    </div>

  </div>
</template>

<script>
  import Card from "@/components/Card.vue";
  import SearchFilter from "@/components/SearchFilter.vue";
  
  export default {
    name: 'HomePage',
    components: {
      Card,
      SearchFilter,
    }
  }

</script>



<style scoped>
  .container {
    padding: 20px;
  }

  .books-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
  }

  .filters {
    margin-bottom: 20px;
  }
</style>