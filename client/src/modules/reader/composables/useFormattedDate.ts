export const useFormattedDate = () => {
  const formatDate = (date?: string | Date | null) => {
    if (!date) {
      return "---";
    }

    const parsedDate = new Date(date);
    if (Number.isNaN(parsedDate.getTime())) {
      return "---";
    }

    return parsedDate.toLocaleDateString("ru-RU");
  };

  return { formatDate };
};
