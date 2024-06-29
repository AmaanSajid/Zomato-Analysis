from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3
import logging
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Restaurant(BaseModel):
    Restaurant_ID: int
    Restaurant_Name: str
    Country_Code: int
    City: str
    Address: str
    Locality: str
    Locality_Verbose: str
    Longitude: float
    Latitude: float
    Cuisines: str
    Average_Cost_for_two: float
    Currency: str
    Has_Table_booking: str
    Has_Online_delivery: str
    Is_delivering_now: str
    Switch_to_order_menu: str
    Price_range: int
    Aggregate_rating: float
    Rating_color: str
    Rating_text: str
    Votes: int
    Country: str

def get_db_connection():
    conn = sqlite3.connect('zomato_database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/restaurant/{restaurant_id}", response_model=Restaurant)
async def get_restaurant(restaurant_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM zomato_restaurants WHERE Restaurant_ID = ?", (restaurant_id,))
        restaurant = cursor.fetchone()
        
        conn.close()
        
        if restaurant is None:
            
        return {}
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/restaurants", response_model=List[Restaurant])
async def get_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    country: Optional[str] = Query(None, description="Filter by country"),
    avg_spend: Optional[float] = Query(None, description="Filter by average spend for two people"),
    cuisines: Optional[str] = Query(None, description="Filter by cuisines (comma-separated)")
):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM zomato_restaurants WHERE 1=1"
        params = []

        if country:
            query += " AND Country = ?"
            params.append(country)

        if avg_spend is not None:
            query += " AND Average_Cost_for_two <= ?"
            params.append(avg_spend)

        if cuisines:
            cuisine_list = [cuisine.strip().lower() for cuisine in cuisines.split(',')]
            cuisine_conditions = " OR ".join(["lower(Cuisines) LIKE ?" for _ in cuisine_list])
            query += f" AND ({cuisine_conditions})"
            params.extend([f"%{cuisine.lower()}%" for cuisine in cuisine_list])

        query += " ORDER BY Restaurant_ID LIMIT ? OFFSET ?"
        params.extend([limit, skip])

        cursor.execute(query, params)
        restaurants = cursor.fetchall()
        
        conn.close()
        
        return [dict(restaurant) for restaurant in restaurants]
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)