import type { EventData } from "../components/EventManagementPopup";


const API_BASE_URL = 'http://localhost:5000/api';

// Get token from localStorage
const getAuthToken = (): string | null => {

    // TODO: Use once done with auth 
    return "some_token"

    // return localStorage.getItem('authToken');
};

// Regular user fetch - no auth required
export const fetchAllEvents = async (): Promise<EventData[]> => {
    try {
        const response = await fetch(`${API_BASE_URL}/events`);
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
    const token = getAuthToken();
    if (!token) {
        throw new Error('No authentication token found');
    }

    try {
        const response = await fetch(`${API_BASE_URL}/manager/events`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
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
export const createEvent = async (eventData: Omit<EventData, 'id'>): Promise<EventData> => {
    const token = getAuthToken();
    if (!token) {
        throw new Error('No authentication token found');
    }

    try {
        const response = await fetch(`${API_BASE_URL}/manager/events`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(eventData)
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
    const token = getAuthToken();
    if (!token) {
        throw new Error('No authentication token found');
    }

    try {
        const response = await fetch(`${API_BASE_URL}/manager/events/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(eventData)
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
    const token = getAuthToken();
    if (!token) {
        throw new Error('No authentication token found');
    }

    try {
        const response = await fetch(`${API_BASE_URL}/manager/events/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
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