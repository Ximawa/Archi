import React, { useState, useEffect } from "react";

function OrderForm() {
  const [beers, setBeers] = useState([]);
  const [recommendedBeers, setRecommendedBeers] = useState([]);
  const [orderData, setOrderData] = useState([]);

  useEffect(() => {
    fetchAllBeers();
    fetchRecommendedBeers();
  }, []);

  const fetchAllBeers = async () => {
    try {
      const response = await fetch("http://localhost:8000/beers");
      const data = await response.json();
      setBeers(data);
    } catch (error) {
      console.error("Failed to fetch beers:", error);
    }
  };

  const fetchRecommendedBeers = async () => {
    try {
      const response = await fetch("http://localhost:8000/beers/low_stock");
      const data = await response.json();
      setRecommendedBeers(data);
    } catch (error) {
      console.error("Failed to fetch recommended beers:", error);
    }
  };

  const addBeerToOrder = (selectedBeer) => {
    const existingOrderIndex = orderData.findIndex(
      (order) => order.beerId === selectedBeer.id
    );
    if (existingOrderIndex === -1) {
      setOrderData([...orderData, { beerId: selectedBeer.id, quantity: 1 }]);
    } else {
      // Optionally handle case where beer is already in the order
    }
  };

  const updateBeerQuantity = (beerId, quantity) => {
    setOrderData(
      orderData.map((order) => {
        if (order.beerId === beerId) {
          return { ...order, quantity: quantity };
        }
        return order;
      })
    );
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log("Submitting order:", JSON.stringify(orderData));
    const submitOrder = async () => {
      try {
        const response = await fetch("http://localhost:8000/orders", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            orders: orderData.map((order) => ({
              beerId: order.beerId,
              quantity: order.quantity,
            })),
          }),
        });
        if (response.ok) {
          console.log("Order submitted successfully");
          // Optionally reset the order data
          setOrderData([]);
        } else {
          console.error("Failed to submit order");
        }
      } catch (error) {
        console.error("Failed to submit order:", error);
      }
    };

    submitOrder();
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Recommended Beer:</label>
        {recommendedBeers.map((beer, index) => (
          <button
            key={index}
            type="button"
            onClick={() => addBeerToOrder(beer)}
          >
            {beer.name}
          </button>
        ))}
      </div>
      <div>
        <label>All Beers:</label>
        {beers.map((beer, index) => (
          <button
            key={index}
            type="button"
            onClick={() => addBeerToOrder(beer)}
          >
            {beer.name}
          </button>
        ))}
      </div>
      {orderData.length > 0 && (
        <div>
          <h3>Order Details:</h3>
          {orderData.map((order, index) => (
            <div key={index}>
              <span>{order.beerName} - Quantity: </span>
              <input
                type="number"
                value={order.quantity}
                onChange={(e) =>
                  updateBeerQuantity(order.beerName, parseInt(e.target.value))
                }
                min="1"
              />
            </div>
          ))}
        </div>
      )}
      <button type="submit">Submit Order</button>
    </form>
  );
}

export default OrderForm;
