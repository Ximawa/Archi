import React, { useState } from "react";
import axios from "axios";

const NewBeerForm = () => {
  const [name, setName] = useState("");
  const [stock, setStock] = useState("");
  const [minStock, setMinStock] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    axios
      .post("http://localhost:8000/beers", {
        name,
        stock: parseInt(stock),
        min_stock: parseInt(minStock),
      })
      .then((response) => {
        setName("");
        setStock("");
        setMinStock("");
        window.location.reload(); // Recharge la page pour afficher la nouvelle bière
      })
      .catch((error) =>
        console.error("There was an error creating the beer!", error)
      );
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>
      <div>
        <label>Stock</label>
        <input
          type="number"
          value={stock}
          onChange={(e) => setStock(e.target.value)}
        />
      </div>
      <div>
        <label>Min Stock</label>
        <input
          type="number"
          value={minStock}
          onChange={(e) => setMinStock(e.target.value)}
        />
      </div>
      <button type="submit">Add Beer</button>
    </form>
  );
};

export default NewBeerForm;
