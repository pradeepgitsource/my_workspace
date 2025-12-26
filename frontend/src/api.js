import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const flightAPI = {
  getFlights: () => api.get('/flights'),
  getFlight: (flightId) => api.get(`/flights/${flightId}`),
  createFlight: (data) => api.post('/flights', data),
};

export const passengerAPI = {
  createPassenger: (data) => api.post('/passengers', data),
  getPassenger: (passengerId) => api.get(`/passengers/${passengerId}`),
  getPassengerBookings: (passengerId) => api.get(`/passengers/${passengerId}/bookings`),
};

export const bookingAPI = {
  createBooking: (data) => api.post('/bookings', data),
  getBooking: (bookingId) => api.get(`/bookings/${bookingId}`),
  cancelBooking: (bookingId) => api.delete(`/bookings/${bookingId}`),
  getCheckinStatus: (bookingId) => api.get(`/bookings/${bookingId}/checkin-status`),
};

export const checkinAPI = {
  performCheckin: (data) => api.post('/checkin', data),
  getBoardingPass: (checkinId) => api.get(`/checkin/${checkinId}`),
};

export default api;
