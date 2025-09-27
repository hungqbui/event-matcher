import React, { useState } from "react";
import "./NotificationSystem.css";

interface Notification {
  id: number;
  message: string;
  read: boolean;
}

const NotificationSystem: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([
    {
      id: 1,
      message: "New event assignment: Community Food Drive",
      read: false,
    },
    {
      id: 2,
      message: "Event update: Beach cleanup location changed",
      read: false,
    },
    { id: 3, message: "Reminder: Community Garden Build tomorrow", read: true },
  ]);

  const [isOpen, setIsOpen] = useState<boolean>(false);

  const unreadCount = notifications.filter((n) => !n.read).length;

  const removeNotification = (id: number): void => {
    setNotifications(notifications.filter((n) => n.id !== id));
  };

  const markAsRead = (id: number): void => {
    setNotifications(
      notifications.map((n) => (n.id === id ? { ...n, read: true } : n))
    );
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
          {notifications.map((notification) => (
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
          ))}
        </div>
      )}
    </div>
  );
};

export default NotificationSystem;
