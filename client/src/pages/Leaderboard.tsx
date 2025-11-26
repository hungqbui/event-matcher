import React, { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import "./Leaderboard.css";

type LeaderboardEntry = {
  name: string;
  volunteer_id: number;
  total_points: number;
};

const Leaderboard: React.FC = () => {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:5000/api/leaderboard")
      .then((res) => res.json())
      .then((data) => {
        setLeaderboard(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching leaderboard:", err);
        setLoading(false);
      });
  }, []);

  const getMedalEmoji = (rank: number) => {
    if (rank === 1) return "🥇";
    if (rank === 2) return "🥈";
    if (rank === 3) return "🥉";
    return rank;
  };

  return (
    <>
      <Navbar />
      <div className="leaderboard-page">
        <div className="leaderboard-container">
          <h1 className="leaderboard-title">🏆 Volunteer Leaderboard</h1>
          <p className="leaderboard-subtitle">Top 10 Volunteers by Points Earned</p>

          {loading ? (
            <p className="leaderboard-loading">Loading...</p>
          ) : leaderboard.length === 0 ? (
            <p className="leaderboard-empty">No volunteers yet. Be the first to earn points!</p>
          ) : (
            <div className="leaderboard-list">
              {leaderboard.map((entry, index) => (
                <div
                  key={entry.volunteer_id}
                  className={`leaderboard-item ${index < 3 ? `leaderboard-item--top${index + 1}` : ""}`}
                >
                  <div className="leaderboard-rank">{getMedalEmoji(index + 1)}</div>
                  <div className="leaderboard-name">{entry.name}</div>
                  <div className="leaderboard-points">
                    <span className="points-value">{entry.total_points}</span>
                    <span className="points-label">points</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      <Footer />
    </>
  );
};

export default Leaderboard;