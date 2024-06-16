import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Beerlist from "./components/Beerlist";
import OrderForm from "./components/OrderForm";
import OrderList from "./components/OrderList";

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
            <li>
              <a href="/ordersList">Liste des commandes</a>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" exact element={<Beerlist />} />
          <Route path="/orders" element={<OrderForm />} />
          <Route path="/ordersList" element={<OrderList />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
