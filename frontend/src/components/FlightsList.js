import React, { useState, useEffect } from 'react';
import { Calendar, MapPin, Plane, AlertCircle } from 'lucide-react';
import { flightAPI } from '../api';

const FlightsList = ({ onSelectFlight }) => {
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchFlights();
  }, []);

  const fetchFlights = async () => {
    try {
      setLoading(true);
      const response = await flightAPI.getFlights();
      setFlights(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load flights');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 flex gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0" />
          <p className="text-red-700 dark:text-red-300">{error}</p>
        </div>
      )}

      {flights.length === 0 ? (
        <div className="text-center py-12">
          <Plane className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">No flights available</p>
        </div>
      ) : (
        flights.map((flight) => (
          <div key={flight.flight_id} className="card hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-4 mb-3">
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                    {flight.flight_id}
                  </h3>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    flight.status === 'scheduled'
                      ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                  }`}>
                    {flight.status}
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                    <MapPin className="w-4 h-4" />
                    <span>{flight.departure_airport} → {flight.arrival_airport}</span>
                  </div>
                  <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                    <Calendar className="w-4 h-4" />
                    <span>{new Date(flight.departure_time).toLocaleString()}</span>
                  </div>
                </div>

                <div className="mt-3 text-sm text-gray-600 dark:text-gray-400">
                  <p>{flight.aircraft_type} • {flight.available_seats}/{flight.total_seats} seats available</p>
                </div>
              </div>

              <button
                onClick={() => onSelectFlight(flight)}
                className="btn-primary ml-4"
              >
                Select
              </button>
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default FlightsList;
