import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Beerlist from "./components/Beerlist";
import OrderPage from "./components/OrderPage";
import OrderForm from "./components/OrderForm";

const App = () => {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <a href="/">Liste des bières</a>
            </li>
            <li>
              <a href="/orders">Passer une commande</a>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" exact element={<Beerlist />} />
          <Route path="/orders" element={<OrderForm />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
