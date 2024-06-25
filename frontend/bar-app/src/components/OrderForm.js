import React, { useState, useEffect } from "react";

const OrderForm = () => {
  const [orderItems, setOrderItems] = useState([{ beer_id: "", quantity: "" }]);
  const [recommendedBeers, setRecommendedBeers] = useState([]);
  const [allBeers, setAllBeers] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/beers/low_stock")
      .then((response) => response.json())
      .then((data) => {
        setRecommendedBeers(data);
        // Use `data` directly instead of `recommendedBeers` for immediate processing
        const initialOrderItems = data.map((beer) => ({
          beer_id: beer.id,
          quantity: Math.max(beer.min_stock - beer.stock, 0),
        }));

        setOrderItems([...initialOrderItems, { beer_id: "", quantity: "" }]);
      })
      .catch((error) =>
        console.error("Error fetching recommended beers:", error)
      );

    fetch("http://localhost:8000/beers/read_all")
      .then((response) => response.json())
      .then((data) => setAllBeers(data))
      .catch((error) => console.error("Error fetching all beers:", error));
  }, []);

  const handleInputChange = (index, event) => {
    const values = [...orderItems];
    if (event.target.name === "beer_id") {
      const beerIdValue = parseInt(event.target.value, 10);
      values[index].beer_id = isNaN(beerIdValue) ? "" : beerIdValue;
    } else {
      const quantityValue = parseInt(event.target.value, 10);
      values[index].quantity = isNaN(quantityValue) ? 0 : quantityValue;
    }
    setOrderItems(values);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const order = {
      items: orderItems.map((item) => ({
        beer_id: parseInt(item.beer_id, 10),
        quantity: parseInt(item.quantity, 10),
      })),
    };
    fetch("http://localhost:8000/orders/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(order),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Order submitted successfully:", data);
        // Do something with the response data
      })
      .catch((error) => {
        console.error("Error submitting order:", error);
        // Handle the error
      });
  };

  const handleAddFields = () => {
    const values = [...orderItems];
    values.push({ beer_id: "", quantity: "" });
    setOrderItems(values);
  };

  const handleRemoveFields = (index) => {
    const values = [...orderItems];
    values.splice(index, 1);
    setOrderItems(values);
  };

  return (
    <>
      <nav>
        <ul>
          <li>
            <a href="/">Login</a>
          </li>
          <li>
            <a href="/list">Liste des bières</a>
          </li>
          <li>
            <a href="/orders">Passer une commande</a>
          </li>
          <li>
            <a href="/ordersList">Liste des commandes</a>
          </li>
        </ul>
      </nav>
      <h1>Passer une commande</h1>
      <form onSubmit={handleSubmit}>
        {orderItems.map((item, index) => (
          <div key={index}>
            <select
              name="beer_id"
              value={item.beer_id}
              onChange={(event) => handleInputChange(index, event)}
            >
              <option value="" disabled>
                Select a beer
              </option>
              <optgroup label="Bieres en stock bas">
                {recommendedBeers.map((beer) => (
                  <option key={beer.id} value={beer.id}>
                    {beer.name}
                  </option>
                ))}
              </optgroup>
              <optgroup label="Toutes les bieres">
                {allBeers
                  .filter(
                    (beer) => !recommendedBeers.find((rb) => rb.id === beer.id)
                  )
                  .map((beer) => (
                    <option key={beer.id} value={beer.id}>
                      {beer.name}
                    </option>
                  ))}
              </optgroup>
            </select>
            <input
              type="text"
              name="quantity"
              value={item.quantity}
              onChange={(event) => handleInputChange(index, event)}
            />
            <button type="button" onClick={() => handleRemoveFields(index)}>
              Remove
            </button>
          </div>
        ))}
        <button type="button" onClick={handleAddFields}>
          Add More
        </button>
        <button type="submit">Submit Order</button>
      </form>
    </>
  );
};

export default OrderForm;
