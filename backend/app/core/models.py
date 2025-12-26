from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class Flight(Base):
    __tablename__ = "flights"
    
    flight_id = Column(String, primary_key=True, index=True)
    departure_airport = Column(String, nullable=False)
    arrival_airport = Column(String, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    aircraft_type = Column(String, nullable=False)
    total_seats = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)
    status = Column(String, default="scheduled")
    
    bookings = relationship("Booking", back_populates="flight")

class Passenger(Base):
    __tablename__ = "passengers"
    
    passenger_id = Column(String, primary_key=True, index=True, default=generate_uuid)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=False)
    
    bookings = relationship("Booking", back_populates="passenger")

class Booking(Base):
    __tablename__ = "bookings"
    
    booking_id = Column(String, primary_key=True, index=True, default=generate_uuid)
    flight_id = Column(String, ForeignKey("flights.flight_id"), nullable=False)
    passenger_id = Column(String, ForeignKey("passengers.passenger_id"), nullable=False)
    seat_number = Column(String, nullable=False)
    booking_status = Column(String, default="confirmed")
    booking_date = Column(DateTime, default=datetime.utcnow)
    
    flight = relationship("Flight", back_populates="bookings")
    passenger = relationship("Passenger", back_populates="bookings")
    checkin = relationship("CheckinRecord", back_populates="booking", uselist=False)

class CheckinRecord(Base):
    __tablename__ = "checkin_records"
    
    checkin_id = Column(String, primary_key=True, index=True, default=generate_uuid)
    booking_id = Column(String, ForeignKey("bookings.booking_id"), nullable=False)
    checkin_time = Column(DateTime, default=datetime.utcnow)
    boarding_pass_number = Column(String, unique=True, nullable=False)
    gate_number = Column(String)
    boarding_group = Column(String, nullable=False)
    
    booking = relationship("Booking", back_populates="checkin")