import React, { useState, useEffect } from "react";
import axios from "axios";

const OrderPage = () => {
  const [beers, setBeers] = useState([]);
  const [recommendedBeers, setRecommendedBeers] = useState([]);
  const [selectedBeers, setSelectedBeers] = useState({});

  useEffect(() => {
    fetchBeers();
  }, []);

  const fetchBeers = async () => {
    try {
      const response = await axios.get("http://localhost:8000/beers");
      const allBeers = response.data;
      setBeers(allBeers);
      setRecommendedBeers(
        allBeers.filter((beer) => beer.stock < beer.min_stock)
      );
    } catch (error) {
      console.error("There was an error fetching the beers!", error);
    }
  };

  const handleBeerChange = (event) => {
    const beerId = parseInt(event.target.value);
    setSelectedBeers((prevSelected) => {
      if (prevSelected[beerId]) {
        const { [beerId]: _, ...rest } = prevSelected;
        return rest;
      } else {
        return { ...prevSelected, [beerId]: 1 };
      }
    });
  };

  const handleQuantityChange = (event, beerId) => {
    const quantity = parseInt(event.target.value);
    setSelectedBeers((prevSelected) => ({
      ...prevSelected,
      [beerId]: quantity,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const orderItems = Object.keys(selectedBeers).map((beerId) => ({
      beer_id: parseInt(beerId),
      quantity: selectedBeers[beerId],
    }));
    try {
      await axios.post("http://localhost:8000/orders", {
        items: orderItems,
      });
      setSelectedBeers({});
      fetchBeers();
    } catch (error) {
      console.error("There was an error creating the order!", error);
    }
  };

  return (
    <div className="order-page">
      <h1>Passer une commande</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Bières recommandées</label>
          <div>
            {recommendedBeers.map((beer) => (
              <div key={beer.id}>
                <label>
                  <input
                    type="checkbox"
                    value={beer.id}
                    checked={!!selectedBeers[beer.id]}
                    onChange={handleBeerChange}
                  />
                  {beer.name} (Stock: {beer.stock})
                </label>
                {selectedBeers[beer.id] && (
                  <input
                    type="number"
                    value={selectedBeers[beer.id]}
                    min="1"
                    onChange={(event) => handleQuantityChange(event, beer.id)}
                  />
                )}
              </div>
            ))}
          </div>
        </div>
        <div>
          <label>Ajouter d'autres bières</label>
          <div>
            {beers
              .filter((beer) => !recommendedBeers.includes(beer))
              .map((beer) => (
                <div key={beer.id}>
                  <label>
                    <input
                      type="checkbox"
                      value={beer.id}
                      checked={!!selectedBeers[beer.id]}
                      onChange={handleBeerChange}
                    />
                    {beer.name} (Stock: {beer.stock})
                  </label>
                  {selectedBeers[beer.id] && (
                    <input
                      type="number"
                      value={selectedBeers[beer.id]}
                      min="1"
                      onChange={(event) => handleQuantityChange(event, beer.id)}
                    />
                  )}
                </div>
              ))}
          </div>
        </div>
        <button type="submit">Passer la commande</button>
      </form>
    </div>
  );
};

export default OrderPage;
