import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import CheckinPage from './CheckinPage';

describe('CheckinPage Component', () => {
  test('renders check-in page title', () => {
    render(<CheckinPage />);
    
    expect(screen.getByText('Web Check-in')).toBeInTheDocument();
    expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('Web Check-in');
  });

  test('displays coming soon message', () => {
    render(<CheckinPage />);
    
    expect(screen.getByText('Check-in functionality coming soon...')).toBeInTheDocument();
  });

  test('has proper structure', () => {
    render(<CheckinPage />);
    
    const container = screen.getByText('Web Check-in').parentElement;
    expect(container).toBeInTheDocument();
    
    const heading = screen.getByRole('heading', { level: 2 });
    expect(heading).toHaveClass('text-2xl', 'font-bold', 'mb-4');
  });
});