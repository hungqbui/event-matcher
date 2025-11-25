import "./volunteerhistory.css";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

type VolunteerRecord = {
  user_id: number;
  name: string;
  eventName: string;
  date: string;
  location: string;
  description: string;
  event_id: number;
  volunteer_id: number;
};

type Task = {
  id: number;
  name: string;
  score: number;
  completed: boolean;
  volunteer_id: number;
  event_id: number;
};

type TaskModalData = {
  volunteer: VolunteerRecord;
  tasks: Task[];
};

export default function VolunteerHistory() {
  const { user } = useAuth();
  const [records, setRecords] = useState<VolunteerRecord[]>([]);
  const [taskModal, setTaskModal] = useState<TaskModalData | null>(null);
  const [ratings, setRatings] = useState<{ [key: number]: number }>({});
  const [loading, setLoading] = useState(false);

  // ===============================
  // 📂 CSV DOWNLOAD
  // ===============================
  const downloadCSV = () => {
    window.open(
      `http://localhost:5000/api/report/volunteer-history/csv?admin_user_id=${user?.id}`,
      "_blank"
    );
  };

  // ===============================
  // 🧾 PDF DOWNLOAD
  // ===============================
  const generatePDF = () => {
    const table = document.querySelector(".vh-table") as HTMLElement;
    if (!table) return alert("No data to export.");

    html2canvas(table).then((canvas) => {
      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF("p", "mm", "a4");
      const imgWidth = 190;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;

      pdf.addImage(imgData, "PNG", 10, 10, imgWidth, imgHeight);
      pdf.save("volunteer_report.pdf");
    });
  };

  // ===============================
  // LOAD HISTORY RECORDS
  // ===============================
  useEffect(() => {
    if (!user?.id) return;

    fetch(
      `http://localhost:5000/api/admin/volunteer-attendance?admin_user_id=${user.id}`
    )
      .then((res) => res.json())
      .then((data) => setRecords(data))
      .catch((err) => console.error("Error:", err));
  }, [user?.id]);

  // ===============================
  // VIEW TASKS IN MODAL
  // ===============================
  const handleViewTasks = async (record: VolunteerRecord) => {
    try {
      const response = await fetch(
        `http://localhost:5000/api/volunteer-tasks/${record.volunteer_id}/${record.event_id}`
      );
      const tasks = await response.json();
      setTaskModal({ volunteer: record, tasks });

      const initialRatings: { [key: number]: number } = {};
      tasks.forEach((task: Task) => {
        initialRatings[task.id] = 100;
      });
      setRatings(initialRatings);
    } catch (err) {
      console.error("Error fetching tasks:", err);
      alert("Failed to load tasks");
    }
  };

  // ===============================
  // RATE TASK
  // ===============================
  const handleRateTask = async (taskId: number) => {
    const ratingPercent = ratings[taskId];
    if (ratingPercent === undefined) return;

    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:5000/api/task/${taskId}/rate`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ rating_percent: ratingPercent }),
        }
      );

      if (response.ok) {
        const result = await response.json();
        alert(
          `Task rated successfully! Score: ${result.actual_score}/${result.original_score} (${result.rating_percent}%)`
        );

        if (taskModal) {
          const updatedResponse = await fetch(
            `http://localhost:5000/api/volunteer-tasks/${taskModal.volunteer.volunteer_id}/${taskModal.volunteer.event_id}`
          );
          const updatedTasks = await updatedResponse.json();
          setTaskModal({ ...taskModal, tasks: updatedTasks });
        }
      } else {
        const error = await response.json();
        alert(error.error || "Failed to rate task");
      }
    } finally {
      setLoading(false);
    }
  };

  const closeModal = () => {
    setTaskModal(null);
    setRatings({});
  };

  return (
    <>
      <Navbar />
      <div className="volunteer-history-page">
        <div className="volunteer-history">
          <h1>Volunteer Participation History</h1>
          <p className="vh-subtitle">Volunteers who attended your events</p>
          <div className="vh-report-panel">
            <h2>Generate Report</h2>

            <button className="vh-download-btn" onClick={downloadCSV}>
              📄 Download CSV
            </button>

            <button className="vh-download-btn" onClick={generatePDF}>
              🧾 Download PDF
            </button>
          </div>
          {records.length === 0 ? (
            <p className="vh-empty">No volunteer attendance records yet.</p>
          ) : (
            <table className="vh-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Event Name</th>
                  <th>Date</th>
                  <th>Location</th>
                  <th>Description</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>
                {records.map((record, index) => (
                  <tr key={index}>
                    <td>{record.name}</td>
                    <td>{record.eventName}</td>
                    <td>{new Date(record.date).toLocaleDateString()}</td>
                    <td>{record.location}</td>
                    <td className="vh-description">{record.description}</td>
                    <td>
                      <button
                        className="vh-view-tasks-btn"
                        onClick={() => handleViewTasks(record)}
                      >
                        View Tasks
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {taskModal && (
          <div className="vh-modal-backdrop" onClick={closeModal}>
            <div
              className="vh-modal"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="vh-modal-header">
                <h2>Tasks for {taskModal.volunteer.name}</h2>
                <p className="vh-modal-subtitle">
                  {taskModal.volunteer.eventName}
                </p>
                <button className="vh-modal-close" onClick={closeModal}>
                  &times;
                </button>
              </div>

              <div className="vh-modal-body">
                {taskModal.tasks.length === 0 ? (
                  <p className="vh-no-tasks">
                    No tasks claimed for this event.
                  </p>
                ) : (
                  <div className="vh-tasks-list">
                    {taskModal.tasks.map((task) => (
                      <div
                        key={task.id}
                        className={`vh-task-card ${
                          task.completed ? "completed" : ""
                        }`}
                      >
                        <div className="vh-task-header">
                          <h3>{task.name}</h3>
                          <span className="vh-task-score">
                            Max Score: {task.score}
                          </span>
                        </div>

                        {task.completed ? (
                          <div className="vh-task-completed">
                            <span className="vh-completed-badge">
                              ✓ Completed & Rated
                            </span>
                            <span className="vh-final-score">
                              Final Score: {task.score}
                            </span>
                          </div>
                        ) : (
                          <div className="vh-task-rating">
                            <label htmlFor={`rating-${task.id}`}>
                              Rating: {ratings[task.id] || 100}%
                            </label>

                            <input
                              id={`rating-${task.id}`}
                              type="range"
                              min="0"
                              max="100"
                              value={ratings[task.id] || 100}
                              onChange={(e) =>
                                setRatings({
                                  ...ratings,
                                  [task.id]: parseInt(e.target.value),
                                })
                              }
                              className="vh-rating-slider"
                            />

                            <div className="vh-rating-info">
                              <span>
                                Score:{" "}
                                {Math.round(
                                  (task.score *
                                    (ratings[task.id] || 100)) /
                                    100
                                )}
                                /{task.score}
                              </span>
                            </div>

                            <button
                              className="vh-rate-btn"
                              onClick={() => handleRateTask(task.id)}
                              disabled={loading}
                            >
                              {loading ? "Rating..." : "Mark Complete & Rate"}
                            </button>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
      <Footer />
    </>
  );
}
