import { useEffect, useState } from "react";

function VolunteerHistory() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetch("/api/admin/volunteer-history")
      .then(res => res.json())
      .then(data => setHistory(data));
  }, []);

  return (
    <div>
      <h1>Volunteer History</h1>
      <table>
        <thead>
          <tr>
            <th>Organization</th>
            <th>Role</th>
            <th>Start</th>
            <th>End</th>
          </tr>
        </thead>
        <tbody>
          {history.map((h: any) => (
            <tr key={h.id}>
              <td>{h.organization}</td>
              <td>{h.role}</td>
              <td>{h.start_date}</td>
              <td>{h.end_date || "Present"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default VolunteerHistory;
