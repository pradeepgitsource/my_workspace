import React from 'react';
import { Moon, Sun, Plane } from 'lucide-react';
import { useTheme } from '../ThemeContext';

const Header = ({ currentPage, setCurrentPage }) => {
  const { isDark, toggleTheme } = useTheme();

  return (
    <header className="bg-white dark:bg-gray-800 shadow-md transition-colors">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Plane className="w-8 h-8 text-primary-600" />
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Flight Check-in
          </h1>
        </div>

        <nav className="flex items-center gap-6">
          <button
            onClick={() => setCurrentPage('flights')}
            className={`font-medium transition-colors ${
              currentPage === 'flights'
                ? 'text-primary-600'
                : 'text-gray-600 dark:text-gray-300 hover:text-primary-600'
            }`}
          >
            Flights
          </button>
          <button
            onClick={() => setCurrentPage('checkin')}
            className={`font-medium transition-colors ${
              currentPage === 'checkin'
                ? 'text-primary-600'
                : 'text-gray-600 dark:text-gray-300 hover:text-primary-600'
            }`}
          >
            Check-in
          </button>
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            aria-label="Toggle theme"
          >
            {isDark ? (
              <Sun className="w-5 h-5 text-yellow-500" />
            ) : (
              <Moon className="w-5 h-5 text-gray-700" />
            )}
          </button>
        </nav>
      </div>
    </header>
  );
};

export default Header;
