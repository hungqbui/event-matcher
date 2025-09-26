import React, { useState } from "react";
import EventManagementPopup from "./EventManagementPopup";
import type { EventData } from "./EventManagementPopup";
import "./EventClickable.css";

type Props = {
	event: EventData;
	onSave?: (updated: EventData) => void;
};

const truncate = (s?: string, n = 100) => {
	if (!s) return "";
	return s.length > n ? s.slice(0, n).trimEnd() + "..." : s;
};

const EventClickable: React.FC<Props> = ({ event, onSave }) => {
	const [open, setOpen] = useState(false);

	const handleSave = (data: EventData) => {
		setOpen(false);
		if (onSave) onSave(data);
	};

	return (
		<>
			<div className="ec-card" onClick={() => setOpen(true)} role="button" tabIndex={0}>
				<button
					className="ec-edit-btn"
					aria-label={`Edit ${event.name}`}
					onClick={(e) => {
						e.stopPropagation();
						setOpen(true);
					}}
				>
					<svg width="16" height="16" viewBox="0 0 24 24" fill="#000" xmlns="http://www.w3.org/2000/svg">
						<path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25z" fill="#000" />
						<path d="M20.71 7.04a1 1 0 000-1.41l-2.34-2.34a1 1 0 00-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" fill="#000" />
					</svg>
				</button>
				{event.img ? (
					// eslint-disable-next-line @next/next/no-img-element
					<img src={event.img} alt={event.name} className="ec-image" />
				) : (
					<div className="ec-image ec-image--placeholder">No Image</div>
				)}

				<div className="ec-body">
					<h4 className="ec-title">{event.name}</h4>
					<div className="ec-time">{event.time}</div>
					<p className="ec-desc">{truncate(event.description, 120)}</p>
				</div>
			</div>

			<EventManagementPopup open={open} initial={event} onSave={handleSave} onClose={() => setOpen(false)} />
		</>
	);
};

export default EventClickable;

