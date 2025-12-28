import React, { useState } from 'react';
import { ThemeProvider } from './ThemeContext';
import Header from './components/Header';
import FlightsPage from './pages/FlightsPage';
import CheckinPage from './pages/CheckinPage';

function App() {
  const [activeTab, setActiveTab] = useState('flights');

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Header />
        <nav className="bg-white dark:bg-gray-800 shadow">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex space-x-8">
              <button
                onClick={() => setActiveTab('flights')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'flights'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                Flights
              </button>
              <button
                onClick={() => setActiveTab('checkin')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'checkin'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                Check-in
              </button>
            </div>
          </div>
        </nav>
        
        <main className="max-w-7xl mx-auto py-6 px-4">
          {activeTab === 'flights' && <FlightsPage />}
          {activeTab === 'checkin' && <CheckinPage />}
        </main>
      </div>
    </ThemeProvider>
  );
}

export default App;