"use client";

import './panel.css';
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import Image from "next/image";

export default function Panel() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push("/");
    }
  }, [loading, user]);

  if (loading || !user) return <p>Loading...</p>;

  return ( <>

    <div className="dashboard-container">

      <div className="welcome-block">
        <h1>TUS Admin Panel</h1>
        <h2>Welcome, {user.username}!</h2>
        <p className="welcome-desc">This is your dashboard. Use the navigation bar to explore Home, Sponsors, and Gallery.</p>
      </div>
    </div></>
  );
}
