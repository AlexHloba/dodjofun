import { useEffect, useState } from "react";
import api from "../lib/api";

export default function UsersPage() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    api.get("/users").then((res) => setUsers(res.data)).catch(console.error);
  }, []);

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">👤 Users</h1>
      <ul className="space-y-2">
        {users.length > 0 ? (
          users.map((u) => (
            <li key={u.id} className="border p-2 rounded">
              {u.username}
            </li>
          ))
        ) : (
          <p>No users found.</p>
        )}
      </ul>
    </main>
  );
}
