import React, { useState, useEffect } from "react";

const OrderList = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/orders/all")
      .then((response) => response.json())
      .then((data) => setOrders(data))
      .catch((error) => console.error("Error fetching orders:", error));
  }, []);

  return (
    <div>
      <h2>Order List</h2>
      <ul>
        {orders.map((order) => (
          <li key={order.id}>
            <a
              href={`http://127.0.0.1:8000/order-pdf/${order.id}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              Commande : {order.id} du{" "}
              {new Date(order.created_at).toLocaleDateString()}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default OrderList;
