import React, { useState, useEffect } from "react";
import "./VolunteerMatchingForm.css";

// Define interfaces for better type safety
interface Volunteer {
  id: number;
  name: string;
  skills: string[];
  availability: string;
}

interface Event {
  id: number;
  name: string;
  requirements: string[];
  date: string;
}

// Mock data - in real app this would come from API
const mockVolunteers: Volunteer[] = [
  {
    id: 1,
    name: "John Doe",
    skills: ["tree planting"],
    availability: "weekends",
  },
  {
    id: 2,
    name: "Jane Smith",
    skills: ["disaster relief"],
    availability: "weekdays",
  },
  {
    id: 3,
    name: "Joe Doe",
    skills: ["youth mentors"],
    availability: "evenings",
  },
  {
    id: 4,
    name: "Jim Doe",
    skills: ["food drives"],
    availability: "flexible",
  },
];

const mockEvents: Event[] = [
  {
    id: 1,
    name: "Food Bank Distribution",
    requirements: ["food drives"],
    date: "10/15/2025",
  },
  {
    id: 2,
    name: "Community Garden Build",
    requirements: ["tree planting"],
    date: "10/20/2025",
  },
  {
    id: 3,
    name: "Hurricane Relief Effort",
    requirements: ["disaster relief"],
    date: "10/25/2025",
  },
  {
    id: 4,
    name: "Youth Mentorship Program",
    requirements: ["youth mentors"],
    date: "10/30/2025",
  },
];

const VolunteerMatchingForm: React.FC = () => {
  const [volunteers, setVolunteers] = useState<Volunteer[]>([]);
  const [events, setEvents] = useState<Event[]>([]);
  const [selectedVolunteer, setSelectedVolunteer] = useState("");
  const [matchedEvent, setMatchedEvent] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Simulate API call
    setLoading(true);
    setTimeout(() => {
      setVolunteers(mockVolunteers);
      setEvents(mockEvents);
      setLoading(false);
    }, 1000);
  }, []);

  const handleVolunteerChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const volunteerId = e.target.value;
    setSelectedVolunteer(volunteerId);

    if (volunteerId) {
      // Auto-match event based on volunteer's skills
      const volunteer = volunteers.find(
        (v: Volunteer) => v.id === parseInt(volunteerId)
      );
      if (volunteer) {
        const bestMatch = events.find((event: Event) =>
          event.requirements.some((req: string) =>
            volunteer.skills.includes(req)
          )
        );
        setMatchedEvent(bestMatch ? bestMatch.id.toString() : "");
      }
    } else {
      setMatchedEvent("");
    }
  };

  const handleSubmit = () => {
    if (!selectedVolunteer || !matchedEvent) {
      alert("Please select both a volunteer and an event");
      return;
    }

    const volunteer = volunteers.find(
      (v: Volunteer) => v.id === parseInt(selectedVolunteer)
    );
    const event = events.find((e: Event) => e.id === parseInt(matchedEvent));

    if (volunteer && event) {
      alert(`Successfully matched ${volunteer.name} to ${event.name}!`);
    }

    // Reset form
    setSelectedVolunteer("");
    setMatchedEvent("");
  };

  if (loading) {
    return <div className="loading">Loading volunteers and events...</div>;
  }

  return (
    <div className="form-container">
      <h2>Volunteer Matching Form</h2>
      <div className="matching-form">
        <div className="form-group">
          <label htmlFor="volunteer-select">Volunteer Name:</label>
          <select
            id="volunteer-select"
            value={selectedVolunteer}
            onChange={handleVolunteerChange}
            className="form-select"
          >
            <option value="">Select a volunteer...</option>
            {volunteers.map((volunteer: Volunteer) => (
              <option key={volunteer.id} value={volunteer.id}>
                {volunteer.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="event-select">Matched Event:</label>
          <select
            id="event-select"
            value={matchedEvent}
            onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
              setMatchedEvent(e.target.value)
            }
            className="form-select"
          >
            <option value="">Select an event...</option>
            {events.map((event: Event) => (
              <option key={event.id} value={event.id}>
                {event.name} - {event.date}
              </option>
            ))}
          </select>
        </div>

        {selectedVolunteer && (
          <div className="volunteer-info">
            <h3>Volunteer Details:</h3>
            {volunteers
              .filter((v: Volunteer) => v.id === parseInt(selectedVolunteer))
              .map((volunteer: Volunteer) => (
                <div key={volunteer.id} className="info-card">
                  <p>
                    <strong>Name:</strong> {volunteer.name}
                  </p>
                  <p>
                    <strong>Skills:</strong> {volunteer.skills.join(", ")}
                  </p>
                  <p>
                    <strong>Availability:</strong> {volunteer.availability}
                  </p>
                </div>
              ))}
          </div>
        )}

        {matchedEvent && (
          <div className="event-info">
            <h3>Event Details:</h3>
            {events
              .filter((e: Event) => e.id === parseInt(matchedEvent))
              .map((event: Event) => (
                <div key={event.id} className="info-card">
                  <p>
                    <strong>Event:</strong> {event.name}
                  </p>
                  <p>
                    <strong>Date:</strong> {event.date}
                  </p>
                  <p>
                    <strong>Requirements:</strong>{" "}
                    {event.requirements.join(", ")}
                  </p>
                </div>
              ))}
          </div>
        )}

        <div className="form-actions">
          <button type="button" className="submit-btn" onClick={handleSubmit}>
            Match Volunteer to Event
          </button>
          <button
            type="button"
            className="reset-btn"
            onClick={() => {
              setSelectedVolunteer("");
              setMatchedEvent("");
            }}
          >
            Reset Form
          </button>
        </div>
      </div>
    </div>
  );
};

export default VolunteerMatchingForm;
