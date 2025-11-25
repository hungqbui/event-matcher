import { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import "./EventView.css";

interface Event {
  id: number;
  name: string;
  description: string;
  date: string;
  time_label: string;
  location: string;
  urgency: string;
  max_volunteers: number;
  current_volunteers: number;
  img?: string;
  required_skills: string[];
  skill_match_count?: number;
  matching_skills?: string[];
  is_skill_match?: boolean;
  is_registered?: boolean;
}

export default function EventView() {
  const { user } = useAuth();
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | "matched">("all");
  const [timeFilter, setTimeFilter] = useState<"upcoming" | "past">("upcoming");
  const [registering, setRegistering] = useState<number | null>(null);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        console.log(user)

        const url = user?.id 
          ? `/api/volunteer_user/events/upcoming?user_id=${user.id}`
          : `/api/volunteer_user/events/upcoming`;
        
        const response = await fetch(url);
        if (response.ok) {
          const data = await response.json();
          setEvents(data);
        }
      } catch (err) {
        console.error("Error fetching events:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, [user?.id]);

  const handleRegister = async (eventId: number) => {
    if (!user?.id) {
      alert("Please log in to register for events");
      return;
    }

    const event = events.find(e => e.id === eventId);
    const isUnregistering = event?.is_registered;

    setRegistering(eventId);
    try {
      if (isUnregistering) {
        // Find the volunteer_id first
        const volunteerResponse = await fetch(`http://127.0.0.1:5000/api/volunteers`);
        if (!volunteerResponse.ok) {
          throw new Error("Failed to fetch volunteer data");
        }
        const volunteers = await volunteerResponse.json();
        const currentVolunteer = volunteers.find((v: any) => v.user_id === user.id);
        
        if (!currentVolunteer) {
          alert("Volunteer profile not found");
          return;
        }

        // Find the match and delete it
        const matchResponse = await fetch(`http://127.0.0.1:5000/api/matches/event/${eventId}`);
        if (matchResponse.ok) {
          const matches = await matchResponse.json();
          const userMatch = matches.find((m: any) => m.volunteer_id === currentVolunteer.id);
          
          if (userMatch) {
            const deleteResponse = await fetch(`http://127.0.0.1:5000/api/matches/${userMatch.id}`, {
              method: "DELETE",
            });
            
            if (deleteResponse.ok) {
              alert("Successfully unregistered from the event!");
              // Update local state
              setEvents(events.map(e => 
                e.id === eventId ? { ...e, is_registered: false, current_volunteers: e.current_volunteers - 1 } : e
              ));
            } else {
              const error = await deleteResponse.json();
              alert(error.error || error.message || "Failed to unregister from event");
            }
          }
        }
      } else {
        // Register for event
        const response = await fetch("http://127.0.0.1:5000/api/register-event", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_id: user.id,
            event_id: eventId,
          }),
        });

        if (response.ok) {
          alert("Successfully registered for the event!");
          // Update local state
          setEvents(events.map(e => 
            e.id === eventId ? { ...e, is_registered: true, current_volunteers: e.current_volunteers + 1 } : e
          ));
        } else {
          const error = await response.json();
          alert(error.error || error.message || "Failed to register for event");
        }
      }
    } catch (err) {
      console.error("Error with event registration:", err);
      alert("Failed to process request. Please try again.");
    } finally {
      setRegistering(null);
    }
  };

  const getUrgencyClass = (urgency: string) => {
    switch (urgency) {
      case "high": return "urgency-high";
      case "medium": return "urgency-medium";
      case "low": return "urgency-low";
      default: return "";
    }
  };

  const isEventPast = (dateStr: string) => {
    const eventDate = new Date(dateStr);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return eventDate < today;
  };

  const timeFilteredEvents = events.filter(e => 
    timeFilter === "past" ? isEventPast(e.time_label) : !isEventPast(e.time_label)
  );

  const filteredEvents = filter === "matched" 
    ? timeFilteredEvents.filter(e => e.is_skill_match)
    : timeFilteredEvents;

  const upcomingCount = events.filter(e => !isEventPast(e.time_label)).length;
  const pastCount = events.filter(e => isEventPast(e.time_label)).length;

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="event-view-page">
          <h1>Loading events...</h1>
        </div>
        <Footer />
      </>
    );
  }

  return (
    <>
      <Navbar />
      <div className="event-view-page">
        <div className="event-view-header">
          <h1>Volunteer Events</h1>
          
          <div className="time-filter-buttons">
            <button
              className={`time-filter-btn ${timeFilter === "upcoming" ? "active" : ""}`}
              onClick={() => setTimeFilter("upcoming")}
            >
              Upcoming ({upcomingCount})
            </button>
            <button
              className={`time-filter-btn ${timeFilter === "past" ? "active" : ""}`}
              onClick={() => setTimeFilter("past")}
            >
              Past Events ({pastCount})
            </button>
          </div>

          {user && (
            <div className="filter-buttons">
              <button
                className={`filter-btn ${filter === "all" ? "active" : ""}`}
                onClick={() => setFilter("all")}
              >
                All Events
              </button>
              <button
                className={`filter-btn ${filter === "matched" ? "active" : ""}`}
                onClick={() => setFilter("matched")}
              >
                Matched Skills ({timeFilteredEvents.filter(e => e.is_skill_match).length})
              </button>
            </div>
          )}
        </div>

        {filteredEvents.length === 0 ? (
          <div className="no-events">
            <p>No {filter === "matched" ? "matching " : ""}events found.</p>
          </div>
        ) : (
          <div className="events-grid">
            {filteredEvents.map((event) => (
              <div 
                key={event.id} 
                className={`event-card ${event.is_skill_match ? "skill-matched" : ""}`}
              >
                {event.is_skill_match && (
                  <div className="skill-match-badge">
                    ✓ {event.skill_match_count} Skill{event.skill_match_count !== 1 ? "s" : ""} Match
                  </div>
                )}
                
                <div className="event-image">
                  <img 
                    src={event.img || "/src/assets/Volunteer_home.jpg"} 
                    alt={event.name}
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = "/src/assets/Volunteer_home.jpg";
                    }}
                  />
                  <span className={`urgency-badge ${getUrgencyClass(event.urgency)}`}>
                    {event.urgency}
                  </span>
                </div>

                <div className="event-content">
                  <h3 className="event-title">{event.name}</h3>
                  
                  <div className="event-meta">
                    <div className="meta-item">
                      <span className="meta-icon">📅</span>
                      <span>{new Date(event.time_label).toLocaleDateString()}</span>
                    </div>
                    <div className="meta-item">
                      <span className="meta-icon">📍</span>
                      <span>{event.location}</span>
                    </div>
                    <div className="meta-item">
                      <span className="meta-icon">👥</span>
                      <span>{event.current_volunteers} / {event.max_volunteers} volunteers</span>
                    </div>
                  </div>

                  <p className="event-description">{event.description}</p>

                  {event.required_skills && event.required_skills.length > 0 && (
                    <div className="event-skills">
                      <strong>Required Skills:</strong>
                      <div className="skills-list">
                        {event.required_skills.map((skill) => (
                          <span 
                            key={skill}
                            className={`skill-tag ${
                              event.matching_skills?.map(s => s.toLowerCase()).includes(skill.toLowerCase()) 
                                ? "matched" 
                                : ""
                            }`}
                          >
                            {skill}
                            {event.matching_skills?.map(s => s.toLowerCase()).includes(skill.toLowerCase()) && " ✓"}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  <button 
                    className={`register-btn ${
                      isEventPast(event.time_label) 
                        ? "disabled" 
                        : event.is_registered 
                          ? "unregister" 
                          : ""
                    }`}
                    disabled={isEventPast(event.time_label) || registering === event.id}
                    onClick={() => handleRegister(event.id)}
                  >
                    {registering === event.id 
                      ? event.is_registered ? "Unregistering..." : "Registering..."
                      : isEventPast(event.time_label) 
                        ? "Event Completed" 
                        : event.is_registered
                          ? "Unregister"
                          : "Register for Event"}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      <Footer />
    </>
  );
}
