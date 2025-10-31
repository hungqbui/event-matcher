import React, { useState, useEffect } from "react";
import EventClickable from "../components/EventClickable";
import EventManagementPopup, { type EventData } from "../components/EventManagementPopup";
import "./EventListing.css";

import * as eventUtils from "../utils/fetchEvents.ts"

const EventListingPage: React.FC = () => {
	const [events, setEvents] = useState<EventData[]>([]);
	const [showCreate, setShowCreate] = useState(false);

	useEffect(() => {
		eventUtils.fetchAllEventsAdmin().then((res : any) => {
			setEvents(res);
		})
	}, [])

	const handleSave = (updated: EventData) => {
		// If the saved event has an id that already exists, update it.
		if (updated.id !== undefined && events.some((e) => e.id === updated.id)) {
			setEvents((prev) => prev.map((e) => (e.id === updated.id ? { ...e, ...updated } : e)));
		} else {
			// Otherwise create a new event and give it a new numeric id.
			setEvents((prev) => [...prev, { ...updated, id: updated.id }]);
			setShowCreate(false);
		}
	};

	const handleOpenCreate = () => setShowCreate(true);
	const handleCloseCreate = () => setShowCreate(false);

	return (
		<div className="el-page">
			<h2 style={{ color: "black" }}>Your Events</h2>
			<div className="el-grid">
				{events.map((ev) => (
					<EventClickable key={ev.id} event={ev} onSave={handleSave} />
				))}
			</div>

			<button className="el-add-btn" onClick={handleOpenCreate} aria-label="Add Event">Add Event +</button>

			<EventManagementPopup open={showCreate} onClose={handleCloseCreate} onSave={handleSave} />
		</div>
	);
};

export default EventListingPage;

