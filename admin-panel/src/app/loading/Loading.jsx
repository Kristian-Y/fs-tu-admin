"use client";

import './loading.css';

export default function Loading() {
  return (
    <div className="loading-container">
      <div className="loading-svg">
        <svg width="80" height="80" viewBox="0 0 80 80">
          <circle
            cx="40"
            cy="40"
            r="32"
            stroke="#3a5aff"
            strokeWidth="8"
            fill="none"
            strokeDasharray="180"
            strokeDashoffset="60"
            style={{ animation: "spin 1.2s linear infinite" }}
          />
          <circle
            cx="40"
            cy="40"
            r="16"
            fill="#3a5aff"
            style={{ opacity: 0.15 }}
          />
        </svg>
      </div>
      <div className="loading-text">
        Preparing magic...
        <span className="loading-dots">
          <span>.</span>
          <span>.</span>
          <span>.</span>
        </span>
      </div>
    </div>
  );
}