import React, { useState, useEffect } from "react";
import "./EventManagementPopup.css";
import * as eventUtils from "../utils/fetchEvents.ts"

export type Urgency = 'low' | 'medium' | 'high';

export type Task = {
	id?: number;
	name: string;
	score: number;
	completed?: boolean;
	volunteer_id?: number;
	event_id?: number;
};

export const AVAILABLE_SKILLS = [
	"First Aid",
	"CPR",
	"Teaching",
	"Leadership",
	"Organization",
	"Communication",
	"Problem Solving",
	"Event Planning",
	"Social Media",
	"Photography",
	"Writing",
	"Public Speaking",
	"Fundraising",
	"Project Management",
	"Language Translation",
	"Medical",
	"Construction",
	"Technology",
	"Cooking",
	"Driving"
] as const;

export type EventData = {
	id?: string | number;
	img?: string;
	name: string;
	time: string;
	location: string;
	urgency: Urgency;
	description?: string;
	desiredSkills: string[];
	tasks?: Task[];
};

type Props = {
	open: boolean;
	initial?: EventData;
	onSave: (data: EventData) => void;
	onClose: () => void;
};

const EventManagementPopup: React.FC<Props> = ({ open, initial, onSave, onClose }) => {
	const [form, setForm] = useState<EventData>({
		name: "",
		time: new Date().toISOString().slice(0, 16),
		location: "",
		urgency: "medium",
		description: "",
		img: "",
		desiredSkills: [],
		tasks: []
	});

	const [skills, setSkills] = useState<string[]>([]);
	const [newTask, setNewTask] = useState({ name: "", score: 0 });
	const [editingTask, setEditingTask] = useState<Task | null>(null);
	const [tasks, setTasks] = useState<Task[]>([]);

	useEffect(() => {
		eventUtils.fetchSkills().then(fetchedSkills => {
			setSkills(fetchedSkills);
		});
	}, []);

	useEffect(() => {
		if (open && initial?.id) {
			// Fetch tasks for this event
			fetch(`http://127.0.0.1:5000/api/tasks/event/${initial.id}`)
				.then(res => res.json())
				.then(data => setTasks(data))
				.catch(err => console.error("Error fetching tasks:", err));
		} else if (!open) {
			setTasks([]);
		}
	}, [open, initial?.id]);
	
	const [skillSearch, setSkillSearch] = useState("");
	const filteredSkills = skills.filter(skill =>
		skill.toLowerCase().includes(skillSearch.toLowerCase())
	);

	useEffect(() => {
		if (initial) setForm({ ...form, ...initial });
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [initial, open]);

	useEffect(() => {
		if (!open) {
			setForm((f) => ({
				...f,
				name: f.name ?? "",
				time: f.time ?? new Date().toISOString().slice(0, 16),
				location: f.location ?? "",
				urgency: f.urgency ?? "medium",
				description: f.description ?? "",
				img: f.img ?? "",
				desiredSkills: f.desiredSkills ?? []
			}));
		}
	}, [open]);

	if (!open) return null;

	const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
		const { name, value } = e.target;
		setForm((s) => ({ ...s, [name]: value }));
	};

	const handleSkillToggle = (skill: string) => {
		setForm(prev => ({
			...prev,
			desiredSkills: prev.desiredSkills.includes(skill)
				? prev.desiredSkills.filter(s => s !== skill)
				: [...prev.desiredSkills, skill]
		}));
	};

	const handleSubmit = (e: React.FormEvent) => {
		e.preventDefault();

		if (form.id !== undefined)
			eventUtils.updateEvent(form.id as number, form).then(() => {
				onSave(form);
			});
		else
			eventUtils.createEvent(form).then((createdEvent) => {
				onSave(createdEvent);
			});
	};

	const handleCreateTask = async () => {
		if (!form.id) {
			alert("Please save the event first before adding tasks.");
			return;
		}

		if (!newTask.name.trim() || newTask.score <= 0) {
			alert("Please provide a task name and a positive score.");
			return;
		}

		try {
			const response = await fetch("http://127.0.0.1:5000/api/tasks/", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					event_id: form.id,
					name: newTask.name,
					score: newTask.score
				})
			});

			if (response.ok) {
				// Refresh tasks list
				const tasksRes = await fetch(`http://127.0.0.1:5000/api/tasks/event/${form.id}`);
				const updatedTasks = await tasksRes.json();
				setTasks(updatedTasks);
				setNewTask({ name: "", score: 0 });
			} else {
				const error = await response.json();
				alert(error.message || "Failed to create task");
			}
		} catch (err) {
			console.error("Error creating task:", err);
			alert("Failed to create task");
		}
	};

	const handleUpdateTask = async () => {
		if (!editingTask || !editingTask.id) return;

		try {
			const response = await fetch(`http://127.0.0.1:5000/api/tasks/${editingTask.id}`, {
				method: "PUT",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					name: editingTask.name,
					score: editingTask.score
				})
			});

			if (response.ok) {
				// Refresh tasks list
				const tasksRes = await fetch(`http://127.0.0.1:5000/api/tasks/event/${form.id}`);
				const updatedTasks = await tasksRes.json();
				setTasks(updatedTasks);
				setEditingTask(null);
			} else {
				const error = await response.json();
				alert(error.message || "Failed to update task");
			}
		} catch (err) {
			console.error("Error updating task:", err);
			alert("Failed to update task");
		}
	};

	const handleDeleteTask = async (taskId: number) => {
		if (!confirm("Are you sure you want to delete this task?")) return;

		try {
			const response = await fetch(`http://127.0.0.1:5000/api/tasks/${taskId}`, {
				method: "DELETE"
			});

			if (response.ok) {
				// Refresh tasks list
				const tasksRes = await fetch(`http://127.0.0.1:5000/api/tasks/event/${form.id}`);
				const updatedTasks = await tasksRes.json();
				setTasks(updatedTasks);
			} else {
				const error = await response.json();
				alert(error.message || "Failed to delete task");
			}
		} catch (err) {
			console.error("Error deleting task:", err);
			alert("Failed to delete task");
		}
	};

	return (
		<div className="emp-backdrop" onMouseDown={onClose}>
			<div className="emp-modal" onMouseDown={(e) => e.stopPropagation()}>
				<h3>{initial ? "Edit Event" : "Create Event"}</h3>
				<form onSubmit={handleSubmit} className="emp-form">
					<label>
						Image URL
						<input name="img" value={form.img || ""} onChange={handleChange} placeholder="https://example.com/image.jpg" />
					</label>

					<label>
						Name
						<input name="name" value={form.name} onChange={handleChange} required placeholder="e.g., Community Food Drive" />
					</label>

					<label>
						Date and Time
						<input
							type="datetime-local"
							name="time"
							value={form.time}
							onChange={handleChange}
							required
						/>
					</label>

					<label>
						Location
						<input
							name="location"
							value={form.location}
							onChange={handleChange}
							required
							placeholder="e.g., Community Center, 123 Main St"
						/>
					</label>

					<label>
						Urgency
						<select
							name="urgency"
							value={form.urgency}
							onChange={handleChange}
							required
							className="emp-select"
						>
							<option value="low">Low Priority</option>
							<option value="medium">Medium Priority</option>
							<option value="high">High Priority</option>
						</select>
					</label>

					<label>
						Description
						<textarea name="description" value={form.description || ""} onChange={handleChange} rows={4} placeholder="Describe the event..." />
					</label>

					<label>
						Desired Skills
						<div className="emp-skills-container">
							<input
								type="text"
								placeholder="Search skills..."
								value={skillSearch}
								onChange={(e) => setSkillSearch(e.target.value)}
								className="emp-skills-search"
							/>
							<div className="emp-skills-list">
								{filteredSkills.map(skill => (
									<div
										key={skill}
										className={`emp-skill-item ${form.desiredSkills.includes(skill) ? 'emp-skill-item--selected' : ''}`}
										onClick={() => handleSkillToggle(skill)}
									>
										{skill}
									</div>
								))}
							</div>
						</div>
					</label>

					{form.id && (
						<div className="emp-tasks-section">
							<h4>Event Tasks</h4>
							<div className="emp-tasks-list">
								{tasks.map(task => (
									<div key={task.id} className="emp-task-item">
										{editingTask?.id === task.id ? (
											<>
												<input
													type="text"
													value={editingTask?.name || ""}
													onChange={(e) => setEditingTask(editingTask ? { ...editingTask, name: e.target.value, score: editingTask.score } : null)}
													className="emp-task-input"
												/>
												<input
													type="number"
													value={editingTask?.score || 0}
													onChange={(e) => setEditingTask(editingTask ? { ...editingTask, name: editingTask.name, score: parseInt(e.target.value) || 0 } : null)}
													className="emp-task-score"
													min="0"
												/>
												<button type="button" onClick={handleUpdateTask} className="emp-task-btn emp-task-save">
													Save
												</button>
												<button type="button" onClick={() => setEditingTask(null)} className="emp-task-btn emp-task-cancel-edit">
													Cancel
												</button>
											</>
										) : (
											<>
												<span className="emp-task-name">{task.name}</span>
												<span className="emp-task-score-badge">{task.score} pts</span>
												<button type="button" onClick={() => setEditingTask(task)} className="emp-task-btn emp-task-edit">
													Edit
												</button>
												<button type="button" onClick={() => handleDeleteTask(task.id!)} className="emp-task-btn emp-task-delete">
													Delete
												</button>
											</>
										)}
									</div>
								))}
							</div>

							<div className="emp-new-task">
								<input
									type="text"
									placeholder="Task name"
									value={newTask.name}
									onChange={(e) => setNewTask({ ...newTask, name: e.target.value })}
									className="emp-task-input"
								/>
								<input
									type="number"
									placeholder="Points"
									value={newTask.score || ""}
									onChange={(e) => setNewTask({ ...newTask, score: parseInt(e.target.value) || 0 })}
									className="emp-task-score"
									min="0"
								/>
								<button type="button" onClick={handleCreateTask} className="emp-task-btn emp-task-add">
									Add Task
								</button>
							</div>
						</div>
					)}

					<div className="emp-actions">
						<button type="button" className="emp-cancel" onClick={onClose}>
							Cancel
						</button>
						<button type="submit" className="emp-save">
							Save
						</button>
					</div>
				</form>
			</div>
		</div>
	);
};

export default EventManagementPopup;

