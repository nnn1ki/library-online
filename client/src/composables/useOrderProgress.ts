import { ref } from "vue";

export const useOrderProgress = () => {
  type ModalStep = {
    title: string;
    error: string;
    messages: string[] | null;
  };

  type ModalState = {
    isOpen: boolean;
    currentStep: number;
    steps: ModalStep[];
    isSuccess: boolean;
    isError: boolean;
  };

  const DEFAULT_STEPS: ModalStep[] = [
    {
      title: "Проверка авторизации",
      error: "Кажется вы не авторизованы, попробуйте перезайти в аккаунт",
      messages: null,
    },
    {
      title: "Проверка количества книг",
      error: "Вы заказали слишком много книг, уменьшите их кол-во",
      messages: null,
    },
    {
      title: "Проверка возвращаемых книг",
      error: "Нужно отметить книги выше, пообещайте что принесете их",
      messages: null,
    },
    {
      title: "Проверка доступности книг",
      error:
        "Кажется некоторые книги не досутпны для заказа,\nони либо не доступны, либо они уже есть у вас\nв прошлых заказах или на руках",
      messages: null,
    },
    {
      title: "Проверка лимитов",
      error: "У вас слишком много заказанных книг или книг на руках",
      messages: null,
    },
    {
      title: "Создание заказа",
      error: "Что то пошло не так, попробуйте ще раз",
      messages: null,
    },
  ];

  const modalState = ref<ModalState>({
    isOpen: false,
    currentStep: 0,
    steps: DEFAULT_STEPS,
    isSuccess: false,
    isError: false,
  });

  const resetModalState = () => {
    modalState.value = {
      ...modalState.value,
      currentStep: 0,
      isSuccess: false,
      isError: false,
      steps: [...DEFAULT_STEPS],
    };
  };

  return {
    modalState,
    resetModalState,
  };
};
