import { useState } from "react";
import { loginUser } from "../utils/api";
import { useRouter } from "next/router";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const { data } = await loginUser(email, password);
      localStorage.setItem("token", data.access_token);
      router.push("/dojo");
    } catch (error) {
      alert("Ошибка входа. Проверьте данные.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <h1 className="text-3xl font-bold mb-6">DojoRise Login</h1>
      <form onSubmit={handleLogin} className="w-80 bg-white p-6 rounded-xl shadow">
        <input
          type="email"
          placeholder="Email"
          className="border p-2 w-full mb-3"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Пароль"
          className="border p-2 w-full mb-3"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          type="submit"
          className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700"
        >
          Войти
        </button>
      </form>
    </div>
  );
}
