import React from "react";

const NavMenu = () => {
  const userInfoString = localStorage.getItem("user");
  const userInfo = userInfoString ? JSON.parse(userInfoString) : null;
  const isAdmin = userInfo && userInfo.role_id === 1;

  return (
    <nav>
      <ul>
        <li>
          <a href="/logout">Logout</a>
        </li>
        <li>
          <a href="/list">Liste des bières</a>
        </li>
        {isAdmin && (
          <>
            <li>
              <a href="/orders">Passer une commande</a>
            </li>
            <li>
              <a href="/ordersList">Liste des commandes</a>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default NavMenu;
