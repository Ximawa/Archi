import React, { useEffect, useState } from "react";
import axios from "axios";

const BeerList = () => {
  const [beers, setBeers] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/beers")
      .then((response) => setBeers(response.data))
      .catch((error) =>
        console.error("There was an error fetching the beers!", error)
      );
  }, []);

  return (
    <div>
      <h1>Beer List</h1>
      <ul>
        {beers.map((beer) => (
          <li key={beer.id}>
            {beer.name}: {beer.stock}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BeerList;
