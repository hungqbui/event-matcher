import React, { useState } from "react";
import EventClickable from "../components/EventClickable";
import EventManagementPopup, { type EventData } from "../components/EventManagementPopup";
import "./EventListing.css";

const initialMock: EventData[] = [
	{
		id: 1,
		img: "/src/assets/Volunteer_home.jpg",
		name: "Community Food Drive",
		time: "Sat, Oct 5 · 9:00 AM - 12:00 PM",
		description:
			"Join us to collect and distribute food to local families in need. Volunteers will help sort donations and assemble boxes for distribution.",
	},
	{
		id: 2,
		img: "/src/assets/TreePlant.jpg",
		name: "Neighborhood Tree Planting",
		time: "Sun, Oct 13 · 10:00 AM - 2:00 PM",
		description:
			"Help us plant trees around the park to improve air quality and provide shade. Gloves and tools will be provided.",
	},
	{
		id: 3,
		img: "/src/assets/VCleanupHome.webp",
		name: "Coastal Cleanup",
		time: "Sat, Nov 2 · 8:00 AM - 11:00 AM",
		description:
			"A morning of beach cleanup to remove litter and protect marine life. All ages welcome; bring reusable water bottle.",
	},
];

const EventListingPage: React.FC = () => {
	const [events, setEvents] = useState<EventData[]>(initialMock);
	const [showCreate, setShowCreate] = useState(false);

	const handleSave = (updated: EventData) => {
		// If the saved event has an id that already exists, update it.
		if (updated.id !== undefined && events.some((e) => e.id === updated.id)) {
			setEvents((prev) => prev.map((e) => (e.id === updated.id ? { ...e, ...updated } : e)));
		} else {
			// Otherwise create a new event and give it a new numeric id.
			const nextId = events.reduce((max, e) => Math.max(max, Number(e.id ?? 0)), 0) + 1;
			setEvents((prev) => [...prev, { ...updated, id: nextId }]);
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

