<template>
  <div v-if="selectedOrder" class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Детали заказа #{{ selectedOrder.id }}</h2>
        <button class="close-button" @click="closeModal">×</button>
      </div>

      <div class="modal-body">
        <div class="section">
          <h3>Заказчик:</h3>
          <span>{{ selectedOrder.user.last_name + " " + selectedOrder.user.first_name }}</span>
        </div>
        <div class="section">
          <h3>История статусов</h3>
          <ul class="status-list">
            <li v-for="status in selectedOrder.statuses" :key="status.date" class="status-item">
              <span class="status-date">{{ formatDate(status.date) }}</span>
              <span class="status-badge" :class="'status-' + status.status">
                {{ orderStatuses[status.status] }}  
              </span>
              <span v-if="status.staff !== null" class="staff-name">
                {{ status.staff?.first_name + " " + status.staff?.last_name }} 
              </span>
              <span v-if="status.description" class="status-description">
                ({{ status.description }})
              </span>
            </li>
          </ul>
        </div>

        <div class="section">
          <h3>Книги ({{ selectedOrder.books.length }})</h3>
          <div class="books-container" :class="{failed : isCheckFailed}">
            <div v-for="orderBook in selectedOrder.books" :key="orderBook.id" class="book-card" :class="{failed : isCheckFailed}">
              <ShortBookCard :book="orderBook.book" :truncate="isCheckFailed"/>
              <!-- <div class="extend-info">
                <div class="book-number">
                  <span class="status-label">Инвентраный номер книги: </span>
                  <span class="status-value" :class="'status-' + orderBook.status">
                    {{ orderBook.book.id }}
                  </span>
                </div>
                <div class="book-status">
                  <span class="status-label">Статус:</span>
                  <span class="status-value" :class="'status-' + orderBook.status">
                    {{ orderBookStatuses[orderBook.status] }}
                  </span>
                </div>

                <div v-if="orderBook.handed_date" class="book-date">
                  <span class="date-label">Выдана:</span>
                  <span class="date-value">{{ formatDate(orderBook.handed_date) }}</span>
                </div>

                <div v-if="orderBook.to_return_date" class="book-date">
                  <span class="date-label">Вернуть до:</span>
                  <span class="date-value">{{ formatDate(orderBook.to_return_date) }}</span>
                </div>

                <div v-if="orderBook.returned_date" class="book-date">
                  <span class="date-label">Возвращена:</span>
                  <span class="date-value">{{ formatDate(orderBook.returned_date) }}</span>
                </div>
              </div> -->
              <template v-if="isCheckFailed">
            <div class="some-info">
              Пока
            </div>
            <div class="some-info">
              все
            </div>
          </template>
          </div>
        </div>
        </div>
      </div>

      <div class="modal-footer">
        <StyledButton
          v-if="prevStatus"
          :disabled="!hasPrevStatus"
          @click="changeToPrevStatus"
          theme="accent"
          >{{ prevStatusButtonText }}</StyledButton
        >
        <StyledButton
          v-if="nextStatus"
          :disabled="!hasNextStatus"
          @click="changeToNextStatus"
          theme="secondary"
          >{{ nextStatusButtonText }}</StyledButton
        >
      </div>
      <button @click="isCheckFailed = !isCheckFailed">Престаиваем вид для неудачной проверки</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed} from "vue";
import ShortBookCard from "@/components/ShortBookCard.vue";
import StyledButton from "./StyledButton.vue";
import type { Order, OrderCheckingInfo } from "@/api/types";
import type { OrderStatusEnum } from "@/api/types";
import { orderStatuses} from "@/api/types";
import VueHtmlToPaper from 'vue-html-to-paper';

const props = defineProps<{
  order: Order;
}>();
const statusTransitions = {
  new: {
    next: "processing",
    prev: null,
    nextButtonText: "Взять в работу",
    prevButtonText: "",
  },
  processing: {
    next: "ready",
    prev: "new",
    nextButtonText: "Проверить готовность",
    prevButtonText: "Вернуть в новые",
  },
  ready: {
    next: "done",
    prev: "processing",
    nextButtonText: "Выдать заказ",
    prevButtonText: "Вернуть в сборку",
  },
  done: {
    next: "archived",
    prev: "ready",
    nextButtonText: "В архив",
    prevButtonText: "Вернуть к выдаче",
  },
  archived: {
    next: null,
    prev: "done",
    nextButtonText: "",
    prevButtonText: "Вернуть из архива",
  },
  cancelled: {
    next: null,
    prev: null,
    nextButtonText: "",
    prevButtonText: "",
  },
  error: {
    next: null,
    prev: null,
    nextButtonText: "",
    prevButtonText: "",
  },
} as const;

const emit = defineEmits<{
  (e: "close"): void;
  (e: "nextOrderStatus", orderId: number, nextStatus: OrderStatusEnum): void;
  (e: "checkOrder", orderId: number): OrderCheckingInfo;
}>();

const selectedOrder = ref<Order>(props.order);

const isCheckFailed = ref(false);

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleString("ru-RU");
}

