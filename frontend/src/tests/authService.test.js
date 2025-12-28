import AuthService from '../services/authService';
import axios from 'axios';

// Mock axios
jest.mock('axios');
const mockedAxios = axios;

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
};
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// Mock window.location
delete window.location;
window.location = { href: '' };

describe('AuthService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorageMock.getItem.mockReturnValue(null);
    AuthService.token = null;
  });

  describe('constructor', () => {
    it('should initialize with token from localStorage', () => {
      localStorageMock.getItem.mockReturnValue('test_token');
      const authService = new (require('../services/authService').default.constructor)();
      expect(localStorageMock.getItem).toHaveBeenCalledWith('token');
    });

    it('should setup axios interceptors', () => {
      expect(mockedAxios.interceptors.request.use).toHaveBeenCalled();
      expect(mockedAxios.interceptors.response.use).toHaveBeenCalled();
    });
  });

  describe('setupInterceptors', () => {
    it('should add Authorization header when token exists', () => {
      AuthService.token = 'test_token';
      const config = { headers: {} };
      
      // Get the request interceptor
      const requestInterceptor = mockedAxios.interceptors.request.use.mock.calls[0][0];
      const result = requestInterceptor(config);
      
      expect(result.headers.Authorization).toBe('Bearer test_token');
    });

    it('should not add Authorization header when token is null', () => {
      AuthService.token = null;
      const config = { headers: {} };
      
      const requestInterceptor = mockedAxios.interceptors.request.use.mock.calls[0][0];
      const result = requestInterceptor(config);
      
      expect(result.headers.Authorization).toBeUndefined();
    });

    it('should handle request interceptor error', () => {
      const requestErrorHandler = mockedAxios.interceptors.request.use.mock.calls[0][1];
      const error = new Error('Request error');
      
      expect(requestErrorHandler(error)).rejects.toBe(error);
    });

    it('should return response on success', () => {
      const response = { data: 'test' };
      const responseInterceptor = mockedAxios.interceptors.response.use.mock.calls[0][0];
      
      expect(responseInterceptor(response)).toBe(response);
    });

    it('should logout on 401 error', () => {
      const logoutSpy = jest.spyOn(AuthService, 'logout');
      const error = { response: { status: 401 } };
      const responseErrorHandler = mockedAxios.interceptors.response.use.mock.calls[0][1];
      
      expect(responseErrorHandler(error)).rejects.toBe(error);
      expect(logoutSpy).toHaveBeenCalled();
    });

    it('should not logout on non-401 error', () => {
      const logoutSpy = jest.spyOn(AuthService, 'logout');
      const error = { response: { status: 500 } };
      const responseErrorHandler = mockedAxios.interceptors.response.use.mock.calls[0][1];
      
      expect(responseErrorHandler(error)).rejects.toBe(error);
      expect(logoutSpy).not.toHaveBeenCalled();
    });

    it('should handle error without response', () => {
      const logoutSpy = jest.spyOn(AuthService, 'logout');
      const error = { message: 'Network error' };
      const responseErrorHandler = mockedAxios.interceptors.response.use.mock.calls[0][1];
      
      expect(responseErrorHandler(error)).rejects.toBe(error);
      expect(logoutSpy).not.toHaveBeenCalled();
    });
  });

  describe('login', () => {
    it('should login successfully', async () => {
      const mockResponse = { data: { access_token: 'new_token' } };
      mockedAxios.post.mockResolvedValue(mockResponse);
      
      const result = await AuthService.login('testuser', 'password');
      
      expect(mockedAxios.post).toHaveBeenCalledWith(
        'http://localhost:8000/auth/token',
        expect.any(FormData)
      );
      expect(AuthService.token).toBe('new_token');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('token', 'new_token');
      expect(result).toEqual({ access_token: 'new_token' });
    });

    it('should handle login error', async () => {
      const error = new Error('Login failed');
      mockedAxios.post.mockRejectedValue(error);
      
      await expect(AuthService.login('testuser', 'password')).rejects.toThrow('Login failed');
    });
  });

  describe('register', () => {
    it('should register successfully', async () => {
      const mockResponse = { data: { id: 1, username: 'testuser' } };
      mockedAxios.post.mockResolvedValue(mockResponse);
      
      const result = await AuthService.register('testuser', 'test@test.com', 'password');
      
      expect(mockedAxios.post).toHaveBeenCalledWith(
        'http://localhost:8000/auth/register',
        {
          username: 'testuser',
          email: 'test@test.com',
          password: 'password'
        }
      );
      expect(result).toEqual({ id: 1, username: 'testuser' });
    });

    it('should handle register error', async () => {
      const error = new Error('Registration failed');
      mockedAxios.post.mockRejectedValue(error);
      
      await expect(AuthService.register('testuser', 'test@test.com', 'password'))
        .rejects.toThrow('Registration failed');
    });
  });

  describe('logout', () => {
    it('should logout and redirect', () => {
      AuthService.token = 'test_token';
      
      AuthService.logout();
      
      expect(AuthService.token).toBeNull();
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('token');
      expect(window.location.href).toBe('/login');
    });
  });

  describe('isAuthenticated', () => {
    it('should return true when token exists', () => {
      AuthService.token = 'test_token';
      expect(AuthService.isAuthenticated()).toBe(true);
    });

    it('should return false when token is null', () => {
      AuthService.token = null;
      expect(AuthService.isAuthenticated()).toBe(false);
    });

    it('should return false when token is empty string', () => {
      AuthService.token = '';
      expect(AuthService.isAuthenticated()).toBe(false);
    });
  });
});