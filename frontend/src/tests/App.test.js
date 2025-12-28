import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from '../App';
import AuthService from '../services/authService';

// Mock AuthService
jest.mock('../services/authService');
const mockedAuthService = AuthService;

// Mock components
jest.mock('../pages/LoginPage', () => {
  return function MockLoginPage() {
    return <div>Login Page</div>;
  };
});

jest.mock('../pages/FlightsPage', () => {
  return function MockFlightsPage() {
    return <div>Flights Page</div>;
  };
});

jest.mock('../pages/CheckinPage', () => {
  return function MockCheckinPage() {
    return <div>Checkin Page</div>;
  };
});

const renderApp = (initialPath = '/') => {
  window.history.pushState({}, 'Test page', initialPath);
  return render(
    <BrowserRouter>
      <App />
    </BrowserRouter>
  );
};

describe('App', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should render login page when not authenticated', () => {
    mockedAuthService.isAuthenticated.mockReturnValue(false);
    
    renderApp('/');
    
    expect(screen.getByText('Login Page')).toBeInTheDocument();
  });

  it('should render flights page when authenticated and on root path', () => {
    mockedAuthService.isAuthenticated.mockReturnValue(true);
    
    renderApp('/');
    
    expect(screen.getByText('Flights Page')).toBeInTheDocument();
  });

  it('should render checkin page when authenticated and on checkin path', () => {
    mockedAuthService.isAuthenticated.mockReturnValue(true);
    
    renderApp('/checkin');
    
    expect(screen.getByText('Checkin Page')).toBeInTheDocument();
  });

  it('should redirect to login when accessing protected route without auth', () => {
    mockedAuthService.isAuthenticated.mockReturnValue(false);
    
    renderApp('/checkin');
    
    expect(screen.getByText('Login Page')).toBeInTheDocument();
  });

  it('should show navigation when authenticated', () => {
    mockedAuthService.isAuthenticated.mockReturnValue(true);
    
    renderApp('/');
    
    expect(screen.getByText('Flight Check-in')).toBeInTheDocument();
    expect(screen.getByText('Flights')).toBeInTheDocument();
    expect(screen.getByText('Check-in')).toBeInTheDocument();
    expect(screen.getByText('Logout')).toBeInTheDocument();
  });

  it('should not show navigation when not authenticated', () => {
    mockedAuthService.isAuthenticated.mockReturnValue(false);
    
    renderApp('/');
    
    expect(screen.queryByText('Flight Check-in')).not.toBeInTheDocument();
    expect(screen.queryByText('Logout')).not.toBeInTheDocument();
  });

  it('should handle logout click', () => {
    mockedAuthService.isAuthenticated.mockReturnValue(true);
    mockedAuthService.logout = jest.fn();
    
    renderApp('/');
    
    const logoutButton = screen.getByText('Logout');
    logoutButton.click();
    
    expect(mockedAuthService.logout).toHaveBeenCalled();
  });
});