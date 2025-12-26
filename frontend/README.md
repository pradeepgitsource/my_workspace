# Flight Check-in Frontend

A professional React application for flight web check-in with light and dark theme support.

## Features

- **Flight Browsing**: View available flights with details
- **Flight Booking**: Book flights with passenger information
- **Web Check-in**: Check in for booked flights and get boarding passes
- **Light/Dark Theme**: Toggle between light and dark modes
- **Responsive Design**: Works on desktop and mobile devices
- **Professional UI**: Built with Tailwind CSS

## Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

4. Update `.env` with your API URL (default is `http://localhost:8000/api`)

5. Start the development server:
```bash
npm start
```

The application will open at `http://localhost:3000`

## Docker

Build and run with Docker:

```bash
docker build -t flight-checkin-frontend .
docker run -p 3000:3000 flight-checkin-frontend
```

## Project Structure

```
src/
├── components/
│   ├── Header.js           # Navigation and theme toggle
│   ├── FlightsList.js      # Display available flights
│   ├── CheckinForm.js      # Web check-in form
│   └── BookingForm.js      # Flight booking form
├── pages/
│   ├── FlightsPage.js      # Flights page
│   └── CheckinPage.js      # Check-in page
├── App.js                  # Main app component
├── index.js                # React entry point
├── index.css               # Global styles
├── api.js                  # API client
└── ThemeContext.js         # Theme management
```

## API Integration

The frontend communicates with the backend API at the URL specified in `.env`:

- **Flights**: GET `/api/flights`, GET `/api/flights/{id}`
- **Passengers**: POST `/api/passengers`, GET `/api/passengers/{id}`
- **Bookings**: POST `/api/bookings`, GET `/api/bookings/{id}`, DELETE `/api/bookings/{id}`
- **Check-in**: POST `/api/checkin`, GET `/api/checkin/{id}`

## Theme Support

The application supports light and dark themes:
- Theme preference is saved to localStorage
- Respects system preference on first visit
- Toggle theme using the button in the header

## Build

Create a production build:

```bash
npm run build
```

The optimized build will be in the `build/` directory.
