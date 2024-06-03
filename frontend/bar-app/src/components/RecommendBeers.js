import React, { useEffect, useState } from "react";
import axios from "axios";

const RecommendBeers = () => {
  const [beers, setBeers] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/beers/recommend")
      .then((response) => setBeers(response.data))
      .catch((error) =>
        console.error(
          "There was an error fetching the recommended beers!",
          error
        )
      );
  }, []);

  return (
    <div>
      <h1>Recommended Beers</h1>
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

export default RecommendBeers;
