import axios from 'axios';
// import { keycloakInstance } from '../App';

const API = axios.create({
    baseURL: process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:8000' : 'http://127.0.0.1:8000',
    withCredentials: true,
    // : '/api'
},);

// export const callProtectedApi = async () => {
//     const token = keycloakInstance.token;

//     const response = await fetch(`${API}/api/protected`, {
//     headers: {
//         'Authorization': `Bearer ${token}`,
//         'Content-Type': 'application/json',
//     },
//     });
    
//     if (!response.ok) {
//     throw new Error('API call failed');
//     }
    
//     return response.json();
// };

// export const callPublicApi = async () => {
//     const response = await fetch(`${API}/api/public`);
//     return response.json();
// };



export default API