import React from "react";
import axios from "axios";

const BeerDetails = ({ beer, onReduceStock }) => {
  const handleReduceStock = async () => {
    try {
      await axios.post(`http://localhost:8000/beers/reduce_stock/${beer.id}`, {
        ...beer,
        stock: beer.stock - 1,
      });
      onReduceStock(beer.id);
    } catch (error) {
      console.error("There was an error reducing the stock!", error);
    }
  };

  return (
    <div className="beer-details">
      <h2>{beer.name}</h2>
      <p>Stock: {beer.stock}</p>
      <p>Minimum Stock: {beer.min_stock}</p>
      <button onClick={handleReduceStock}>Percuter</button>
    </div>
  );
};

export default BeerDetails;
