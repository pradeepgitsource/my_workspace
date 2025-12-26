import React, { useState } from 'react';
import { AlertCircle, CheckCircle, Loader } from 'lucide-react';
import { checkinAPI, bookingAPI } from '../api';

const CheckinForm = () => {
  const [bookingId, setBookingId] = useState('');
  const [passengerId, setPassengerId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [boardingPass, setBoardingPass] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setBoardingPass(null);

    if (!bookingId || !passengerId) {
      setError('Please fill in all fields');
      return;
    }

    try {
      setLoading(true);
      const response = await checkinAPI.performCheckin({
        booking_id: bookingId,
        passenger_id: passengerId,
      });

      setBoardingPass(response.data.data);
      setSuccess('Check-in successful!');
      setBookingId('');
      setPassengerId('');
    } catch (err) {
      const message = err.response?.data?.detail || 'Check-in failed';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="card">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          Web Check-in
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Booking ID
            </label>
            <input
              type="text"
              value={bookingId}
              onChange={(e) => setBookingId(e.target.value)}
              placeholder="Enter your booking ID"
              className="input-field"
              disabled={loading}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Passenger ID
            </label>
            <input
              type="text"
              value={passengerId}
              onChange={(e) => setPassengerId(e.target.value)}
              placeholder="Enter your passenger ID"
              className="input-field"
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader className="w-4 h-4 animate-spin" />
                Processing...
              </>
            ) : (
              'Check-in'
            )}
          </button>
        </form>

        {error && (
          <div className="mt-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 flex gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0" />
            <p className="text-red-700 dark:text-red-300">{error}</p>
          </div>
        )}

        {success && (
          <div className="mt-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4 flex gap-3">
            <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0" />
            <p className="text-green-700 dark:text-green-300">{success}</p>
          </div>
        )}
      </div>

      {boardingPass && (
        <div className="mt-6 card border-2 border-primary-600">
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            Boarding Pass
          </h3>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Boarding Pass #:</span>
              <span className="font-mono font-bold text-gray-900 dark:text-white">
                {boardingPass.boarding_pass_number}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Flight:</span>
              <span className="font-bold text-gray-900 dark:text-white">
                {boardingPass.flight_id}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Seat:</span>
              <span className="font-bold text-gray-900 dark:text-white">
                {boardingPass.seat_number}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Boarding Group:</span>
              <span className="font-bold text-primary-600">{boardingPass.boarding_group}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Gate:</span>
              <span className="font-bold text-gray-900 dark:text-white">
                {boardingPass.gate_number}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Check-in Time:</span>
              <span className="text-gray-900 dark:text-white">
                {new Date(boardingPass.checkin_time).toLocaleString()}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CheckinForm;
