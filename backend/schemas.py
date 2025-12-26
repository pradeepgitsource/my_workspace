from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
import re

class FlightCreate(BaseModel):
    flight_id: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    aircraft_type: str
    total_seats: int

class FlightResponse(BaseModel):
    flight_id: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    aircraft_type: str
    total_seats: int
    available_seats: int
    status: str

    class Config:
        from_attributes = True

class PassengerCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: str
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters')
        return v.strip().title()
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        pattern = r'^\+?1?[0-9]{10,15}$'
        clean_phone = re.sub(r'[-\s()]', '', v)
        if not re.match(pattern, clean_phone):
            raise ValueError('Invalid phone format')
        return clean_phone

class PassengerResponse(BaseModel):
    passenger_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    date_of_birth: str

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    flight_id: str
    passenger_id: str
    seat_number: Optional[str] = None
    
    @field_validator('seat_number')
    @classmethod
    def validate_seat(cls, v):
        if v is not None:
            pattern = r'^[1-9][0-9]?[A-F]$'
            if not re.match(pattern, v.upper()):
                raise ValueError('Seat must be in format like 12A')
            return v.upper()
        return v

class BookingResponse(BaseModel):
    booking_id: str
    flight_id: str
    passenger_id: str
    seat_number: str
    booking_status: str
    booking_date: datetime

    class Config:
        from_attributes = True

class CheckinRequest(BaseModel):
    booking_id: str
    passenger_id: str

class BoardingPassResponse(BaseModel):
    checkin_id: str
    boarding_pass_number: str
    flight_id: str
    seat_number: str
    boarding_group: str
    gate_number: Optional[str]
    checkin_time: datetime

    class Config:
        from_attributes = True