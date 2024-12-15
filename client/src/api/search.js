import apiClient from './index';

/**
 * Выполнить поиск книг.
 * @param {Object} searchParams - Параметры поиска.
 * @param {string} searchParams.database - База данных для поиска.
 * @param {string} searchParams.expression - Поисковое выражение.
 * @param {string} searchParams.format - Формат данных.
 * @param {Object} searchParams.years - Диапазон лет.
 * @returns {Promise<Object>} - Результаты поиска.
 */
export const searchBooks = async (searchParams) => {
  try {
    const { data } = await apiClient.post('/search', searchParams);
    return data; // Вернуть данные для обработки
  } catch (error) {
    console.error('Ошибка при поиске книг:', error);
    throw error; // Пробросить ошибку для обработки в компонентах
  }
};