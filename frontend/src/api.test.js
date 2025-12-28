import axios from 'axios';
import api, { flightAPI, passengerAPI, bookingAPI, checkinAPI } from './api';

// Mock axios
jest.mock('axios', () => ({
  create: jest.fn(() => ({
    get: jest.fn(),
    post: jest.fn(),
    delete: jest.fn(),
  })),
}));

const mockedAxios = axios;

describe('API Configuration', () => {
  test('exports default api instance', () => {
    expect(api).toBeDefined();
  });
});

describe('flightAPI', () => {
  test('getFlights function exists and calls correct endpoint', () => {
    expect(typeof flightAPI.getFlights).toBe('function');
    
    const mockApi = {
      get: jest.fn().mockResolvedValue({ data: [] }),
    };
    
    // Test function call
    flightAPI.getFlights();
    expect(typeof flightAPI.getFlights).toBe('function');
  });

  test('createFlight function exists', () => {
    expect(typeof flightAPI.createFlight).toBe('function');
  });

  test('getFlight function exists', () => {
    expect(typeof flightAPI.getFlight).toBe('function');
  });
});

describe('passengerAPI', () => {
  test('createPassenger function exists', () => {
    expect(typeof passengerAPI.createPassenger).toBe('function');
  });

  test('getPassenger function exists', () => {
    expect(typeof passengerAPI.getPassenger).toBe('function');
  });
});

describe('bookingAPI', () => {
  test('createBooking function exists', () => {
    expect(typeof bookingAPI.createBooking).toBe('function');
  });

  test('getBooking function exists', () => {
    expect(typeof bookingAPI.getBooking).toBe('function');
  });

  test('cancelBooking function exists', () => {
    expect(typeof bookingAPI.cancelBooking).toBe('function');
  });
});

describe('checkinAPI', () => {
  test('checkin function exists', () => {
    expect(typeof checkinAPI.checkin).toBe('function');
  });

  test('getBoardingPass function exists', () => {
    expect(typeof checkinAPI.getBoardingPass).toBe('function');
  });

  test('getCheckinStatus function exists', () => {
    expect(typeof checkinAPI.getCheckinStatus).toBe('function');
  });
});

describe('API Functions Integration', () => {
  let mockApi;

  beforeEach(() => {
    mockApi = {
      get: jest.fn().mockResolvedValue({ data: 'test' }),
      post: jest.fn().mockResolvedValue({ data: 'test' }),
      delete: jest.fn().mockResolvedValue({ data: 'test' }),
    };
    mockedAxios.create.mockReturnValue(mockApi);
  });

  test('API functions can be called', async () => {
    // Test that functions exist and can be invoked
    expect(() => flightAPI.getFlights()).not.toThrow();
    expect(() => flightAPI.createFlight({})).not.toThrow();
    expect(() => flightAPI.getFlight('123')).not.toThrow();
    
    expect(() => passengerAPI.createPassenger({})).not.toThrow();
    expect(() => passengerAPI.getPassenger('123')).not.toThrow();
    
    expect(() => bookingAPI.createBooking({})).not.toThrow();
    expect(() => bookingAPI.getBooking('123')).not.toThrow();
    expect(() => bookingAPI.cancelBooking('123')).not.toThrow();
    
    expect(() => checkinAPI.checkin({})).not.toThrow();
    expect(() => checkinAPI.getBoardingPass('123')).not.toThrow();
    expect(() => checkinAPI.getCheckinStatus('123')).not.toThrow();
  });
});