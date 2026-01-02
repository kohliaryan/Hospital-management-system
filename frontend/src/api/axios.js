import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:5000/api', // Your Flask URL
    headers: {
        'Content-Type': 'application/json'
    }
});

// Optional: Automatically add the token to every request if you use login
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authentication = `Bearer ${token}`; // Flask-Security usually expects this
    }
    return config;
});

export default api;