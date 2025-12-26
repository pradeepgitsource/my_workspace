import React, { useState } from 'react';
import FlightsList from '../components/FlightsList';
import BookingForm from '../components/BookingForm';

const FlightsPage = () => {
  const [selectedFlight, setSelectedFlight] = useState(null);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Available Flights
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Browse and book your flight
        </p>
      </div>

      <FlightsList onSelectFlight={setSelectedFlight} />

      {selectedFlight && (
        <BookingForm
          flight={selectedFlight}
          onClose={() => setSelectedFlight(null)}
        />
      )}
    </div>
  );
};

export default FlightsPage;
