import { useState } from "react";

export default function ProfilePage() {
  const [formData, setFormData] = useState({
    fullName: "",
    address1: "",
    address2: "",
    city: "",
    state: "",
    zip: "",
    skills: [] as string[],
    preferences: "",
    availability: [] as string[], // store ISO dates
  });

  const [newDate, setNewDate] = useState("");

  const states = [
    { code: "TX", name: "Texas" },
    { code: "CA", name: "California" },
    { code: "NY", name: "New York" },
    // add more as needed
  ];

  const skillsOptions = ["Tree Planting", "Disaster Relief", "Youth Mentorship", "Food Drives", "Blood Drives"];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSkillsChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selected = Array.from(e.target.selectedOptions, opt => opt.value);
    setFormData(prev => ({ ...prev, skills: selected }));
  };

  const handleAddDate = () => {
    if (newDate && !formData.availability.includes(newDate)) {
      setFormData(prev => ({ ...prev, availability: [...prev.availability, newDate] }));
      setNewDate("");
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Saved profile:", formData);
    alert("Profile saved (check console for data)");
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>User Profile Management</h1>
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1rem", maxWidth: "500px" }}>
        
        <label>
          Full Name (required):
          <input
            type="text"
            name="fullName"
            maxLength={50}
            required
            value={formData.fullName}
            onChange={handleChange}
          />
        </label>

        <label>
          Address 1 (required):
          <input
            type="text"
            name="address1"
            maxLength={100}
            required
            value={formData.address1}
            onChange={handleChange}
          />
        </label>

        <label>
          Address 2 (optional):
          <input
            type="text"
            name="address2"
            maxLength={100}
            value={formData.address2}
            onChange={handleChange}
          />
        </label>

        <label>
          City (required):
          <input
            type="text"
            name="city"
            maxLength={100}
            required
            value={formData.city}
            onChange={handleChange}
          />
        </label>

        <label>
          State (required):
          <select name="state" required value={formData.state} onChange={handleChange}>
            <option value="">--Select State--</option>
            {states.map(s => (
              <option key={s.code} value={s.code}>{s.name}</option>
            ))}
          </select>
        </label>

        <label>
          Zip Code (min 5, max 9 chars, required):
          <input
            type="text"
            name="zip"
            pattern="^\d{5,9}$"
            required
            value={formData.zip}
            onChange={handleChange}
          />
        </label>

        <label>
          Skills (multi-select, required):
          <select
            name="skills"
            multiple
            required
            value={formData.skills}
            onChange={handleSkillsChange}
          >
            {skillsOptions.map(skill => (
              <option key={skill} value={skill}>{skill}</option>
            ))}
          </select>
        </label>

        <label>
          Preferences (optional):
          <textarea
            name="preferences"
            value={formData.preferences}
            onChange={handleChange}
          />
        </label>

        <label>
          Availability (pick multiple dates, required):
          <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
            <input
              type="date"
              value={newDate}
              onChange={(e) => setNewDate(e.target.value)}
            />
            <button type="button" onClick={handleAddDate}>Add</button>
          </div>
          <ul>
            {formData.availability.map(date => (
              <li key={date}>{date}</li>
            ))}
          </ul>
        </label>

        <button type="submit">Save Profile</button>
      </form>
    </div>
  );
}
