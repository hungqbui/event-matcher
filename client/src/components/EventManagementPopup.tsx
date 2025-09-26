import React, { useState, useEffect } from "react";
import "./EventManagementPopup.css";

export type EventData = {
	id?: string | number;
	img?: string;
	name: string;
	time: string;
	description?: string;
};

type Props = {
	open: boolean;
	initial?: EventData;
	onSave: (data: EventData) => void;
	onClose: () => void;
};

const EventManagementPopup: React.FC<Props> = ({ open, initial, onSave, onClose }) => {
	const [form, setForm] = useState<EventData>({ name: "", time: "", description: "", img: "" });

	useEffect(() => {
		if (initial) setForm({ ...form, ...initial });
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [initial, open]);

	useEffect(() => {
		if (!open) {
			setForm((f) => ({ ...f, name: f.name ?? "", time: f.time ?? "", description: f.description ?? "", img: f.img ?? "" }));
		}
	}, [open]);

	if (!open) return null;

	const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
		const { name, value } = e.target;
		setForm((s) => ({ ...s, [name]: value }));
	};

	const handleSubmit = (e: React.FormEvent) => {
		e.preventDefault();
		onSave(form);
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
						Time
						<input name="time" value={form.time} onChange={handleChange} required placeholder="e.g., Sat, Oct 5 · 9:00 AM" />
					</label>

					<label>
						Description
						<textarea name="description" value={form.description || ""} onChange={handleChange} rows={4} placeholder="Describe the event..." />
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

