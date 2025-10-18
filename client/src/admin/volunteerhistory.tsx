import AdminNavbar from "./adminnavbar";
import "./volunteerhistory.css";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { useState, useEffect } from "react";

type VolunteerRecord = {
  name: string;
  eventName: string;
  date: string;
  location: string;
  description: string;
  status: "Registered" | "Attended" | "Cancelled" | "No-Show";
};

export default function VolunteerHistory() {
  const [records, setRecords] = useState<VolunteerRecord[]>([]); 
  useEffect(() => {
  fetch('http://localhost:5000/api/volunteer-history')
    .then(res => res.json())
    .then(data => setRecords(data))
    .catch(err => console.error("Error:", err));
}, []);

  return (
    <>
    <Navbar />
    <div>
  
      <AdminNavbar />

      <div className="volunteer-history">
        <h1>Volunteer Participation History</h1>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Event Name</th>
              <th>Date</th>
              <th>Location</th>
              <th>Description</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {records.map((record, index) => (
              <tr key={index}>
              <td>{record.name}</td>
              <td>{record.eventName}</td>
              <td>{record.date}</td>
              <td>{record.location}</td>
              <td>{record.description}</td>
              <td>{record.status}</td>
            </tr>
          ))}
          </tbody>
        </table>
      </div>
    </div>
    <Footer />
    </>
  );
}
