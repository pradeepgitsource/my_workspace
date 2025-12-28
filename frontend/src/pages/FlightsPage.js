import React, { useState, useEffect } from 'react';
import { flightAPI } from '../api';

const FlightsPage = () => {
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [testingConnection, setTestingConnection] = useState(false);

  const testConnection = async () => {
    setTestingConnection(true);
    try {
      const response = await fetch('http://localhost:8000/health');
      const data = await response.json();
      console.log('Backend health check:', data);
      alert('✅ Backend connection successful!');
    } catch (err) {
      console.error('Backend connection failed:', err);
      alert('❌ Cannot connect to backend. Please start the backend server.');
    } finally {
      setTestingConnection(false);
    }
  };

  useEffect(() => {
    const fetchFlights = async () => {
      try {
        console.log('Fetching flights from:', process.env.REACT_APP_API_URL || 'http://localhost:8000/api');
        const response = await flightAPI.getFlights();
        console.log('Flights response:', response.data);
        setFlights(response.data);
      } catch (err) {
        console.error('Error fetching flights:', err);
        if (err.code === 'ECONNREFUSED' || err.message.includes('Network Error')) {
          setError('Cannot connect to backend server. Please ensure the backend is running on port 8000.');
        } else if (err.response) {
          setError(`Server error: ${err.response.status} - ${err.response.data?.detail || 'Unknown error'}`);
        } else {
          setError('Failed to load flights. Please check your connection.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchFlights();
  }, []);

  if (loading) return <div className="text-center py-8">Loading flights...</div>;
  if (error) return <div className="text-red-600 text-center py-8">{error}</div>;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Available Flights</h2>
        <button
          onClick={testConnection}
          disabled={testingConnection}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-md text-sm"
        >
          {testingConnection ? 'Testing...' : 'Test Connection'}
        </button>
      </div>
      
      {flights.length === 0 ? (
        <div className="text-center py-8 text-gray-500 dark:text-gray-400">
          No flights available
        </div>
      ) : (
        <div className="grid gap-4">
          {flights.map((flight) => (
            <div key={flight.flight_id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    {flight.flight_id}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300">
                    {flight.departure_airport} → {flight.arrival_airport}
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {flight.aircraft_type}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Available Seats
                  </p>
                  <p className="text-lg font-semibold text-green-600">
                    {flight.available_seats}/{flight.total_seats}
                  </p>
                </div>
              </div>
              
              <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-gray-500 dark:text-gray-400">Departure</p>
                  <p className="font-medium text-gray-900 dark:text-white">
                    {new Date(flight.departure_time).toLocaleString()}
                  </p>
                </div>
                <div>
                  <p className="text-gray-500 dark:text-gray-400">Arrival</p>
                  <p className="font-medium text-gray-900 dark:text-white">
                    {new Date(flight.arrival_time).toLocaleString()}
                  </p>
                </div>
              </div>
              
              <div className="mt-4">
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                  flight.status === 'scheduled' 
                    ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                    : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
                }`}>
                  {flight.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FlightsPage;