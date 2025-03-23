<script lang="ts" setup>
import { onMounted, ref } from "vue";
import {
  fetchNewOrders,
  fetchProcessingOrders,
  fetchReadyOrders,
  fetchDoneOrders,
} from "@/api/order";

import type { UserOrder, PaginatedOrders } from "@/api/types";

const newOrders = ref<UserOrder>();
const processingOrders = ref<UserOrder>();
const readyOrders = ref<UserOrder>();
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
