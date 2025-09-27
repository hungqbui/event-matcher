import React from "react";
import type { VolunteerHistoryEventData, Task } from "./VolunteerHistoryEvent";
import "./VolunteerHistoryPopup.css";

type Props = {
	open: boolean;
	event: VolunteerHistoryEventData | null;
	onClose: () => void;
};

const VolunteerHistoryPopup: React.FC<Props> = ({ open, event, onClose }) => {
	if (!open || !event) return null;

	const totalPossibleScore = event.tasks.reduce((sum, task) => sum + task.score, 0);
	const progress = totalPossibleScore > 0 ? (event.score / totalPossibleScore) * 100 : 0;

	return (
		<div className="vhp-backdrop" onMouseDown={onClose}>
			<div className="vhp-modal" onMouseDown={(e) => e.stopPropagation()}>
				<h3>{event.name}</h3>
				<div className="vhp-image-container">
					{event.img ? (
						// eslint-disable-next-line @next/next/no-img-element
						<img src={event.img} alt={event.name} className="vhp-image" />
					) : (
						<div className="vhp-image vhp-image--placeholder">No Image</div>
					)}
				</div>
				<div className="vhp-details">
					<p className="vhp-time">{event.time}</p>
					<p className="vhp-description">{event.description}</p>
					<div className="vhp-score-bar">
						<div className="vhp-score-progress" style={{ width: `${progress}%` }}></div>
						<span className="vhp-score-text">Score: {event.score} / {totalPossibleScore}</span>
					</div>
				</div>
				<div className="vhp-tasks">
					<h4>Tasks Completed:</h4>
					<ul>
						{event.tasks.map((task: Task) => (
							<li key={task.id} className={task.completed ? "vhp-task--completed" : ""}>
								{task.name} (Score: {task.score})
							</li>
						))}
					</ul>
				</div>
				<button className="vhp-close-btn" onClick={onClose}>Close</button>
			</div>
		</div>
	);
};

export default VolunteerHistoryPopup;
