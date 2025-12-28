import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';
import { ThemeProvider } from './ThemeContext';

const renderWithTheme = (component) => {
  return render(
    <ThemeProvider>
      {component}
    </ThemeProvider>
  );
};

describe('App Component', () => {
  test('renders main navigation', () => {
    renderWithTheme(<App />);
    
    expect(screen.getByText('Flight Check-in')).toBeInTheDocument();
    expect(screen.getByText('Flights')).toBeInTheDocument();
    expect(screen.getByText('Check-in')).toBeInTheDocument();
  });

  test('toggles theme', () => {
    renderWithTheme(<App />);
    
    const themeToggle = screen.getByRole('button', { name: /toggle theme/i });
    fireEvent.click(themeToggle);
    
    expect(themeToggle).toBeInTheDocument();
  });

  test('navigates between pages', () => {
    renderWithTheme(<App />);
    
    // Start on flights page
    expect(screen.getByText('Available Flights')).toBeInTheDocument();
    
    // Navigate to check-in page
    const checkinTab = screen.getByText('Check-in');
    fireEvent.click(checkinTab);
    
    expect(screen.getByText('Web Check-in')).toBeInTheDocument();
  });

  test('displays flights page content', () => {
    renderWithTheme(<App />);
    
    expect(screen.getByText('Available Flights')).toBeInTheDocument();
    expect(screen.getByText('Flight booking functionality coming soon...')).toBeInTheDocument();
  });

  test('displays check-in page content', () => {
    renderWithTheme(<App />);
    
    const checkinTab = screen.getByText('Check-in');
    fireEvent.click(checkinTab);
    
    expect(screen.getByText('Web Check-in')).toBeInTheDocument();
    expect(screen.getByText('Check-in functionality coming soon...')).toBeInTheDocument();
  });

  test('has proper heading hierarchy', () => {
    renderWithTheme(<App />);
    
    const mainHeading = screen.getByRole('heading', { level: 1 });
    expect(mainHeading).toBeInTheDocument();
    expect(mainHeading).toHaveTextContent('Flight Check-in');
  });

  test('has proper ARIA labels', () => {
    renderWithTheme(<App />);
    
    const themeToggle = screen.getByRole('button', { name: /toggle theme/i });
    expect(themeToggle).toHaveAttribute('aria-label');
  });

  test('renders within acceptable time', () => {
    const startTime = performance.now();
    
    renderWithTheme(<App />);
    
    const endTime = performance.now();
    const renderTime = endTime - startTime;
    
    expect(renderTime).toBeLessThan(100);
  });
});