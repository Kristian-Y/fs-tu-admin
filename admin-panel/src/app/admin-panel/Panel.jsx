"use client";

import './panel.css';
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function Panel() {
  const { user, loading } = useAuth();
  const [timeRange, setTimeRange] = useState('30');
  const [activeTab, setActiveTab] = useState('views');
  const router = useRouter();

  const sampleData = [
    { date: "2025-09-30", views: 120 },
    { date: "2025-10-01", views: 98 },
    { date: "2025-10-02", views: 134 },
    { date: "2025-10-03", views: 167 },
    { date: "2025-10-04", views: 145 },
    { date: "2025-10-05", views: 190 },
    { date: "2025-10-06", views: 210 },
    { date: "2025-10-07", views: 156 },
    { date: "2025-10-08", views: 173 },
    { date: "2025-10-09", views: 189 },
    { date: "2025-10-10", views: 202 },
    { date: "2025-10-11", views: 250 },
    { date: "2025-10-12", views: 230 },
    { date: "2025-10-13", views: 210 },
    { date: "2025-10-14", views: 270 },
    { date: "2025-10-15", views: 295 },
    { date: "2025-10-16", views: 310 },
    { date: "2025-10-17", views: 280 },
    { date: "2025-10-18", views: 260 },
    { date: "2025-10-19", views: 240 },
    { date: "2025-10-20", views: 300 },
    { date: "2025-10-21", views: 340 },
    { date: "2025-10-22", views: 390 },
    { date: "2025-10-23", views: 370 },
    { date: "2025-10-24", views: 410 },
    { date: "2025-10-25", views: 420 },
    { date: "2025-10-26", views: 450 },
    { date: "2025-10-27", views: 470 },
    { date: "2025-10-28", views: 490 },
    { date: "2025-10-29", views: 512 },
  ];

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!loading && !user) {
      router.push("/");
    }
  }, [loading, user]);

  useEffect(() => {
    const welcomeBlock = document.querySelector('.welcome-block');
    if (!welcomeBlock) return;

    const handleMouseMove = (e) => {
      const rect = welcomeBlock.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / welcomeBlock.clientWidth) * 100;
      const y = ((e.clientY - rect.top) / welcomeBlock.clientHeight) * 100;
      welcomeBlock.style.setProperty('--x', `${x}%`);
      welcomeBlock.style.setProperty('--y', `${y}%`);
    };

    welcomeBlock.addEventListener('mousemove', handleMouseMove);
    return () => welcomeBlock.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const chartData = {
    labels: sampleData.map(v => v.date),
    datasets: [
      {
        label: `Посещения (последни ${timeRange} дни)`,
        data: sampleData.map(v => v.views),
        borderColor: "#3380FF",
        backgroundColor: "rgba(51, 128, 255, 0.1)",
        fill: true,
        tension: 0.3,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#E5E5E5'
        }
      }
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(229, 229, 229, 0.1)'
        },
        ticks: {
          color: '#E5E5E5'
        }
      },
      y: {
        grid: {
          color: 'rgba(229, 229, 229, 0.1)'
        },
        ticks: {
          color: '#E5E5E5'
        }
      }
    }
  };

  if (loading || !user) return <div className="loading">Loading...</div>;

  return (
    <div className="dashboard-container">
      <div className="welcome-block">
        <div className="welcome-content">
          <h1>TUS Admin Panel</h1>
          <p className="welcome-desc">Welcome back, {user.username}! Here's what's happening with your site.</p>
        </div>
        <div className="welcome-stats">
          <div className="welcome-stat">
            <span className="welcome-stat-label">Last login</span>
            <span className="welcome-stat-value">Today, 10:45 AM</span>
          </div>
          <div className="welcome-stat">
            <span className="welcome-stat-label">Session</span>
            <span className="welcome-stat-value">2h 15m</span>
          </div>
        </div>
      </div>
      
      <section className='stats'>
        <div className="stats-header">
          <div className="stats-tabs">
            <button 
              className={`tab ${activeTab === 'views' ? 'active' : ''}`}
              onClick={() => setActiveTab('views')}
            >
              Views
            </button>
            
          </div>
          <div className="time-range">
            <select 
              value={timeRange} 
              onChange={(e) => setTimeRange(e.target.value)}
            >
              <option value="7">Last 7 days</option>
              <option value="30">Last 30 days</option>
              <option value="90">Last 90 days</option>
            </select>
          </div>
        </div>

        <div className='stat-cards'>
          <div className='stat-card'>
            <h3>Total Views</h3>
            <p className="stat-number">1,234</p>
            <span className="stat-change positive">+12.5%</span>
          </div>
          <div className='stat-card'>
            <h3>New Views (last 30 days)</h3>
            <p className="stat-number">456</p>
            <span className="stat-change negative">-2.3%</span>
          </div>
          <div className='stat-card'>
            <h3>Total Photos</h3>
            <p className="stat-number">89</p>
          </div>
        </div>

        <div className='chart-container'>
          <Line data={chartData} options={chartOptions} />
        </div>
      </section>
    </div>
  );
}