function closeModal() {
  emit("close");
}

function printSearchList() {
  const options = {
    name: 'searchList',
    specs: [
      'fullscreen=yes',
      'titlebar=yes',
      'scrollbars=yes'
    ],
    styles: []
  }
}

const currentStatus = computed(() => {
  return props.order.statuses[props.order.statuses.length - 1].status;
});

const hasPrevStatus = computed(() => {
  return !!statusTransitions[currentStatus.value].prev;
});

const hasNextStatus = computed(() => {
  return !!statusTransitions[currentStatus.value].next;
});

const prevStatus = computed(() => {
  return statusTransitions[currentStatus.value].prev;
});

const nextStatus = computed(() => {
  return statusTransitions[currentStatus.value].next;
});

const prevStatusButtonText = computed(() => {
  return statusTransitions[currentStatus.value].prevButtonText;
});

const nextStatusButtonText = computed(() => {
  return statusTransitions[currentStatus.value].nextButtonText;
});

const changeToPrevStatus = () => {
  if (prevStatus.value) {
    emit("nextOrderStatus", selectedOrder.value.id, prevStatus.value);
    emit("close");
  }
};

const changeToNextStatus = () => {
  if (nextStatus.value) {
    emit("nextOrderStatus", selectedOrder.value.id, nextStatus.value);
    emit("close");
  }
};

</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: grid;
  place-items: center;
  z-index: 1000;
  padding: 1rem;
}

.some-info {
  background-color: red;
  text-align: center;
  width: 150px;
}

.modal-content {
  background: var(--color-background-50);
  border-radius: 0.5rem;
  width: min(100%, 56rem);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.2);
  border: 1px solid var(--color-text-200);
}

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--color-text-100);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--color-background-100);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.375rem;
  color: var(--color-text-800);
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-text-400);
  padding: 0 0.5rem;
  line-height: 1;
  transition: color 0.2s;
}

.close-button:hover {
  color: var(--color-primary-600);
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex-grow: 1;
}

.section {
  margin-bottom: 1.5rem;
}

.section h3 {
  margin: 0 0 1rem;
  font-size: 1.125rem;
  color: var(--color-text-700);
  border-bottom: 1px solid var(--color-text-100);
  padding-bottom: 0.5rem;
  font-weight: 500;
}

.status-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.status-item {
  padding: 0.75rem 0;
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  border-bottom: 1px dashed var(--color-text-100);
}

.status-item:last-child {
  border-bottom: none;
}

.status-date {
  color: var(--color-text-500);
  font-size: 0.875rem;
  min-width: 10rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid transparent;
}

.status-new {
  background-color: var(--background-status-new);
  color: var(--color-status-new);
  border-color: var(--color-status-new);
}

.status-processing {
  background-color: var(--background-status-processing);
  color: var(--color-status-processing);
  border-color: var(--color-status-processing);
}

.status-ready {
  background-color: var(--background-status-ready);
  color: var(--color-status-ready);
  border-color: var(--color-status-ready);
}

.status-done {
  background-color: var(--background-status-done);
  color: var(--color-status-done);
  border-color: var(--color-status-done);
}

.status-cancelled {
  background-color: var(--background-status-cancelled);
  color: var(--color-status-cancelled);
  border-color: var(--color-status-cancelled);
}

.status-error {
  background-color: var(--background-status-error);
  color: var(--color-status-error);
  border-color: var(--color-status-error);
}

.status-archived {
  background-color: var(--background-status-archived);
  color: var(--color-status-archived);
  border-color: var(--color-status-archived);
}

.status-description {
  color: var(--color-text-500);
  font-size: 0.875rem;
  flex-basis: 100%;
  margin-top: 0.25rem;
  padding-left: 11rem;
}

.books-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(18rem, 1fr));
  gap: 1rem;
  &.failed {
    grid-template-columns: repeat(1, minmax(18rem, 1fr));
  }
}

.book-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1rem;
  gap: 0.5rem;
  background-color: var(--color-background-100);
  transition:
    transform 0.2s,
    box-shadow 0.2s;

  &.failed {
    flex-direction: row;
  }
}

.book-card:hover {
  transform: translateY(-0.125rem);
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.1);
}

.extend-info {
  padding: 1rem;
  background-color: var(--color-accent-200);
  font-size: 0.875rem;
}

.book-number,
.book-status,
.book-date {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.status-label,
.date-label {
  color: var(--color-text-500);
}

.status-value {
  font-weight: 500;
}

.status-ordered {
  color: var(--color-primary-600);
}
.status-handed {
  color: var(--color-secondary-600);
}
.status-returned {
  color: var(--color-accent-600);
}
.status-cancelled {
  color: var(--color-text-700);
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--color-text-100);
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  background-color: var(--color-background-100);
}

@media (max-width: 640px) {
  .status-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .status-date {
    min-width: auto;
  }

  .status-description {
    padding-left: 0;
  }

  .books-container {
    grid-template-columns: 1fr;
  }

  .modal-footer {
    flex-direction: column;
  }
}
</style>
