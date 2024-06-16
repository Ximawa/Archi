import React from "react";

const Logout = () => {
  // Clear local storage
  localStorage.clear();

  // Redirect to the home page
  window.location.href = "/";
  return <div></div>;
};

export default Logout;
