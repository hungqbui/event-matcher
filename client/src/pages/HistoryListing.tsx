import React, { useState, useEffect } from "react";
import VolunteerHistoryEvent, { type VolunteerHistoryEventData } from "../components/VolunteerHistoryEvent";
import VolunteerHistoryPopup from "../components/VolunteerHistoryPopup";
import "./HistoryListing.css";
import * as eventUtils from "../utils/fetchEvents.ts";



const HistoryListingPage: React.FC = () => {
	const [selectedEvent, setSelectedEvent] = useState<VolunteerHistoryEventData | null>(null);
	const [isPopupOpen, setIsPopupOpen] = useState(false);
	const [historyEvents, setHistoryEvents] = useState<VolunteerHistoryEventData[]>([]);

	useEffect(() => {
		eventUtils.fetchHistoryEvents().then((res: VolunteerHistoryEventData[]) => {
			setHistoryEvents(res);
		});
	}, []);

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
				{historyEvents.map((event) => (
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
