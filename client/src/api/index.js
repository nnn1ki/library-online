import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'https://library.istu.edu/opac/api', // Базовый URL API
    headers: {
      'Content-Type': 'application/json',
    },
  });

export default apiClient;