"use client";
import "./login.css";
import Image from "next/image";
import { useState } from "react";
import { useAuth } from "../../context/AuthContext";

export default function Login() {
  const { handleLogin, user } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handelLogin = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      setError("Please enter both username and password.");
      return;
    }

    try {
      const res = await handleLogin(username, password);
      window.location.href = '/admin-panel';
    } catch (err) {
      setError("Login failed. Please try again.");
    }
  };
  return (
    <>
      <main>
          <div className="welcome">
            <Image src={"/logo-tus-white.png"} alt="logo" width={350} height={74}/>
            <h1>TUS Admin Panel</h1>
          </div>
        <form action="login" onSubmit={handelLogin} className="login-form">
          <h2>Login</h2>
          <div className="input">
            <label htmlFor="name">Username: </label>
            <input type="text" placeholder="Username" onChange={e => setUsername(e.target.value)}/>
          </div>
          <div className="input">
            <label htmlFor="password">Password: </label>
            <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)}/>
          </div>
          <button type="submit">Login</button>
          {error && <p style={{color: 'red'}}>{error}</p>}
        </form>
      </main>
    </>
  );
}