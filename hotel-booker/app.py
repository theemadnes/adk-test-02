import uuid
from typing import List, Dict

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

# --- Pydantic Models ---
class BookingCreate(BaseModel):
    hotel_name: str
    duration: int = Field(..., gt=0, description="Duration of stay in days, must be greater than 0")
    customer_name: str

class BookingRecord(BookingCreate):
    booking_id: uuid.UUID = Field(default_factory=uuid.uuid4)

# --- In-memory Database ---
# A simple dictionary to store bookings in memory
bookings_db: Dict[uuid.UUID, BookingRecord] = {}

# --- FastAPI Application ---
app = FastAPI(
    title="Hotel Booker API",
    description="API for creating and retrieving hotel bookings.",
    version="1.0.0"
)

# --- API Endpoints ---
@app.post("/bookings/", response_model=BookingRecord, status_code=status.HTTP_201_CREATED)
async def create_booking(booking_in: BookingCreate):
    """
    Create a new hotel booking.
    """
    new_booking = BookingRecord(**booking_in.model_dump())
    bookings_db[new_booking.booking_id] = new_booking
    return new_booking

@app.get("/bookings/", response_model=List[BookingRecord])
async def get_all_bookings():
    """
    Retrieve all existing booking records.
    """
    return list(bookings_db.values())

