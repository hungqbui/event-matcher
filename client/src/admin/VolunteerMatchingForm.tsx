import React, { useState, useEffect } from "react";
import AdminNavbar from "./adminnavbar";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import "./VolunteerMatchingForm.css";

interface Volunteer {
  id: number;
  name: string;
  email?: string;
  phone?: string;
  skills: string | string[]; // backend may return CSV or array;
  availability: string;
}

interface Event {
  id: number;
  name: string;
  description?: string;
  requirements: string | string[];
  date: string;
  location?: string;
  max_volunteers?: number;
  current_volunteers?: number;
}

const API = "/api";

const VolunteerMatchingForm: React.FC = () => {
  const [volunteers, setVolunteers] = useState<Volunteer[]>([]);
  const [events, setEvents] = useState<Event[]>([]);
  const [selectedVol, setSelectedVol] = useState("");
  const [selectedEvt, setSelectedEvt] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [volRes, evtRes] = await Promise.all([
        fetch(`${API}/volunteers`),
        fetch(`${API}/events`),
      ]);

      if (!volRes.ok || !evtRes.ok) {
        throw new Error("Failed to load data");
      }

      const vols = await volRes.json();

      const evts = await evtRes.json();

      setVolunteers(vols);

      setEvents(evts);
    } catch (err) {
      console.error(err);

      setError("Could not connect to the server.");
    } finally {
      setLoading(false);
    }
  };

  const handleVolChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    const id = e.target.value;
    setSelectedVol(id);
    setSelectedEvt("");
    setError("");
    setSuccess("");

    if (!id) return;

    try {
      const res = await fetch(`${API}/match/find`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ volunteer_id: parseInt(id) }),
      });

      if (res.ok) {
        const data = await res.json();
        if (data.event) {
          setSelectedEvt(data.event.id.toString());
        } else {
          setError("No suitable events found.");
        }
      } else if (res.status === 404) {
        setError("No matching events found");
      }
    } catch (err) {
      console.error(err);
      setError("Error finding match.");
    }
  };

  const handleSubmit = async () => {
    if (!selectedVol || !selectedEvt) {
      setError("Select volunteer and event");
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const res = await fetch(`${API}/match`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          volunteer_id: parseInt(selectedVol),
          event_id: parseInt(selectedEvt),
        }),
      });
      const data = await res.json();
      if (res.ok) {
        const vol = volunteers.find((v) => v.id === parseInt(selectedVol));
        const evt = events.find((e) => e.id === parseInt(selectedEvt));
        setSuccess(`${vol?.name} successfully matched to ${evt?.name}!`);

        await loadData();

        setTimeout(() => {
          setSelectedVol("");
          setSelectedEvt("");
          setSuccess("");
        }, 3000);
      } else {
        setError(data.error || "Failed to create match.");
      }
    } catch (err) {
      console.error(err);
      setError("Error creating match.");
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setSelectedVol("");
    setSelectedEvt("");
    setError("");
    setSuccess("");
  };

  if (loading && volunteers.length === 0) {
    return <div className="loading">Loading...</div>;
  }

  const vol = volunteers.find((v) => v.id === parseInt(selectedVol));
  const evt = events.find((e) => e.id === parseInt(selectedEvt));

  const formatList = (value: string | string[]) => {
    if (Array.isArray(value)) return value.join(", ");
    return value;
  };

  if (loading && volunteers.length === 0) {
    return <div className="loading">Loading volunteers and events...</div>;
  }

  return (
    <>
    <Navbar /> 
    <AdminNavbar />
    <div className="form-container">
      <h2>Volunteer Matching Form</h2>

      {error && (
        <div
          style={{
            background: "#fee",
            border: "1px solid #fcc",
            color: "#c00",
            padding: "10px",
            borderRadius: "5px",
            marginBottom: "15px",
          }}
        >
          {error}
        </div>
      )}

      {success && (
        <div
          style={{
            background: "#efe",
            border: "1px solid #cfc",
            color: "#060",
            padding: "10px",
            borderRadius: "5px",
            marginBottom: "15px",
          }}
        >
          {success}
        </div>
      )}

      <div className="matching-form">
        <div className="form-group">
          <label htmlFor="vol-select">Volunteer:</label>
          <select
            id="vol-select"
            value={selectedVol}
            onChange={handleVolChange}
            className="form-select"
            disabled={loading}
          >
            <option value="">Select volunteer...</option>
            {volunteers.map((v) => (
              <option key={v.id} value={v.id}>
                {v.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="evt-select">Event:</label>
          <select
            id="evt-select"
            value={selectedEvt}
            onChange={(e) => setSelectedEvt(e.target.value)}
            className="form-select"
            disabled={loading}
          >
            <option value="">Select event...</option>
            {events.map((e) => (
              <option key={e.id} value={e.id}>
                {e.name} - {e.date}{" "}
                {e.max_volunteers && e.current_volunteers !== undefined
                  ? `(${e.current_volunteers}/${e.max_volunteers})`
                  : ""}
              </option>
            ))}
          </select>
        </div>

        {vol && (
          <div className="volunteer-info">
            <h3>Volunteer Details:</h3>
            <div className="info-card">
              <p>
                <strong>Name:</strong> {vol.name}
              </p>
              {vol.email && (
                <p>
                  <strong>Email:</strong> {vol.email}
                </p>
              )}
              {vol.phone && (
                <p>
                  <strong>Phone:</strong> {vol.phone}
                </p>
              )}
              <p>
                <strong>Skills:</strong> {formatList(vol.skills)}
              </p>
              <p>
                <strong>Availability:</strong> {vol.availability}
              </p>
            </div>
          </div>
        )}

        {evt && (
          <div className="event-info">
            <h3>Event Details:</h3>
            <div className="info-card">
              <p>
                <strong>Event:</strong> {evt.name}
              </p>
              {evt.description && (
                <p>
                  <strong>Description:</strong> {evt.description}
                </p>
              )}
              <p>
                <strong>Date:</strong> {evt.date}
              </p>
              {evt.location && (
                <p>
                  <strong>Location:</strong> {evt.location}
                </p>
              )}
              <p>
                <strong>Requirements:</strong> {formatList(evt.requirements)}
              </p>
              {evt.max_volunteers && (
                <p>
                  <strong>Volunteers:</strong> {evt.current_volunteers ?? 0}/
                  {evt.max_volunteers}
                </p>
              )}
            </div>
          </div>
        )}

        <div className="form-actions">
          <button
            type="button"
            className="submit-btn"
            onClick={handleSubmit}
            disabled={loading || !selectedVol || !selectedEvt}
          >
            {loading ? "Matching..." : "Match Volunteer"}
          </button>
          <button
            type="button"
            className="reset-btn"
            onClick={reset}
            disabled={loading}
          >
            Reset
          </button>
        </div>
      </div>
    </div>
    <Footer />
    </>
  );
};

export default VolunteerMatchingForm;
