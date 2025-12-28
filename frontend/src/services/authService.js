import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class AuthService {
  constructor() {
    this.token = localStorage.getItem('token');
    this.setupInterceptors();
  }

  setupInterceptors() {
    axios.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.logout();
        }
        return Promise.reject(error);
      }
    );
  }

  async login(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await axios.post(`${API_BASE_URL}/auth/token`, formData);
    this.token = response.data.access_token;
    localStorage.setItem('token', this.token);
    return response.data;
  }

  async register(username, email, password) {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, {
      username,
      email,
      password
    });
    return response.data;
  }

  logout() {
    this.token = null;
    localStorage.removeItem('token');
    window.location.href = '/login';
  }

  isAuthenticated() {
    return !!this.token;
  }
}

const authService = new AuthService();
export { axios }; // Export configured axios instance
export default authService;