import { axios } from './services/authService';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Use the authenticated axios instance from AuthService
const api = axios;
api.defaults.baseURL = API_BASE_URL;

export const flightAPI = {
  getFlights: () => api.get('/api/flights'),
  createFlight: (flightData) => api.post('/api/flights', flightData),
  getFlight: (flightId) => api.get(`/api/flights/${flightId}`),
};

export const passengerAPI = {
  createPassenger: (passengerData) => api.post('/api/passengers', passengerData),
  getPassenger: (passengerId) => api.get(`/api/passengers/${passengerId}`),
};

export const bookingAPI = {
  createBooking: (bookingData) => api.post('/api/bookings', bookingData),
  getBooking: (bookingId) => api.get(`/api/bookings/${bookingId}`),
  cancelBooking: (bookingId) => api.delete(`/api/bookings/${bookingId}`),
};

export const checkinAPI = {
  checkin: (checkinData) => api.post('/api/checkin', checkinData),
  getBoardingPass: (checkinId) => api.get(`/api/checkin/${checkinId}`),
  getCheckinStatus: (bookingId) => api.get(`/api/bookings/${bookingId}/checkin-status`),
};

export default api;