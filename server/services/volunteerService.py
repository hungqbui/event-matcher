MOCKHISTORY = [
	{
		"id": 101,
		"img": "/src/assets/FoodDrive.jpg",
		"name": "Annual Food Bank Collection",
		"time": "Sat, Sep 10, 2023 · 9:00 AM - 3:00 PM",
		"description": "Participated in sorting and packing food donations for local families. Helped organize the warehouse and load delivery trucks.",
		"score": 85,
		"location": "Houston Food Bank",
		"urgency": "medium",
		"desiredSkills": ["Organization", "Teamwork", "Logistics"],
		"tasks": [
			{ "id": 1, "name": "Sorted canned goods", "completed": True, "score": 30 },
			{ "id": 2, "name": "Packed fresh produce", "completed": True, "score": 25 },
			{ "id": 3, "name": "Loaded delivery trucks", "completed": True, "score": 30 },
			{ "id": 4, "name": "Assisted with registration", "completed": False, "score": 10 },
		],
	},
	{
		"id": 102,
		"img": "/src/assets/BloodDrive.webp",
		"name": "Community Blood Drive",
		"time": "Sun, Aug 14, 2022 · 10:00 AM - 4:00 PM",
		"description": "Assisted medical staff with donor registration and provided post-donation care. Ensured a comfortable environment for all participants.",
		"score": 95,
		"location": "Downtown Community Center",
		"urgency": "high",
		"desiredSkills": ["Communication", "Empathy", "Medical Assistance"],
		"tasks": [
			{ "id": 1, "name": "Registered donors", "completed": True, "score": 40 },
			{ "id": 2, "name": "Provided refreshments", "completed": True, "score": 30 },
			{ "id": 3, "name": "Monitored waiting area", "completed": True, "score": 25 },
		],
	},
	{
		"id": 103,
		"img": "/src/assets/DisasterRelief.jpg",
		"name": "Hurricane Relief Effort",
		"time": "Mon, Oct 3, 2022 · 8:00 AM - 5:00 PM",
		"description": "Helped distribute emergency supplies and clear debris in affected neighborhoods after the hurricane. Provided support to displaced families.",
		"score": 70,
		"location": "Coastal Neighborhoods",
		"urgency": "high",
		"desiredSkills": ["Physical Strength", "Problem Solving", "Compassion"],
		"tasks": [
			{ "id": 1, "name": "Distributed water and food", "completed": True, "score": 30 },
			{ "id": 2, "name": "Cleared fallen trees", "completed": True, "score": 20 },
			{ "id": 3, "name": "Assisted with temporary shelter setup", "completed": False, "score": 20 },
		],
	},
]

mocktemp = [
    {
        "name": "John Doe",
        "eventName": "Food Drive",
        "date": "2025-09-20",
        "location": "Houston Community Center",
        "description": "Helped distribute meals.",
        "status": "Attended"
    },
    {
        "name": "Jane Smith",
        "eventName": "Beach Cleanup",
        "date": "2025-08-15",
        "location": "Galveston Beach",
        "description": "Collected trash along shoreline.",
        "status": "No-Show"
    }
]

from flask import jsonify
class VolunteerService:
    """Service for managing volunteer history"""

    @staticmethod
    def get_volunteer_history_user(user_id=None):
        """Get volunteer history for a user"""
        # In a real app, you'd filter by user_id
        return jsonify(MOCKHISTORY), 200
    
    @staticmethod
    def get_volunteer_history_admin():
        """Get mock volunteer history"""
        return jsonify(mocktemp), 200