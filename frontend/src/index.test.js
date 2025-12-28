import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import { ThemeProvider } from './ThemeContext';

// Mock ReactDOM
jest.mock('react-dom/client', () => ({
  createRoot: jest.fn(() => ({
    render: jest.fn(),
  })),
}));

// Mock App component
jest.mock('./App', () => {
  return function MockApp() {
    return <div>Mock App</div>;
  };
});

// Mock ThemeProvider
jest.mock('./ThemeContext', () => ({
  ThemeProvider: ({ children }) => <div>{children}</div>,
}));

describe('index.js', () => {
  test('renders App with ThemeProvider', () => {
    // Mock DOM element
    const mockElement = document.createElement('div');
    mockElement.id = 'root';
    document.getElementById = jest.fn().mockReturnValue(mockElement);

    // Mock createRoot
    const mockRender = jest.fn();
    const mockRoot = { render: mockRender };
    createRoot.mockReturnValue(mockRoot);

    // Import and run index.js
    require('./index.js');

    // Verify createRoot was called with root element
    expect(createRoot).toHaveBeenCalledWith(mockElement);
    
    // Verify render was called
    expect(mockRender).toHaveBeenCalled();
  });
});