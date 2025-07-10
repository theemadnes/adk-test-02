from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Tuple
import math

# --- Pydantic Models ---
class GridLocation(BaseModel):
    name: str
    x: int = Field(..., ge=0, le=99, description="X coordinate on a 100x100 grid (0-99).")
    y: int = Field(..., ge=0, le=99, description="Y coordinate on a 100x100 grid (0-99).")

class UserCoordinates(BaseModel):
    x: int = Field(..., ge=0, le=99, description="User's X coordinate (0-99).")
    y: int = Field(..., ge=0, le=99, description="User's Y coordinate (0-99).")

class ClosestLocationResponse(BaseModel):
    input_coordinates: UserCoordinates
    closest_location: GridLocation
    distance: float = Field(..., description="Euclidean distance to the closest location.")

app = FastAPI(
    title="Closest Location API (Grid)",
    description="Finds the closest named location on a 100x100 grid (0-99 for x and y) to the given input (x, y) coordinates.",
    version="1.0.0"
)

# Sample list of named locations on the grid
# Coordinates are integers between 0 and 99.
locations_db: List[GridLocation] = [
    GridLocation(name="Central Hub Hostel", x=50, y=50),
    GridLocation(name="North Outpost BnB", x=50, y=95),
    GridLocation(name="East Market Hotel", x=90, y=50),
    GridLocation(name="South West Inn", x=10, y=10),
    GridLocation(name="Library Properties", x=25, y=75),
    GridLocation(name="Cafe Hotel", x=70, y=30),
    GridLocation(name="Park Entrance Residences", x=5, y=40),
]

def euclidean_distance(coord1: Tuple[int, int], coord2: Tuple[int, int]) -> float:
    """Calculates the Euclidean distance between two grid coordinates."""
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# adding in a GET to just dump locations_db for testing
@app.get("/locations/", response_model=List[GridLocation])
async def get_locations():
    """
    Dumps JSON of locations_db.

    Example: `/locations/`
    """
    return locations_db

@app.get("/find_closest_location_on_grid/", response_model=ClosestLocationResponse)
async def find_closest_location_on_grid(
    x: int = Query(..., ge=0, le=99, description="Your X coordinate on the grid (0-99)."),
    y: int = Query(..., ge=0, le=99, description="Your Y coordinate on the grid (0-99).")
):
    """
    Finds the closest named location from a predefined list to the given (x, y) grid coordinates.
    Coordinates must be integers between 0 and 99, inclusive.

    Example: `/find_closest_location_on_grid/?x=30&y=40`
    """
    if not locations_db:
        raise HTTPException(status_code=404, detail="No locations available in the database.")

    user_coords_tuple = (x, y)
    closest_loc_obj = None
    min_distance = float('inf')

    for location in locations_db:
        location_coords_tuple = (location.x, location.y)
        distance = euclidean_distance(user_coords_tuple, location_coords_tuple)
        if distance < min_distance:
            min_distance = distance
            closest_loc_obj = location

    if closest_loc_obj:
        return ClosestLocationResponse(
            input_coordinates=UserCoordinates(x=x, y=y),
            closest_location=closest_loc_obj,
            distance=min_distance
        )
    else:
        # This case should ideally not be reached if locations_db is not empty
        # and initialized correctly, but it's good for robustness.
        raise HTTPException(status_code=500, detail="Could not determine the closest location.")

# To run this application:
# 1. Save it as a Python file (e.g., main_grid.py).
# 2. Install FastAPI, Uvicorn and Pydantic: pip install fastapi uvicorn pydantic
# 3. Run Uvicorn: uvicorn app:app --reload
# 4. Open your browser and go to: http://127.0.0.1:8000/find_closest_location_on_grid/?x=YOUR_X&y=YOUR_Y
#    For example: curl "http://127.0.0.1:8000/find_closest_location_on_grid/?x=30&y=40"
#    You can also access the auto-generated API docs at http://127.0.0.1:8000/docs
