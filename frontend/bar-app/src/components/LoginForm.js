import React, { useState } from "react";

const LoginForm = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    // Make API call to validate username and password
    // Assuming the API call returns user information in the response
    fetch("http://localhost:8000/users/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) {
          window.alert("Mauvais identifiants");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Response data:", data); // Log the full response data
        if (data.success) {
          data = JSON.stringify(data.user);
          console.log("User data:", data); // Log the user data
          localStorage.setItem("user", data);
          window.location.href = "/list";
        }
      })
      .catch((error) => {
        console.error("There was a problem with your fetch operation:", error);
      });
    // Reset form fields
    setUsername("");
    setPassword("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="username">Username:</label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={handleUsernameChange}
        />
      </div>
      <div>
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={handlePasswordChange}
        />
      </div>
      <button type="submit">Login</button>
    </form>
  );
};

export default LoginForm;
