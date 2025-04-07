import { ref } from 'vue';

export const useFormattedDate = () => {
  const formatDate = (date: string | Date, locale: string = "ru-RU", options: Intl.DateTimeFormatOptions = { day: '2-digit', month: '2-digit', year: 'numeric' }) => {
    const formattedDate = new Date(date).toLocaleDateString(locale, options);
    return formattedDate;
  };

  return { formatDate };
};


