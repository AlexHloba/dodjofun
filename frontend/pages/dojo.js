import { useEffect, useState } from "react";
import { getLessons } from "../utils/api";

export default function DojoPage() {
  const [lessons, setLessons] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;
    getLessons(token).then((res) => setLessons(res.data));
  }, []);

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-4">🏯 Dojo Уроки</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {lessons.map((lesson) => (
          <div key={lesson.id} className="p-4 bg-white rounded-xl shadow">
            <h2 className="text-xl font-semibold">{lesson.title}</h2>
            <p className="text-gray-500">{lesson.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
