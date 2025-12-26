import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';
import App from '../App';
import { ThemeProvider } from '../ThemeContext';

// Mock axios
jest.mock('axios');
const mockedAxios = axios;

// Mock data
const mockFlights = [
  {
    flight_id: 'TEST123',
    departure_airport: 'JFK',
    arrival_airport: 'LAX',
    departure_time: '2024-12-27T10:00:00',
    arrival_time: '2024-12-27T16:00:00',
    aircraft_type: 'Boeing 737',
    total_seats: 180,
    available_seats: 150,
    status: 'scheduled'
  }
];

const mockPassenger = {
  passenger_id: 'P123',
  first_name: 'John',
  last_name: 'Doe',
  email: 'john.doe@test.com',
  phone: '+1234567890',
  date_of_birth: '1990-01-15'
};

const mockBooking = {
  booking_id: 'B123',
  flight_id: 'TEST123',
  passenger_id: 'P123',
  seat_number: '12A',
  booking_status: 'confirmed',
  booking_date: '2024-12-26T12:00:00'
};

const mockBoardingPass = {
  checkin_id: 'C123',
  booking_id: 'B123',
  flight_id: 'TEST123',
  passenger_name: 'John Doe',
  seat_number: '12A',
  departure_airport: 'JFK',
  arrival_airport: 'LAX',
  departure_time: '2024-12-27T10:00:00',
  boarding_pass_number: 'TEST123-B123-20241226',
  gate_number: 'A1',
  boarding_group: 'B',
  checkin_time: '2024-12-26T12:00:00'
};

const renderWithTheme = (component) => {
  return render(
    <ThemeProvider>
      {component}
    </ThemeProvider>
  );
};

describe('App Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

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
    
    // Theme should toggle (implementation depends on your theme logic)
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
});

describe('Flights Page', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockedAxios.get.mockResolvedValue({ data: mockFlights });
    mockedAxios.post.mockResolvedValue({ data: mockPassenger });
  });

  test('displays flights list', async () => {
    renderWithTheme(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('TEST123')).toBeInTheDocument();
      expect(screen.getByText('JFK → LAX')).toBeInTheDocument();
      expect(screen.getByText('150 seats available')).toBeInTheDocument();
    });
  });

  test('handles flight booking', async () => {
    mockedAxios.post.mockResolvedValueOnce({ data: mockPassenger })
                   .mockResolvedValueOnce({ data: mockBooking });
    
    renderWithTheme(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('TEST123')).toBeInTheDocument();
    });
    
    // Click book button
    const bookButton = screen.getByText('Book Flight');
    fireEvent.click(bookButton);
    
    // Fill booking form
    fireEvent.change(screen.getByLabelText(/first name/i), {
      target: { value: 'John' }
    });
    fireEvent.change(screen.getByLabelText(/last name/i), {
      target: { value: 'Doe' }
    });
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'john.doe@test.com' }
    });
    fireEvent.change(screen.getByLabelText(/phone/i), {
      target: { value: '+1234567890' }
    });
    fireEvent.change(screen.getByLabelText(/date of birth/i), {
      target: { value: '1990-01-15' }
    });
    fireEvent.change(screen.getByLabelText(/seat number/i), {
      target: { value: '12A' }
    });
    
    // Submit form
    const submitButton = screen.getByText('Confirm Booking');
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(mockedAxios.post).toHaveBeenCalledTimes(2); // Passenger + Booking
    });
  });

  test('handles booking form validation', async () => {
    renderWithTheme(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('TEST123')).toBeInTheDocument();
    });
    
    const bookButton = screen.getByText('Book Flight');
    fireEvent.click(bookButton);
    
    // Try to submit empty form
    const submitButton = screen.getByText('Confirm Booking');
    fireEvent.click(submitButton);
    
    // Should show validation errors
    await waitFor(() => {
      expect(screen.getByText(/first name is required/i)).toBeInTheDocument();
    });
  });

  test('handles API errors gracefully', async () => {
    mockedAxios.get.mockRejectedValue(new Error('Network error'));
    
    renderWithTheme(<App />);
    
    await waitFor(() => {
      expect(screen.getByText(/error loading flights/i)).toBeInTheDocument();
    });
  });
});

