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
  createFlight: (flightData) => api.post('/flights', flightData),
  getFlight: (flightId) => api.get(`/flights/${flightId}`),
};

export const passengerAPI = {
  createPassenger: (passengerData) => api.post('/passengers', passengerData),
  getPassenger: (passengerId) => api.get(`/passengers/${passengerId}`),
};

export const bookingAPI = {
  createBooking: (bookingData) => api.post('/bookings', bookingData),
  getBooking: (bookingId) => api.get(`/bookings/${bookingId}`),
  cancelBooking: (bookingId) => api.delete(`/bookings/${bookingId}`),
};

export const checkinAPI = {
  checkin: (checkinData) => api.post('/checkin', checkinData),
  getBoardingPass: (checkinId) => api.get(`/checkin/${checkinId}`),
  getCheckinStatus: (bookingId) => api.get(`/bookings/${bookingId}/checkin-status`),
};

export default api;