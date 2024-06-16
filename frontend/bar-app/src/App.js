import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Beerlist from "./components/Beerlist";
import OrderForm from "./components/OrderForm";
import LoginForm from "./components/LoginForm";
import OrderList from "./components/OrderList";
import Logout from "./components/Logout"; // Corrected file name

const App = () => {
  const userInfoString = localStorage.getItem("user");
  var userInfo = userInfoString ? JSON.parse(userInfoString) : null;
  if (userInfo != null && userInfo.detail === "User not found") {
    localStorage.clear();
    userInfo = null;
    window.location.href = "/";
  }
  const isAdmin = userInfo && userInfo.role_id === 1;

  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<LoginForm />} />
          <Route path="/logout" element={<Logout />} />
          {userInfo ? (
            <>
              <Route path="/list" exact element={<Beerlist />} />
              {isAdmin ? (
                <>
                  <Route path="/orders" element={<OrderForm />} />
                  <Route path="/ordersList" element={<OrderList />} />
                </>
              ) : (
                <Route
                  path="*"
                  element={
                    <h1>
                      Vous n'avez pas les droits pour accéder à cette page
                    </h1>
                  }
                />
              )}
            </>
          ) : (
            <>
              <Route
                path="*"
                element={
                  <>
                    <h1>Vous devez vous connecter pour accéder à cette page</h1>
                    <a href="/">Connectez vous</a>
                  </>
                }
              />
            </>
          )}
        </Routes>
      </div>
    </Router>
  );
};
export default App;
