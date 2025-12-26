import React, { useState } from 'react';
import Header from './components/Header';
import FlightsPage from './pages/FlightsPage';
import CheckinPage from './pages/CheckinPage';

function App() {
  const [currentPage, setCurrentPage] = useState('flights');

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
      <Header currentPage={currentPage} setCurrentPage={setCurrentPage} />
      
      <main>
        {currentPage === 'flights' && <FlightsPage />}
        {currentPage === 'checkin' && <CheckinPage />}
      </main>

      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-12 transition-colors">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-600 dark:text-gray-400 text-sm">
          <p>&copy; 2024 Flight Check-in System. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
