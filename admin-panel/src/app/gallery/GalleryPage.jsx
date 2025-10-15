"use client";

import './gallery.css';
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import axiosInstance from "@/lib/axiosInstance";
import Loading from '@/app/loading/Loading';

export default function GalleryPage() {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [years, setYears] = useState([]);
  const [openYear, setOpenYear] = useState(null);
  const [newYear, setNewYear] = useState("");
  const [uploadFiles, setUploadFiles] = useState({});
  const [error, setError] = useState("");
  const [addingYear, setAddingYear] = useState(false);

  useEffect(() => {
    if (!loading && !user) router.push("/");
  }, [loading, user, router]);

  useEffect(() => {
    async function fetchGallery() {
      try {
        const res = await axiosInstance.get("photos/years-with-photos");
        console.log(res.data);
        setYears(res.data); // [{id, year, photos:[{id, image}], ...}]
      } catch {
        setError("Could not load gallery.");
      }
    }
    fetchGallery();
  }, []);

  async function handleAddYear(e) {
    e.preventDefault();
    setAddingYear(true);
    setError("");
    try {
      const res = await axiosInstance.post("photos/years/", { year: newYear });
      setYears([...years, { ...res.data, photos: [] }]);
      setNewYear("");
    } catch {
      setError("Error adding year.");
    }
    setAddingYear(false);
  }

  async function handleDeleteYear(id) {
    if (!confirm("Delete this year and all its photos?")) return;
    try {
      await axiosInstance.delete(`photos/years/${id}/`);
      setYears(years.filter(y => y.id !== id));
      if (openYear === id) setOpenYear(null);
    } catch {
      setError("Error deleting year.");
    }
  }

  function handleFileChange(yearId, files) {
    setUploadFiles({ ...uploadFiles, [yearId]: files });
  }

  async function handleUploadPhotos(yearId) {
    if (!uploadFiles[yearId] || uploadFiles[yearId].length === 0) return;
    const formData = new FormData();
    Array.from(uploadFiles[yearId]).forEach(file => formData.append("images", file));
    try {
      const res = await axiosInstance.post(`photos/team-photos/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setYears(years.map(y => y.id === yearId ? { ...y, photos: [...y.photos, ...res.data] } : y));
      setUploadFiles({ ...uploadFiles, [yearId]: null });
    } catch {
      setError("Error uploading photos.");
    }
  }

  async function handleDeletePhoto(yearId, photoId) {
    try {
      await axiosInstance.delete(`gallery/photos/${photoId}/`);
      setYears(years.map(y => y.id === yearId ? { ...y, photos: y.photos.filter(p => p.id !== photoId) } : y));
    } catch {
      setError("Error deleting photo.");
    }
  }

  if (loading || !user) return <Loading />;

  return (
    <div className="gallery-page">
      <h2>Team Gallery</h2>
      {error && <div className="error">{error}</div>}
      <form className="add-year-form" onSubmit={handleAddYear}>
        <input
          type="number"
          placeholder="Add year (e.g. 2024)"
          value={newYear}
          onChange={e => setNewYear(e.target.value)}
          required
        />
        <button type="submit" disabled={addingYear}>
          {addingYear ? "Adding..." : "Add Year"}
        </button>
      </form>
      {years.length === 0 ? (
        <p>No years found.</p>
      ) : (
        years.sort((a, b) => b.year - a.year).map(y => (
          <div key={y.id} className="gallery-year-block">
            <div className="gallery-year-header" onClick={() => setOpenYear(openYear === y.id ? null : y.id)}>
              <h3>{y.year}</h3>
              <button className="delete-year-btn" onClick={e => { e.stopPropagation(); handleDeleteYear(y.id); }}>🗑️</button>
            </div>
            {openYear === y.id && (
              <div className="gallery-year-content">
                <div className="gallery-photos">
                  {y.photos.length === 0 ? <p>No photos.</p> : y.photos.map(photo => (
                    <div key={photo.id} className="gallery-photo-wrapper">
                      <img src={photo.image} alt={`Team photo ${y.year}`} className="gallery-photo" />
                      <button
                        className="delete-photo-btn"
                        title="Delete photo"
                        onClick={() => handleDeletePhoto(y.id, photo.id)}
                      >✖</button>
                    </div>
                  ))}
                </div>
                <div className="upload-block">
                  <label className="file-label">
                    Upload Photos
                    <input
                      type="file"
                      multiple
                      accept="image/*"
                      onChange={e => handleFileChange(y.id, e.target.files)}
                      style={{ display: "none" }}
                    />
                  </label>
                  <button
                    className="upload-btn"
                    onClick={() => handleUploadPhotos(y.id)}
                    disabled={!uploadFiles[y.id] || uploadFiles[y.id].length === 0}
                  >
                    Upload
                  </button>
                  <span className="selected-file-name">
                    {uploadFiles[y.id] && Array.from(uploadFiles[y.id]).map(f => f.name).join(", ")}
                  </span>
                </div>
              </div>
            )}
          </div>
        ))
      )}
    </div>
  );
}
