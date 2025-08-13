import axios from 'axios';

const API = axios.create({
    baseURL: process.env.NODE_ENV === 'development'
    ? 'http://127.0.0.1:8000'
    : 'http://127.0.0.1:8000'
    // : '/api'
});

export default API