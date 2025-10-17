import AdminNavbar from "./adminnavbar";
import "./volunteerhistory.css";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

type VolunteerRecord = {
  name: string;
  eventName: string;
  date: string;
  location: string;
  description: string;
  status: "Registered" | "Attended" | "Cancelled" | "No-Show";
};

const dummyData: VolunteerRecord[] = [
  {
    name: "John Doe",
    eventName: "Food Drive",
    date: "2025-09-20",
    location: "Houston Community Center",
    description: "Helped distribute meals.",
    status: "Attended",
  },
  {
    name: "Jane Smith",
    eventName: "Beach Cleanup",
    date: "2025-08-15",
    location: "Galveston Beach",
    description: "Collected trash along shoreline.",
    status: "No-Show",
  },
];

export default function VolunteerHistory() {
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
            {dummyData.map((record, index) => (
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
