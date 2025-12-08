import axios from "axios";


const axiosInstance = axios.create({
    baseURL: '/api',
    timeout:10000,
})

axiosInstance.interceptors.request.use(
    (config) => {
        return config;
    },
    (error) => {
        return Promise.reject(error);
    } 
);
axiosInstance.interceptors.response.use(
    (response) => {
        // 返回整个response对象而不仅仅是data，确保前端能正确处理
        return response;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default axiosInstance;