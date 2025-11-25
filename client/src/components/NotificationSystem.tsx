import React, { useState, useEffect } from "react";
import "./NotificationSystem.css";

interface Notification {
  id: number;
  message: string;
  read: boolean;
}

const NotificationSystem: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [isOpen, setIsOpen] = useState<boolean>(false);

  useEffect(() => {
    const intId = setInterval(() => { fetchNotifications() }, 5000); // Refresh every 5 seconds
    fetchNotifications()
    return () => { clearInterval(intId); }
  }, []);

  const fetchNotifications = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/notifications?user_id=" + localStorage.getItem("pp_user_id"));
      const data = await response.json();
      setNotifications(data);
    } catch (error) {
      console.error("Error fetching notifications:", error);
    }
  };

  const unreadCount = notifications.filter((n) => !n.read).length;

  const removeNotification = async (id: number): Promise<void> => {
    try {
      const response = await fetch(
        `http://localhost:5000/api/notifications/${id}`,
        {
          method: "DELETE",
        }
      );

      if (response.ok) {
        setNotifications(notifications.filter((n) => n.id !== id));
      }
    } catch (error) {
      console.error("Error deleting notification:", error);
    }
  };

  const markAsRead = async (id: number): Promise<void> => {
    try {
      const response = await fetch(
        `http://localhost:5000/api/notifications/${id}/read`,
        {
          method: "PUT",
        }
      );

      if (response.ok) {
        setNotifications(
          notifications.map((n) => (n.id === id ? { ...n, read: true } : n))
        );
      }
    } catch (error) {
      console.error("Error marking as read:", error);
    }
  };

  return (
    <div className="notification-container">
      <button className="bell-button" onClick={() => setIsOpen(!isOpen)}>
        🔔
        {unreadCount > 0 && <span className="badge">{unreadCount}</span>}
      </button>
      {isOpen && (
        <div className="notification-dropdown">
          <h3>Notifications</h3>
          {notifications.length === 0 ? (
            <p className="no-notifications">No notifications</p>
          ) : (
            notifications.map((notification) => (
              <div
                key={notification.id}
                className={`notification ${!notification.read ? "unread" : ""}`}
                onClick={() => markAsRead(notification.id)}
              >
                <p>{notification.message}</p>
                <button
                  className="close-btn"
                  onClick={(e: React.MouseEvent) => {
                    e.stopPropagation();
                    removeNotification(notification.id);
                  }}
                >
                  ×
                </button>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default NotificationSystem;
