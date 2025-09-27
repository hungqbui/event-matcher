import React, { useState } from "react";
import VolunteerHistoryEvent, { type VolunteerHistoryEventData } from "../components/VolunteerHistoryEvent";
import VolunteerHistoryPopup from "../components/VolunteerHistoryPopup";
import "./HistoryListing.css";

const mockHistoryEvents: VolunteerHistoryEventData[] = [
	{
		id: 101,
		img: "/src/assets/FoodDrive.jpg",
		name: "Annual Food Bank Collection",
		time: "Sat, Sep 10, 2023 · 9:00 AM - 3:00 PM",
		description: "Participated in sorting and packing food donations for local families. Helped organize the warehouse and load delivery trucks.",
		score: 85,
		location: "Houston Food Bank",
		urgency: "medium",
		desiredSkills: ["Organization", "Teamwork", "Logistics"],
		tasks: [
			{ id: 1, name: "Sorted canned goods", completed: true, score: 30 },
			{ id: 2, name: "Packed fresh produce", completed: true, score: 25 },
			{ id: 3, name: "Loaded delivery trucks", completed: true, score: 30 },
			{ id: 4, name: "Assisted with registration", completed: false, score: 10 },
		],
	},
	{
		id: 102,
		img: "/src/assets/BloodDrive.webp",
		name: "Community Blood Drive",
		time: "Sun, Aug 14, 2022 · 10:00 AM - 4:00 PM",
		description: "Assisted medical staff with donor registration and provided post-donation care. Ensured a comfortable environment for all participants.",
		score: 95,
		location: "Downtown Community Center",
		urgency: "high",
		desiredSkills: ["Communication", "Empathy", "Medical Assistance"],
		tasks: [
			{ id: 1, name: "Registered donors", completed: true, score: 40 },
			{ id: 2, name: "Provided refreshments", completed: true, score: 30 },
			{ id: 3, name: "Monitored waiting area", completed: true, score: 25 },
		],
	},
	{
		id: 103,
		img: "/src/assets/DisasterRelief.jpg",
		name: "Hurricane Relief Effort",
		time: "Mon, Oct 3, 2022 · 8:00 AM - 5:00 PM",
		description: "Helped distribute emergency supplies and clear debris in affected neighborhoods after the hurricane. Provided support to displaced families.",
		score: 70,
		location: "Coastal Neighborhoods",
		urgency: "high",
		desiredSkills: ["Physical Strength", "Problem Solving", "Compassion"],
		tasks: [
			{ id: 1, name: "Distributed water and food", completed: true, score: 30 },
			{ id: 2, name: "Cleared fallen trees", completed: true, score: 20 },
			{ id: 3, name: "Assisted with temporary shelter setup", completed: false, score: 20 },
		],
	},
];

const HistoryListingPage: React.FC = () => {
	const [selectedEvent, setSelectedEvent] = useState<VolunteerHistoryEventData | null>(null);
	const [isPopupOpen, setIsPopupOpen] = useState(false);

	const handleEventClick = (event: VolunteerHistoryEventData) => {
		setSelectedEvent(event);
		setIsPopupOpen(true);
	};

	const handleClosePopup = () => {
		setIsPopupOpen(false);
		setSelectedEvent(null);
	};

	return (
		<div className="hl-page">
			<h2 className="hl-title">Your Volunteering History</h2>
			<div className="hl-grid">
				{mockHistoryEvents.map((event) => (
					<VolunteerHistoryEvent key={event.id} event={event} onClick={handleEventClick} />
				))}
			</div>

			<VolunteerHistoryPopup
				open={isPopupOpen}
				event={selectedEvent}
				onClose={handleClosePopup}
			/>
		</div>
	);
};

export default HistoryListingPage;
