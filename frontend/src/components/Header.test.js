import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Header from './Header';
import { ThemeProvider } from '../ThemeContext';

const renderWithTheme = (component) => {
  return render(
    <ThemeProvider>
      {component}
    </ThemeProvider>
  );
};

describe('Header Component', () => {
  test('renders header with title', () => {
    renderWithTheme(<Header />);
    
    expect(screen.getByText('Flight Check-in')).toBeInTheDocument();
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Flight Check-in');
  });

  test('renders theme toggle button', () => {
    renderWithTheme(<Header />);
    
    const toggleButton = screen.getByRole('button', { name: /toggle theme/i });
    expect(toggleButton).toBeInTheDocument();
    expect(toggleButton).toHaveAttribute('aria-label', 'Toggle theme');
  });

  test('displays moon icon initially (light theme)', () => {
    renderWithTheme(<Header />);
    
    const toggleButton = screen.getByRole('button', { name: /toggle theme/i });
    expect(toggleButton).toHaveTextContent('🌙');
  });

  test('toggles theme icon when clicked', () => {
    renderWithTheme(<Header />);
    
    const toggleButton = screen.getByRole('button', { name: /toggle theme/i });
    
    // Initially shows moon (light theme)
    expect(toggleButton).toHaveTextContent('🌙');
    
    // Click to toggle to dark theme
    fireEvent.click(toggleButton);
    expect(toggleButton).toHaveTextContent('☀️');
    
    // Click again to toggle back to light theme
    fireEvent.click(toggleButton);
    expect(toggleButton).toHaveTextContent('🌙');
  });

  test('has proper CSS classes', () => {
    renderWithTheme(<Header />);
    
    const header = screen.getByRole('banner');
    expect(header).toHaveClass('bg-blue-600', 'text-white');
    
    const toggleButton = screen.getByRole('button', { name: /toggle theme/i });
    expect(toggleButton).toHaveClass('p-2', 'rounded-md', 'bg-blue-700', 'hover:bg-blue-800');
  });
});