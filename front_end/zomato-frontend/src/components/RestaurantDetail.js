import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

function RestaurantDetail() {
  const [restaurant, setRestaurant] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    const fetchRestaurant = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`http://localhost:8000/restaurant/${id}`);
        setRestaurant(response.data);
        setLoading(false);
      } catch (err) {
        setError('Error fetching restaurant details');
        setLoading(false);
      }
    };

    fetchRestaurant();
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;
  if (!restaurant) return <div>No restaurant found</div>;

  return (
    <div className="restaurant-detail">
      <h2>{restaurant.Restaurant_Name}</h2>
      <p><strong>City:</strong> {restaurant.City}</p>
      <p><strong>Address:</strong> {restaurant.Address}</p>
      <p><strong>Locality:</strong> {restaurant.Locality}</p>
      <p><strong>Cuisines:</strong> {restaurant.Cuisines}</p>
      <p><strong>Average Cost for Two:</strong> {restaurant.Average_Cost_for_two} {restaurant.Currency}</p>
      <p><strong>Has Table Booking:</strong> {restaurant.Has_Table_booking}</p>
      <p><strong>Has Online Delivery:</strong> {restaurant.Has_Online_delivery}</p>
      <p><strong>Price Range:</strong> {restaurant.Price_range}</p>
      <p><strong>Aggregate Rating:</strong> {restaurant.Aggregate_rating}</p>
      <p><strong>Rating Color:</strong> {restaurant.Rating_color}</p>
      <p><strong>Rating Text:</strong> {restaurant.Rating_text}</p>
      <p><strong>Votes:</strong> {restaurant.Votes}</p>
      <Link to="/">Back to Restaurant List</Link>
    </div>
  );
}

export default RestaurantDetail;