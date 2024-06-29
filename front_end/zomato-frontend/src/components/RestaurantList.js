import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function RestaurantList() {
  const [restaurants, setRestaurants] = useState([]);
  const [page, setPage] = useState(0);
  const [country, setCountry] = useState('');
  const [avgSpend, setAvgSpend] = useState('');
  const [cuisines, setCuisines] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchRestaurants = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      let url = `http://localhost:8000/restaurants?skip=${page * 10}&limit=10`;
      if (country) url += `&country=${encodeURIComponent(country)}`;
      if (avgSpend) url += `&avg_spend=${encodeURIComponent(avgSpend)}`;
      if (cuisines) url += `&cuisines=${encodeURIComponent(cuisines)}`;

      const response = await axios.get(url);
      setRestaurants(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching restaurants:', error);
      setError('Error fetching restaurants. Please try again.');
      setLoading(false);
    }
  }, [page, country, avgSpend, cuisines]);

  useEffect(() => {
    fetchRestaurants();
  }, [fetchRestaurants]);

  const handleFilter = (e) => {
    e.preventDefault();
    setPage(0);
    fetchRestaurants();
  };

  return (
    <div className="restaurant-list">
      <h2>Restaurant List</h2>
      
      <form onSubmit={handleFilter} className="filter-form">
        <input 
          type="text" 
          value={country} 
          onChange={(e) => setCountry(e.target.value)} 
          placeholder="Country"
        />
        <input 
          type="number" 
          value={avgSpend} 
          onChange={(e) => setAvgSpend(e.target.value)} 
          placeholder="Average Spend"
        />
        <input 
          type="text" 
          value={cuisines} 
          onChange={(e) => setCuisines(e.target.value)} 
          placeholder="Cuisines (comma-separated)"
        />
        <button type="submit">Apply Filters</button>
      </form>

      {loading && <div>Loading...</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}

      {!loading && !error && (
        <>
          <div className="restaurant-items">
            {restaurants.map(restaurant => (
              <div key={restaurant.Restaurant_ID} className="restaurant-item">
                <Link to={`/restaurant/${restaurant.Restaurant_ID}`}>
                  {restaurant.Restaurant_Name}
                </Link>
              </div>
            ))}
            {restaurants.length === 0 && <div>No restaurants found.</div>}
          </div>
          <div className="pagination">
            <button onClick={() => setPage(prev => Math.max(0, prev - 1))} disabled={page === 0}>Previous</button>
            <button onClick={() => setPage(prev => prev + 1)} disabled={restaurants.length < 10}>Next</button>
          </div>
        </>
      )}
    </div>
  );
}

export default RestaurantList;