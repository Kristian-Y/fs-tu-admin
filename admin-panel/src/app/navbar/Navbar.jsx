"use client";

import './navbar.css';
import Image from "next/image";

export default function Panel() {

  return ( <>
    <nav className="navbar">
        <div className="navbar-logo">
          <Image src="/logo-tus-blue-true.png" alt="logo" width={400} height={48} />
          {/* <span className="navbar-title">TUS Admin</span> */}
        </div>
        <ul className="navbar-links">
          <li><a href="/admin-panel">Home</a></li>
          <li><a href="/sponsors">Sponsors</a></li>
          <li><a href="/gallery">Gallery</a></li>
          <li><a href="#">Logout</a></li>
        </ul>
      </nav>
    </>
  );
}
