import React from "react";
import { formatTimeLabel } from "../utils/dateFormatters";
import "./VolunteerHistoryEvent.css";

export type Task = {
	id: number;
	name: string;
	completed: boolean;
	score: number;
	volunteer_id?: number;
	event_id?: number;
};

export type VolunteerHistoryEventData = {
	id: number;
	volunteer_id: number;
	name: string;
	event_name: string;
	event_id?: number;
	time_label: string;
	description: string;
	location: string;
	urgency: "low" | "medium" | "high";
	score: number;
	created_at: string;
	img?: string;
	tasks?: Task[];
	date?: string;
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
	const totalPossibleScore = event.tasks?.reduce((sum, task) => sum + task.score, 0) || 0;
	const progress = totalPossibleScore > 0 ? (event.score / totalPossibleScore) * 100 : 0;

	return (
		<div className="vhe-card" onClick={() => onClick && onClick(event)} role="button" tabIndex={0}>
			{event.img ? (
				// eslint-disable-next-line @next/next/no-img-element
				<img src={event.img} alt={event.event_name} className="vhe-image" />
			) : (
				<div className="vhe-image vhe-image--placeholder">No Image</div>
			)}

			<div className="vhe-body">
				<h4 className="vhe-title">{event.event_name}</h4>
				<div className="vhe-time">{formatTimeLabel(event.time_label)}</div>
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
