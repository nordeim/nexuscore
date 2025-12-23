/**
 * API Client
 * Axios instance with auth interceptor and idempotency support
 */
import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

// Create axios instance
const apiClient = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 30000,
});

// Token storage (client-side only)
let accessToken: string | null = null;

/**
 * Set the access token for authentication
 */
export const setAccessToken = (token: string | null) => {
    accessToken = token;
    if (typeof window !== 'undefined' && token) {
        localStorage.setItem('access_token', token);
    }
};

/**
 * Get access token from storage
 */
export const getAccessToken = (): string | null => {
    if (accessToken) return accessToken;
    if (typeof window !== 'undefined') {
        return localStorage.getItem('access_token');
    }
    return null;
};

/**
 * Generate idempotency key for mutations
 */
export const generateIdempotencyKey = (): string => {
    return `${Date.now()}-${Math.random().toString(36).substring(2, 15)}`;
};

// Request interceptor - add auth token
apiClient.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        const token = getAccessToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor - handle errors
apiClient.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
        const originalRequest = error.config;

        // Handle 401 - token expired
        if (error.response?.status === 401 && originalRequest) {
            // Clear token and redirect to login
            setAccessToken(null);
            if (typeof window !== 'undefined') {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
            }
        }

        return Promise.reject(error);
    }
);

export default apiClient;

// Type-safe API methods
export const api = {
    get: <T>(url: string, config = {}) =>
        apiClient.get<T>(url, config).then(res => res.data),

    post: <T>(url: string, data = {}, config = {}) =>
        apiClient.post<T>(url, data, config).then(res => res.data),

    put: <T>(url: string, data = {}, config = {}) =>
        apiClient.put<T>(url, data, config).then(res => res.data),

    patch: <T>(url: string, data = {}, config = {}) =>
        apiClient.patch<T>(url, data, config).then(res => res.data),

    delete: <T>(url: string, config = {}) =>
        apiClient.delete<T>(url, config).then(res => res.data),

    // POST with idempotency key
    postIdempotent: <T>(url: string, data = {}, config = {}) =>
        apiClient.post<T>(url, data, {
            ...config,
            headers: {
                ...((config as { headers?: Record<string, string> }).headers || {}),
                'Idempotency-Key': generateIdempotencyKey(),
            },
        }).then(res => res.data),
};
