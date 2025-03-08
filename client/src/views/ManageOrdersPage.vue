<script lang="ts" setup>
import { onMounted, ref } from "vue";
import {
  fetchNewOrders,
  fetchProcessingOrders,
  fetchReadyOrders,
  fetchDoneOrders,
} from "@/api/order";
import type { ShortOrder, PaginatedOrders } from "@/api/types";
const newOrders = ref<ShortOrder>();
const processingOrders = ref<ShortOrder>();
const readyOrders = ref<ShortOrder>();
const doneOrders = ref<PaginatedOrders>();
onMounted(async () => {
  newOrders.value = await fetchNewOrders();
  processingOrders.value = await fetchProcessingOrders();
  readyOrders.value = await fetchReadyOrders();
  doneOrders.value = await fetchDoneOrders();
});
</script>

<template>
  {{ newOrders }} <br />
  =================================<br />
  {{ processingOrders }} <br />
  =================================<br />
  {{ readyOrders }} <br />
  =================================<br />
  {{ doneOrders }} <br />
</template>

<style lang="scss" scoped></style>
