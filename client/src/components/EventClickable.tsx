import React, { useState } from "react";
import EventManagementPopup from "./EventManagementPopup";
import type { EventData } from "./EventManagementPopup";
import "./EventClickable.css";
import { FaEdit } from "react-icons/fa";

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
					<div><FaEdit /></div>
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

