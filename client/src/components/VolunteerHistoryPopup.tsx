import React, { useState, useEffect } from "react";
import type { VolunteerHistoryEventData, Task } from "./VolunteerHistoryEvent";
import { formatTimeLabel } from "../utils/dateFormatters";
import "./VolunteerHistoryPopup.css";

type Props = {
	open: boolean;
	event: VolunteerHistoryEventData | null;
	onClose: () => void;
	isCurrentEvent?: boolean;
};

const VolunteerHistoryPopup: React.FC<Props> = ({ open, event, onClose, isCurrentEvent = false }) => {
	const [tasks, setTasks] = useState<Task[]>([]);
	const [unassignedTasks, setUnassignedTasks] = useState<Task[]>([]);
	const [volunteerId, setVolunteerId] = useState<number | null>(null);

	useEffect(() => {
		// Fetch volunteer_id from user_id on component mount
		const fetchVolunteerId = async () => {
			const userId = localStorage.getItem("pp_user_id");
			if (!userId) return;

			try {
				const response = await fetch(`http://127.0.0.1:5000/api/volunteers`);
				if (response.ok) {
					const volunteers = await response.json();
					const currentVolunteer = volunteers.find((v: any) => v.user_id === parseInt(userId));
					if (currentVolunteer) {
						setVolunteerId(currentVolunteer.id);
					}
				}
			} catch (err) {
				console.error("Error fetching volunteer ID:", err);
			}
		};

		fetchVolunteerId();
	}, []);

	useEffect(() => {
		if (open && event) {
			// Fetch all tasks for this event if it's a current event
			if (isCurrentEvent && event.event_id) {
				fetch(`/api/tasks/event/${event.event_id}`)
					.then(res => res.json())
					.then(data => {
						setTasks(data);
						// Filter unassigned tasks
						const unassigned = data.filter((t: Task) => !t.volunteer_id);
						setUnassignedTasks(unassigned);
					})
					.catch(err => console.error("Error fetching tasks:", err));
			} else {
				// For past events, use the tasks from the event data
				setTasks(event.tasks || []);
				setUnassignedTasks([]);
			}
		}
	}, [open, event, isCurrentEvent]);

	const handleClaimTask = async (taskId: number) => {
		if (!volunteerId) {
			alert("Volunteer ID not found. Please log in again.");
			return;
		}

		try {
			const response = await fetch(`http://127.0.0.1:5000/api/tasks/${taskId}/assign`, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ volunteer_id: volunteerId })
			});

			if (response.ok) {
				alert("Task claimed successfully!");
				// Refresh tasks
				if (event?.event_id) {
					const tasksRes = await fetch(`http://127.0.0.1:5000/api/tasks/event/${event.event_id}`);
					const updatedTasks = await tasksRes.json();
					setTasks(updatedTasks);
					const unassigned = updatedTasks.filter((t: Task) => !t.volunteer_id);
					setUnassignedTasks(unassigned);
				}
			} else {
				const error = await response.json();
				alert(error.message || "Failed to claim task");
			}
		} catch (err) {
			console.error("Error claiming task:", err);
			alert("Failed to claim task");
		}
	};

	if (!open || !event) return null;

	const totalPossibleScore = tasks.reduce((sum, task) => sum + task.score, 0) || 0;
	const myTasks = tasks.filter(t => t.volunteer_id === volunteerId);
	const myScore = myTasks.filter(t => t.completed).reduce((sum, task) => sum + task.score, 0);
	const progress = totalPossibleScore > 0 ? (myScore / totalPossibleScore) * 100 : 0;

	return (
		<div className="vhp-backdrop" onMouseDown={onClose}>
			<div className="vhp-modal" onMouseDown={(e) => e.stopPropagation()}>
				<h3>{event.event_name}</h3>
				<div className="vhp-image-container">
					{event.img ? (
						// eslint-disable-next-line @next/next/no-img-element
						<img src={event.img} alt={event.event_name} className="vhp-image" />
					) : (
						<div className="vhp-image vhp-image--placeholder">No Image</div>
					)}
				</div>
				<div className="vhp-details">
					<div className="vhp-info-grid">
					<div className="vhp-info-item">
						<span className="vhp-label">Date & Time:</span>
						<span>{formatTimeLabel(event.time_label)}</span>
					</div>
						<div className="vhp-info-item">
							<span className="vhp-label">Location:</span>
							<span>{event.location}</span>
						</div>
						<div className="vhp-info-item">
							<span className="vhp-label">Urgency:</span>
							<span className={`vhp-urgency vhp-urgency--${event.urgency}`}>
								{event.urgency.charAt(0).toUpperCase() + event.urgency.slice(1)}
							</span>
						</div>
					</div>

					<div className="vhp-description-section">
						<span className="vhp-label">Description:</span>
						<p className="vhp-description">{event.description}</p>
					</div>

					{isCurrentEvent && unassignedTasks.length > 0 && (
						<div className="vhp-tasks-section">
							<h4>Available Tasks to Claim:</h4>
							<div className="vhp-tasks-list">
								{unassignedTasks.map((task: Task) => (
									<div key={task.id} className="vhp-task-item">
										<span className="vhp-task-name">{task.name}</span>
										<span className="vhp-task-score">{task.score} pts</span>
										<button 
											className="vhp-task-claim-btn"
											onClick={() => handleClaimTask(task.id!)}
										>
											Claim Task
										</button>
									</div>
								))}
							</div>
						</div>
					)}

					{myTasks.length > 0 && (
						<div className="vhp-tasks-section">
							<h4>{isCurrentEvent ? "My Tasks:" : "Tasks Completed:"}</h4>
							<div className="vhp-score-section">
								<div className="vhp-score-bar">
									<div className="vhp-score-progress" style={{ width: `${progress}%` }}></div>
									<span className="vhp-score-text">Score: {myScore} / {totalPossibleScore}</span>
								</div>
							</div>
							<ul className="vhp-tasks-list-simple">
								{myTasks.map((task: Task) => (
									<li key={task.id} className={task.completed ? "vhp-task--completed" : "vhp-task--pending"}>
										{task.name} - {task.score} pts {task.completed ? "✓" : "(pending)"}
									</li>
								))}
							</ul>
						</div>
					)}

					{!isCurrentEvent && event.tasks && event.tasks.length > 0 && myTasks.length === 0 && (
						<>
							<div className="vhp-score-section">
								<span className="vhp-label">Performance Score:</span>
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
						</>
					)}
				</div>
				<button className="vhp-close-btn" onClick={onClose}>Close</button>
			</div>
		</div>
	);
};

export default VolunteerHistoryPopup;
