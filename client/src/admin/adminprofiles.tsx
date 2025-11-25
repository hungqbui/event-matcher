import "../profile/profile.css";
import { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import Navbar from "./adminnavbar";
import Footer from "../components/Footer";

export default function AdminProfilePage() {
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    fullName: "",
    address1: "",
    address2: "",
    city: "",
    state: "",
    zip: "",
    skills: [] as string[],
    preferences: "",
    availability: [] as string[], // days of the week
  });

  const [availableSkills, setAvailableSkills] = useState<string[]>([]);
  const [loadingSkills, setLoadingSkills] = useState(true);
  const [loadingProfile, setLoadingProfile] = useState(true);

  const daysOfWeek = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
  ];

  useEffect(() => {
    // Fetch available skills from database
    const fetchSkills = async () => {
      try {
        const response = await fetch("/api/skills");
        if (response.ok) {
          const skills = await response.json();
          setAvailableSkills(skills);
        }
      } catch (err) {
        console.error("Error fetching skills:", err);
      } finally {
        setLoadingSkills(false);
      }
    };

    // Fetch user profile data
    const fetchProfile = async () => {
      if (!user?.id) return;
      
      try {
        const response = await fetch(`/api/profile?user_id=${user.id}`);
        if (response.ok) {
          const data = await response.json();
          setFormData(data);
        }
      } catch (err) {
        console.error("Error fetching profile:", err);
      } finally {
        setLoadingProfile(false);
      }
    };

    fetchSkills();
    fetchProfile();
  }, [user?.id]);

  const states = [
    { code: "AL", name: "Alabama" },
    { code: "AK", name: "Alaska" },
    { code: "AZ", name: "Arizona" },
    { code: "AR", name: "Arkansas" },
    { code: "CA", name: "California" },
    { code: "CO", name: "Colorado" },
    { code: "CT", name: "Connecticut" },
    { code: "DE", name: "Delaware" },
    { code: "FL", name: "Florida" },
    { code: "GA", name: "Georgia" },
    { code: "HI", name: "Hawaii" },
    { code: "ID", name: "Idaho" },
    { code: "IL", name: "Illinois" },
    { code: "IN", name: "Indiana" },
    { code: "IA", name: "Iowa" },
    { code: "KS", name: "Kansas" },
    { code: "KY", name: "Kentucky" },
    { code: "LA", name: "Louisiana" },
    { code: "ME", name: "Maine" },
    { code: "MD", name: "Maryland" },
    { code: "MA", name: "Massachusetts" },
    { code: "MI", name: "Michigan" },
    { code: "MN", name: "Minnesota" },
    { code: "MS", name: "Mississippi" },
    { code: "MO", name: "Missouri" },
    { code: "MT", name: "Montana" },
    { code: "NE", name: "Nebraska" },
    { code: "NV", name: "Nevada" },
    { code: "NH", name: "New Hampshire" },
    { code: "NJ", name: "New Jersey" },
    { code: "NM", name: "New Mexico" },
    { code: "NY", name: "New York" },
    { code: "NC", name: "North Carolina" },
    { code: "ND", name: "North Dakota" },
    { code: "OH", name: "Ohio" },
    { code: "OK", name: "Oklahoma" },
    { code: "OR", name: "Oregon" },
    { code: "PA", name: "Pennsylvania" },
    { code: "RI", name: "Rhode Island" },
    { code: "SC", name: "South Carolina" },
    { code: "SD", name: "South Dakota" },
    { code: "TN", name: "Tennessee" },
    { code: "TX", name: "Texas" },
    { code: "UT", name: "Utah" },
    { code: "VT", name: "Vermont" },
    { code: "VA", name: "Virginia" },
    { code: "WA", name: "Washington" },
    { code: "WV", name: "West Virginia" },
    { code: "WI", name: "Wisconsin" },
    { code: "WY", name: "Wyoming" },
  ];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSkillsChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selected = Array.from(e.target.selectedOptions, opt => opt.value);
    setFormData(prev => ({ ...prev, skills: selected }));
  };

  const handleAvailabilityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selected = Array.from(e.target.selectedOptions, opt => opt.value);
    setFormData(prev => ({ ...prev, availability: selected }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!user?.id) {
      alert("User not authenticated");
      return;
    }

    try {
      const res = await fetch('/api/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...formData, userId: user.id })
      });
      const data = await res.json();
      
      if (!res.ok) {
        throw new Error(data.error || data.message || 'Failed to save profile');
      }
      alert("Profile saved successfully!");
    } catch (err: any) {
      alert(`Error: ${err.message || 'Unknown error'}`);
    }
  };

  return (
    <>
    <Navbar />
    <div className="profile-page">
      {loadingProfile ? (
        <div className="profile-card">
          <div className="profile-loading">Loading profile...</div>
        </div>
      ) : (
        <div className="profile-card">
          <h1 className="profile-title">Profile Management</h1>
          <p className="profile-subtitle">Welcome, {formData.fullName || user?.name || "User"}!</p>
          <form onSubmit={handleSubmit} className="profile-form">
        
        <div className="form-group">
          <label htmlFor="fullName">
            Full Name <span className="required">*</span>
          </label>
          <input
            id="fullName"
            type="text"
            name="fullName"
            maxLength={50}
            required
            value={formData.fullName}
            onChange={handleChange}
            placeholder="Enter your full name"
          />
        </div>

        <div className="form-group">
          <label htmlFor="address1">
            Address Line 1 <span className="required">*</span>
          </label>
          <input
            id="address1"
            type="text"
            name="address1"
            maxLength={100}
            required
            value={formData.address1}
            onChange={handleChange}
            placeholder="Street address"
          />
        </div>

        <div className="form-group">
          <label htmlFor="address2">
            Address Line 2 <span className="optional">(optional)</span>
          </label>
          <input
            id="address2"
            type="text"
            name="address2"
            maxLength={100}
            value={formData.address2}
            onChange={handleChange}
            placeholder="Apt, suite, etc."
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="city">
              City <span className="required">*</span>
            </label>
            <input
              id="city"
              type="text"
              name="city"
              maxLength={100}
              required
              value={formData.city}
              onChange={handleChange}
              placeholder="City"
            />
          </div>

          <div className="form-group form-group-small">
            <label htmlFor="state">
              State <span className="required">*</span>
            </label>
            <select id="state" name="state" required value={formData.state} onChange={handleChange}>
              <option value="">--Select--</option>
              {states.map(s => (
                <option key={s.code} value={s.code}>{s.code}</option>
              ))}
            </select>
          </div>

          <div className="form-group form-group-small">
            <label htmlFor="zip">
              Zip Code <span className="required">*</span>
            </label>
            <input
              id="zip"
              type="text"
              name="zip"
              pattern="^\d{5,9}$"
              required
              value={formData.zip}
              onChange={handleChange}
              placeholder="12345"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="skills">
            Skills <span className="required">*</span>
          </label>
          <select
            id="skills"
            name="skills"
            multiple
            required
            value={formData.skills}
            onChange={handleSkillsChange}
            disabled={loadingSkills}
            className="multi-select"
          >
            {loadingSkills ? (
              <option disabled>Loading skills...</option>
            ) : (
              availableSkills.map(skill => (
                <option key={skill} value={skill}>{skill}</option>
              ))
            )}
          </select>
          <small className="form-hint">Hold Ctrl (Cmd on Mac) to select multiple</small>
        </div>

        <div className="form-group">
          <label htmlFor="preferences">
            Preferences <span className="optional">(optional)</span>
          </label>
          <textarea
            id="preferences"
            name="preferences"
            value={formData.preferences}
            onChange={handleChange}
            placeholder="Tell us about your volunteer preferences..."
            rows={4}
          />
        </div>

        <div className="form-group">
          <label htmlFor="availability">
            Availability <span className="required">*</span>
          </label>
          <select
            id="availability"
            name="availability"
            multiple
            required
            value={formData.availability}
            onChange={handleAvailabilityChange}
            className="multi-select availability-select"
          >
            {daysOfWeek.map(day => (
              <option key={day} value={day}>{day}</option>
            ))}
          </select>
          <small className="form-hint">
            Select the days you're generally available to volunteer
          </small>
        </div>

        <button type="submit" className="profile-save-btn">💾 Save Profile</button>
      </form>
        </div>
      )}
    </div>
    <Footer />
    </>
  );
}
