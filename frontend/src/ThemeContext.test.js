import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ThemeProvider, useTheme } from './ThemeContext';

// Test component to use the theme context
const TestComponent = () => {
  const { isDark, toggleTheme } = useTheme();
  
  return (
    <div>
      <span data-testid="theme-status">{isDark ? 'dark' : 'light'}</span>
      <button onClick={toggleTheme} data-testid="toggle-button">
        Toggle Theme
      </button>
    </div>
  );
};

describe('ThemeContext', () => {
  test('provides default light theme', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );
    
    expect(screen.getByTestId('theme-status')).toHaveTextContent('light');
  });

  test('toggles theme when button is clicked', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );
    
    const toggleButton = screen.getByTestId('toggle-button');
    const themeStatus = screen.getByTestId('theme-status');
    
    expect(themeStatus).toHaveTextContent('light');
    
    fireEvent.click(toggleButton);
    expect(themeStatus).toHaveTextContent('dark');
    
    fireEvent.click(toggleButton);
    expect(themeStatus).toHaveTextContent('light');
  });

  test('applies dark class when theme is dark', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );
    
    const toggleButton = screen.getByTestId('toggle-button');
    
    // Initially light theme
    expect(document.querySelector('.dark')).toBeNull();
    
    // Toggle to dark theme
    fireEvent.click(toggleButton);
    expect(document.querySelector('.dark')).toBeInTheDocument();
  });

  test('throws error when useTheme is used outside provider', () => {
    // Suppress console.error for this test
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    
    expect(() => {
      render(<TestComponent />);
    }).toThrow('useTheme must be used within a ThemeProvider');
    
    consoleSpy.mockRestore();
  });
});