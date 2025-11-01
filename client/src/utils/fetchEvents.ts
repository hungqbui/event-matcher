import type { EventData } from "../components/EventManagementPopup";
import type { VolunteerHistoryEventData } from "../components/VolunteerHistoryEvent";


// Get user ID from localStorage
const getUserId = (): string | null => {

    return localStorage.getItem("pp_user_id");

};

// Regular user fetch - no auth required
export const fetchAllEvents = async (): Promise<EventData[]> => {
    try {
        const response = await fetch(`api/events`);
        if (!response.ok) {
            throw new Error('Failed to fetch events');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching events:', error);
        throw error;
    }
};

// Admin fetch with auth
export const fetchAllEventsAdmin = async (): Promise<EventData[]> => {
    const userId = getUserId();
    if (!userId) {
        throw new Error('No user ID found');
    }

    try {
        const response = await fetch(`api/manager/listevents`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userId })
        });

        if (response.status === 401) {
            throw new Error('Unauthorized access');
        }

        if (response.status === 403) {
            throw new Error('Admin privileges required');
        }

        if (!response.ok) {
            throw new Error('Failed to fetch events');
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching events:', error);
        throw error;
    }
};

// Create new event (Admin only)
export const createEvent = async (eventData: EventData): Promise<EventData> => {
    const userId = getUserId();
    if (!userId) {
        throw new Error('No user ID found');
    }

    try {
        const response = await fetch(`api/manager/events`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ...eventData, userId })
        });

        if (response.status === 401) {
            throw new Error('Unauthorized access');
        }

        if (response.status === 403) {
            throw new Error('Admin privileges required');
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Failed to create event');
        }

        return await response.json();
    } catch (error) {
        console.error('Error creating event:', error);
        throw error;
    }
};

// Update event (Admin only)
export const updateEvent = async (id: number, eventData: Partial<EventData>): Promise<EventData> => {
    const userId = getUserId();
    if (!userId) {
        throw new Error('No user ID found');
    }

    try {
        const response = await fetch(`api/manager/events/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ...eventData, userId })
        });

        if (response.status === 401) {
            throw new Error('Unauthorized access');
        }

        if (response.status === 403) {
            throw new Error('Admin privileges required');
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Failed to update event');
        }

        return await response.json();
    } catch (error) {
        console.error('Error updating event:', error);
        throw error;
    }
};

// Delete event (Admin only)
export const deleteEvent = async (id: number): Promise<void> => {
    const userId = getUserId();
    if (!userId) {
        throw new Error('No user ID found');
    }

    try {
        const response = await fetch(`api/manager/events/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userId })
        });

        if (response.status === 401) {
            throw new Error('Unauthorized access');
        }

        if (response.status === 403) {
            throw new Error('Admin privileges required');
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Failed to delete event');
        }
    } catch (error) {
        console.error('Error deleting event:', error);
        throw error;
    }
};

export const fetchHistoryEvents = async (): Promise<VolunteerHistoryEventData[]> => {
    const userId = getUserId();
    if (!userId) {
        throw new Error('No user ID found');
    }

    try {
        const response = await fetch(`api/volunteer_user/history`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userId })
        });
        if (!response.ok) {
            throw new Error('Failed to fetch history events');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching history events:', error);
        throw error;
    }
};

export const fetchSkills = async (): Promise<string[]> => {
    try {
        const response = await fetch(`api/skills`);
        if (!response.ok) {
            throw new Error('Failed to fetch skills');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching skills:', error);
        throw error;
    }
}