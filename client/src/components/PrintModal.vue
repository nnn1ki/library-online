<template>
  <div id="PrintingList">
    <h1>Заказ #{{ selectedOrder.id }}</h1>
    <h3>Книги ({{ selectedOrder.books.length }})</h3>
    <qrcode-vue :value="selectedOrder.user.library_card" :size="300" level="H" render-as="svg" />
  </div>
</template>

<script setup lang="ts">
  import { defineProps, ref, computed } from "vue";
  import QrcodeVue from 'qrcode.vue';
  import type { Order } from "@/api/types";
  import VueHtmlToPaper from "vue-html-to-paper";

  const props = defineProps<{
    order: Order;
  }>();

  const selectedOrder = ref<Order>(props.order);
</script>
