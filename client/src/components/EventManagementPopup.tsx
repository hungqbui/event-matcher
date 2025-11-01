import React, { useState, useEffect } from "react";
import "./EventManagementPopup.css";
import * as eventUtils from "../utils/fetchEvents.ts"

export type Urgency = 'low' | 'medium' | 'high';

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
		desiredSkills: []
	});

	const [skills, setSkills] = useState<string[]>([]);

	useEffect(() => {

		eventUtils.fetchSkills().then(fetchedSkills => {
			setSkills(fetchedSkills);
		});
	}, []);
	
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