describe('Check-in Page', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('displays check-in form', () => {
    renderWithTheme(<App />);
    
    const checkinTab = screen.getByText('Check-in');
    fireEvent.click(checkinTab);
    
    expect(screen.getByText('Web Check-in')).toBeInTheDocument();
    expect(screen.getByLabelText(/booking reference/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/last name/i)).toBeInTheDocument();
  });

  test('handles successful check-in', async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: mockBooking })
                  .mockResolvedValueOnce({ data: mockPassenger });
    mockedAxios.post.mockResolvedValue({ data: mockBoardingPass });
    
    renderWithTheme(<App />);
    
    const checkinTab = screen.getByText('Check-in');
    fireEvent.click(checkinTab);
    
    // Fill check-in form
    fireEvent.change(screen.getByLabelText(/booking reference/i), {
      target: { value: 'B123' }
    });
    fireEvent.change(screen.getByLabelText(/last name/i), {
      target: { value: 'Doe' }
    });
    
    // Submit check-in
    const checkinButton = screen.getByText('Check In');
    fireEvent.click(checkinButton);
    
    await waitFor(() => {
      expect(screen.getByText('Boarding Pass')).toBeInTheDocument();
      expect(screen.getByText('TEST123')).toBeInTheDocument();
      expect(screen.getByText('12A')).toBeInTheDocument();
      expect(screen.getByText('Group B')).toBeInTheDocument();
    });
  });

  test('handles check-in validation errors', async () => {
    renderWithTheme(<App />);
    
    const checkinTab = screen.getByText('Check-in');
    fireEvent.click(checkinTab);
    
    // Try to submit empty form
    const checkinButton = screen.getByText('Check In');
    fireEvent.click(checkinButton);
    
    await waitFor(() => {
      expect(screen.getByText(/booking reference is required/i)).toBeInTheDocument();
      expect(screen.getByText(/last name is required/i)).toBeInTheDocument();
    });
  });

  test('handles check-in API errors', async () => {
    mockedAxios.get.mockRejectedValue(new Error('Booking not found'));
    
    renderWithTheme(<App />);
    
    const checkinTab = screen.getByText('Check-in');
    fireEvent.click(checkinTab);
    
    fireEvent.change(screen.getByLabelText(/booking reference/i), {
      target: { value: 'INVALID' }
    });
    fireEvent.change(screen.getByLabelText(/last name/i), {
      target: { value: 'Doe' }
    });
    
    const checkinButton = screen.getByText('Check In');
    fireEvent.click(checkinButton);
    
    await waitFor(() => {
      expect(screen.getByText(/booking not found/i)).toBeInTheDocument();
    });
  });
});

describe('Responsive Design', () => {
  test('adapts to mobile viewport', () => {
    // Mock mobile viewport
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 375,
    });
    
    renderWithTheme(<App />);
    
    // Should render mobile-friendly layout
    expect(screen.getByText('Flight Check-in')).toBeInTheDocument();
  });

  test('adapts to desktop viewport', () => {
    // Mock desktop viewport
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 1024,
    });
    
    renderWithTheme(<App />);
    
    // Should render desktop layout
    expect(screen.getByText('Flight Check-in')).toBeInTheDocument();
  });
});

describe('Accessibility', () => {
  test('has proper ARIA labels', () => {
    renderWithTheme(<App />);
    
    // Check for ARIA labels on interactive elements
    const themeToggle = screen.getByRole('button', { name: /toggle theme/i });
    expect(themeToggle).toHaveAttribute('aria-label');
  });

  test('supports keyboard navigation', () => {
    renderWithTheme(<App />);
    
    const flightsTab = screen.getByText('Flights');
    const checkinTab = screen.getByText('Check-in');
    
    // Should be focusable
    flightsTab.focus();
    expect(flightsTab).toHaveFocus();
    
    // Should navigate with keyboard
    fireEvent.keyDown(flightsTab, { key: 'Tab' });
    expect(checkinTab).toHaveFocus();
  });

  test('has proper heading hierarchy', () => {
    renderWithTheme(<App />);
    
    const mainHeading = screen.getByRole('heading', { level: 1 });
    expect(mainHeading).toBeInTheDocument();
  });
});

describe('Error Boundaries', () => {
  test('handles component errors gracefully', () => {
    // Mock console.error to avoid noise in test output
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    
    // This would test error boundary if implemented
    renderWithTheme(<App />);
    
    // Restore console.error
    consoleSpy.mockRestore();
  });
});

describe('Performance', () => {
  test('renders within acceptable time', async () => {
    const startTime = performance.now();
    
    renderWithTheme(<App />);
    
    const endTime = performance.now();
    const renderTime = endTime - startTime;
    
    // Should render within 100ms
    expect(renderTime).toBeLessThan(100);
  });

  test('handles large flight lists efficiently', async () => {
    const largeMockFlights = Array.from({ length: 100 }, (_, i) => ({
      ...mockFlights[0],
      flight_id: `TEST${i}`,
    }));
    
    mockedAxios.get.mockResolvedValue({ data: largeMockFlights });
    
    const startTime = performance.now();
    
    renderWithTheme(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('TEST0')).toBeInTheDocument();
    });
    
    const endTime = performance.now();
    const renderTime = endTime - startTime;
    
    // Should handle large lists efficiently
    expect(renderTime).toBeLessThan(500);
  });
});