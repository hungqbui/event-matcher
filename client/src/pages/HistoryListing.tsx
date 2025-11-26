import React, { useState, useEffect } from "react";
import VolunteerHistoryEvent, { type VolunteerHistoryEventData } from "../components/VolunteerHistoryEvent";
import VolunteerHistoryPopup from "../components/VolunteerHistoryPopup";
import "./HistoryListing.css";
import * as eventUtils from "../utils/fetchEvents.ts";
import Navbar from "../components/Navbar";


const HistoryListingPage: React.FC = () => {
	const [selectedEvent, setSelectedEvent] = useState<VolunteerHistoryEventData | null>(null);
	const [isPopupOpen, setIsPopupOpen] = useState(false);
	const [historyEvents, setHistoryEvents] = useState<VolunteerHistoryEventData[]>([]);
	const [activeTab, setActiveTab] = useState<"current" | "past">("current");
	const [totalPoints, setTotalPoints] = useState(0);

	useEffect(() => {
		eventUtils.fetchHistoryEvents()
			.then((res: VolunteerHistoryEventData[]) => {
				console.log("Fetched history events:", res);
				setHistoryEvents(res);
			})
			.catch(err => {
				console.error("Error in fetchHistoryEvents:", err);
			});
		
		// Fetch total points
		const userId = localStorage.getItem('pp_user_id');
		if (userId) {
			fetch(`http://localhost:5000/api/volunteer-total-points?user_id=${userId}`)
				.then(res => res.json())
				.then(data => setTotalPoints(data.total_points || 0))
				.catch(err => console.error("Error fetching total points:", err));
		}
	}, []);

	const handleEventClick = (event: VolunteerHistoryEventData) => {
		setSelectedEvent(event);
		setIsPopupOpen(true);
	};

	const handleClosePopup = () => {
		setIsPopupOpen(false);
		setSelectedEvent(null);
	};

	// Filter events by date
	const currentDate = new Date();
	currentDate.setHours(0, 0, 0, 0);

	const currentEvents = historyEvents.filter(event => {
		if (!event.time_label) return false;
		const eventDate = new Date(event.time_label);
		return eventDate >= currentDate;
	});

	const pastEvents = historyEvents.filter(event => {
		if (!event.time_label) return true; // If no date, consider it past
		const eventDate = new Date(event.time_label);
		return eventDate < currentDate;
	});

	const displayEvents = activeTab === "current" ? currentEvents : pastEvents;
	const isCurrentEvent = activeTab === "current";

	return (
		<div className="hl-page">
			<Navbar />
			<h2 className="hl-title">My Events</h2>
			
			<div className="hl-points-banner">
				<div className="hl-points-content">
					<span className="hl-points-label">Total Points Earned</span>
					<span className="hl-points-value">{totalPoints}</span>
				</div>
			</div>
			
			<div className="hl-tabs">
				<button 
					className={`hl-tab ${activeTab === "current" ? "hl-tab--active" : ""}`}
					onClick={() => setActiveTab("current")}
				>
					Current Events ({currentEvents.length})
				</button>
				<button 
					className={`hl-tab ${activeTab === "past" ? "hl-tab--active" : ""}`}
					onClick={() => setActiveTab("past")}
				>
					Past Events ({pastEvents.length})
				</button>
			</div>

			<div className="hl-grid">
				{displayEvents.length > 0 ? (
					displayEvents.map((event) => (
						<VolunteerHistoryEvent key={event.id} event={event} onClick={handleEventClick} />
					))
				) : (
					<p className="hl-empty-message">
						{activeTab === "current" 
							? "No current events. Join some events to see them here!" 
							: "No past events yet."}
					</p>
				)}
			</div>

			<VolunteerHistoryPopup
				open={isPopupOpen}
				event={selectedEvent}
				onClose={handleClosePopup}
				isCurrentEvent={isCurrentEvent}
			/>
		</div>
	);
};

export default HistoryListingPage;
