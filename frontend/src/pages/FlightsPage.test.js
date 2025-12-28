import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import FlightsPage from './FlightsPage';

describe('FlightsPage Component', () => {
  test('renders flights page title', () => {
    render(<FlightsPage />);
    
    expect(screen.getByText('Available Flights')).toBeInTheDocument();
    expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('Available Flights');
  });

  test('displays coming soon message', () => {
    render(<FlightsPage />);
    
    expect(screen.getByText('Flight booking functionality coming soon...')).toBeInTheDocument();
  });

  test('has proper structure', () => {
    render(<FlightsPage />);
    
    const container = screen.getByText('Available Flights').parentElement;
    expect(container).toBeInTheDocument();
    
    const heading = screen.getByRole('heading', { level: 2 });
    expect(heading).toHaveClass('text-2xl', 'font-bold', 'mb-4');
  });
});