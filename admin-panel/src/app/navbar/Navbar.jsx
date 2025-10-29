"use client";

import './navbar.css';
import Image from "next/image";
import { useEffect, useState } from "react";

export default function Panel() {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`navbar ${isScrolled ? 'scrolled' : ''}`}>
      <div className="navbar-logo">
        <Image src="/logo-tus-blue-true.png" alt="logo" width={400} height={48} />
      </div>
      <ul className="navbar-links">
        <li><a href="/admin-panel">Home</a></li>
        <li><a href="/sponsors">Sponsors</a></li>
        <li><a href="/forms">Forms</a></li>
        <li><a href="#">Logout</a></li>
      </ul>
    </nav>
  );
}
