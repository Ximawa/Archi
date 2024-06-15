import React, { useState, useEffect } from "react";
import axios from "axios";
import BeerDetails from "./BeerDetails";
import NewBeerForm from "./NewBeerForm";

const BeerList = () => {
  const [beers, setBeers] = useState([]);

  useEffect(() => {
    fetchBeers();
  }, []);

  const fetchBeers = async () => {
    try {
      const response = await axios.get("http://localhost:8000/beers");
      setBeers(response.data);
    } catch (error) {
      console.error("There was an error fetching the beers!", error);
    }
  };

  const handleReduceStock = (beerId) => {
    setBeers(
      beers.map((beer) =>
        beer.id === beerId ? { ...beer, stock: beer.stock - 1 } : beer
      )
    );
  };

  return (
    <>
      <NewBeerForm />
      <div className="beer-list">
        {beers.map((beer) => (
          <BeerDetails
            key={beer.id}
            beer={beer}
            onReduceStock={handleReduceStock}
          />
        ))}
      </div>
    </>
  );
};

export default BeerList;
