import React from 'react';
import CheckinForm from '../components/CheckinForm';

const CheckinPage = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Web Check-in
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Check in for your flight and get your boarding pass
        </p>
      </div>

      <CheckinForm />
    </div>
  );
};

export default CheckinPage;
