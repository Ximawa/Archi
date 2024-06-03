import React from "react";
import "./App.css";
import BeerList from "./components/Beerlist";
import NewBeerForm from "./components/NewBeerForm";
import RecommendBeers from "./components/RecommendBeers";

function App() {
  return (
    <div className="App">
      <NewBeerForm />
      <BeerList />
      <RecommendBeers />
    </div>
  );
}

export default App;
