import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export const authHeaders = (token) => ({
  headers: { Authorization: `Bearer ${token}` },
});
