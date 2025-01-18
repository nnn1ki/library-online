import apiClient from './index';

const options = {method: 'GET', url: 'https://library.istu.edu/opac/api/announces'};

export const announcesItems = async () => {
    try{
        // const { data } = await apiClient.get('/announces');
        const { data } = await axios.request(options);
        console.log("data", data);
        return data; 
    }catch (error) {
        console.error("Ошибка при поиске новинок", error);
        throw error;
    }
}

