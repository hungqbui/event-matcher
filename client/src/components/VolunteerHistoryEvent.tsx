import React from "react";
import type { EventData } from "./EventManagementPopup";
import "./VolunteerHistoryEvent.css";

export type Task = {
	id: number;
	name: string;
	completed: boolean;
	score: number;
};

export type VolunteerHistoryEventData = EventData & {
	score: number;
	tasks: Task[];
    time: string;
};

type Props = {
	event: VolunteerHistoryEventData;
	onClick?: (event: VolunteerHistoryEventData) => void;
};

const truncate = (s?: string, n = 100) => {
	if (!s) return "";
	return s.length > n ? s.slice(0, n).trimEnd() + "..." : s;
};

const VolunteerHistoryEvent: React.FC<Props> = ({ event, onClick }) => {
	const totalPossibleScore = event.tasks.reduce((sum, task) => sum + task.score, 0);
	const progress = totalPossibleScore > 0 ? (event.score / totalPossibleScore) * 100 : 0;

	return (
		<div className="vhe-card" onClick={() => onClick && onClick(event)} role="button" tabIndex={0}>
			{event.img ? (
				// eslint-disable-next-line @next/next/no-img-element
				<img src={event.img} alt={event.name} className="vhe-image" />
			) : (
				<div className="vhe-image vhe-image--placeholder">No Image</div>
			)}

			<div className="vhe-body">
				<h4 className="vhe-title">{event.name}</h4>
				<div className="vhe-time">{event.time}</div>
				<p className="vhe-desc">{truncate(event.description, 120)}</p>
				<div className="vhe-score-bar">
					<div className="vhe-score-progress" style={{ width: `${progress}%` }}></div>
					<span className="vhe-score-text">Score: {event.score} / {totalPossibleScore}</span>
				</div>
			</div>
		</div>
	);
};

export default VolunteerHistoryEvent;
