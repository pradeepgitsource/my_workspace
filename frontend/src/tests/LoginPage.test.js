import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import LoginPage from '../pages/LoginPage';
import AuthService from '../services/authService';

// Mock AuthService
jest.mock('../services/authService');
const mockedAuthService = AuthService;

// Mock useNavigate
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

const renderLoginPage = () => {
  return render(
    <BrowserRouter>
      <LoginPage />
    </BrowserRouter>
  );
};

describe('LoginPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should render login form', () => {
    renderLoginPage();
    
    expect(screen.getByText('Login')).toBeInTheDocument();
    expect(screen.getByLabelText('Username')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Login' })).toBeInTheDocument();
  });

  it('should handle successful login', async () => {
    mockedAuthService.login.mockResolvedValue({ access_token: 'test_token' });
    
    renderLoginPage();
    
    fireEvent.change(screen.getByLabelText('Username'), { target: { value: 'testuser' } });
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'password' } });
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));
    
    await waitFor(() => {
      expect(mockedAuthService.login).toHaveBeenCalledWith('testuser', 'password');
      expect(mockNavigate).toHaveBeenCalledWith('/');
    });
  });

  it('should handle login error', async () => {
    mockedAuthService.login.mockRejectedValue(new Error('Invalid credentials'));
    
    renderLoginPage();
    
    fireEvent.change(screen.getByLabelText('Username'), { target: { value: 'testuser' } });
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'wrongpass' } });
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));
    
    await waitFor(() => {
      expect(screen.getByText('Login failed. Please try again.')).toBeInTheDocument();
    });
  });

  it('should show loading state during login', async () => {
    mockedAuthService.login.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));
    
    renderLoginPage();
    
    fireEvent.change(screen.getByLabelText('Username'), { target: { value: 'testuser' } });
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'password' } });
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));
    
    expect(screen.getByText('Logging in...')).toBeInTheDocument();
  });

  it('should prevent form submission with empty fields', () => {
    renderLoginPage();
    
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));
    
    expect(mockedAuthService.login).not.toHaveBeenCalled();
  });

  it('should update form fields on input change', () => {
    renderLoginPage();
    
    const usernameInput = screen.getByLabelText('Username');
    const passwordInput = screen.getByLabelText('Password');
    
    fireEvent.change(usernameInput, { target: { value: 'newuser' } });
    fireEvent.change(passwordInput, { target: { value: 'newpass' } });
    
    expect(usernameInput.value).toBe('newuser');
    expect(passwordInput.value).toBe('newpass');
  });
});