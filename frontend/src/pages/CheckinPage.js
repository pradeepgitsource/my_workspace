import React, { useState } from 'react';
import { checkinAPI } from '../api';

const CheckinPage = () => {
  const [bookingId, setBookingId] = useState('');
  const [passengerId, setPassengerId] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleCheckin = async (e) => {
    e.preventDefault();
    if (!bookingId || !passengerId) {
      setError('Please enter both Booking ID and Passenger ID');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await checkinAPI.checkin({
        booking_id: bookingId,
        passenger_id: passengerId
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Check-in failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Web Check-in</h2>
      
      <form onSubmit={handleCheckin} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Booking ID
          </label>
          <input
            type="text"
            value={bookingId}
            onChange={(e) => setBookingId(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            placeholder="Enter booking ID"
          />
        </div>
        
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Passenger ID
          </label>
          <input
            type="text"
            value={passengerId}
            onChange={(e) => setPassengerId(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            placeholder="Enter passenger ID"
          />
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-2 px-4 rounded-md transition duration-200"
        >
          {loading ? 'Checking in...' : 'Check In'}
        </button>
      </form>
      
      {error && (
        <div className="mt-4 p-4 bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-600 text-red-700 dark:text-red-200 rounded">
          {error}
        </div>
      )}
      
      {result && (
        <div className="mt-4 p-4 bg-green-100 dark:bg-green-900 border border-green-400 dark:border-green-600 text-green-700 dark:text-green-200 rounded">
          <h3 className="font-semibold mb-2">Check-in Successful!</h3>
          <p><strong>Boarding Pass:</strong> {result.boarding_pass_number}</p>
          <p><strong>Flight:</strong> {result.flight_id}</p>
          <p><strong>Seat:</strong> {result.seat_number}</p>
          <p><strong>Boarding Group:</strong> {result.boarding_group}</p>
          {result.gate_number && <p><strong>Gate:</strong> {result.gate_number}</p>}
        </div>
      )}
    </div>
  );
};

export default CheckinPage;