import { useState } from "react";
import ProfileForm from "./profile"; //ProfileForm is a functional component in profile.tsx

export default function ProfilePage() {
  // Fake user data – in a real app this would come from a backend
  const [user, setUser] = useState({
    name: "John Smith",
    email: "jsmith@example.com",
  });

  return (
    <div style={{ padding: "2rem" }}>
      <h1>User Profile</h1>
      <p>
        <strong>Name:</strong> {user.name}
      </p>
      <p>
        <strong>Email:</strong> {user.email}
      </p>

      <h2>Edit Profile</h2>
      <ProfileForm user={user} onSave={setUser} />
    </div>
  );
}
