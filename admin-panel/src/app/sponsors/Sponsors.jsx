"use client";

import './sponsors.css';
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import Image from "next/image";


import { useState } from "react";
import axiosInstance from "@/lib/axiosInstance";

export default function Sponsors() {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [sponsors, setSponsors] = useState([]);
  const [name, setName] = useState("");
  const [link, setLink] = useState("");
  const [logo, setLogo] = useState(null);
  const [adding, setAdding] = useState(false);
  const [error, setError] = useState("");
  const [preview, setPreview] = useState(null);

  useEffect(() => {
    if (!loading && !user) {
      router.push("/");
    }
  }, [loading, user]);

  useEffect(() => {
    async function fetchSponsors() {
      try {
        const res = await axiosInstance.get("sponsors/");
        setSponsors(res.data);
        console.log(res.data);
      } catch (err) {
        setError("Could not load sponsors.");
      }
    }
    fetchSponsors();
  }, []);

  function handleLogoChange(e) {
    const file = e.target.files[0];
    setLogo(file);
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    } else {
      setPreview(null);
    }
  }

  async function handleAddSponsor(e) {
    e.preventDefault();
    setAdding(true);
    setError("");
    const formData = new FormData();
    formData.append("name", name);
    formData.append("link", link);
    if (logo) formData.append("logo", logo);
    try {
      const res = await axiosInstance.post("sponsors/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSponsors([...sponsors, res.data]);
      setName("");
      setLink("");
      setLogo(null);
      setPreview(null);
    } catch (err) {
      setError("Error adding sponsor.");
    }
    setAdding(false);
  }

  async function handleDeleteSponsor(id) {
    if (!confirm("Are you sure you want to delete this sponsor?")) return;
    try {
      await axiosInstance.delete(`sponsors/${id}/`);
      setSponsors(sponsors.filter((s) => s.id !== id));
    } catch (err) {
      setError("Error deleting sponsor.");
    }
  }


  if (loading || !user) return <p>Loading...</p>;


  return (
    <div className="sponsors-page">
      <h2>All Sponsors</h2>
      {error && <div className="error">{error}</div>}
      {console.log(sponsors)}
 
      <ul className="sponsor-list">
        {sponsors.length == 0 ? <li>No sponsors found.</li> : sponsors.map((s) => (
          <li key={s.id} className="sponsor-item">
            {s.logo && (
              <img src={s.logo} alt={s.name} className="sponsor-logo" />
            )}
            <div className="sponsor-info">
              <span className="sponsor-name">{s.name}</span>
              {s.link && (
                <a href={s.link} target="_blank" rel="noopener noreferrer" className="sponsor-link">Visit</a>
              )}
              <button onClick={() => handleDeleteSponsor(s.id)} className='sponsor-delete'>Delete</button>
            </div>
          </li>
        ))}
      </ul>
      <form className="add-sponsor-form" onSubmit={handleAddSponsor}>
        <h3>Add New Sponsor</h3>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="url"
          placeholder="Link (optional)"
          value={link}
          onChange={(e) => setLink(e.target.value)}
        />
        <div className="file">
          <label className="file-label">
            Choose Logo
            <input
              type="file"
              accept="image/*"
              onChange={handleLogoChange}
              style={{ display: "none" }}
            />
          </label>
          <span className="selected-file-name">
            {logo ? logo.name : ""}
          </span>
        </div>
        {preview && (
          <div className="preview-block">
            <span>Preview:</span>
            <img src={preview} alt="Preview" className="preview-img" />
          </div>
        )}
        <button type="submit" disabled={adding}>
          {adding ? "Adding..." : "Add Sponsor"}
        </button>
      </form>
    </div>
  );
}
