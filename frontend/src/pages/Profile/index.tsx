import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "@/context/useAuth";

type UserProfile = {
  email: string;
  username: string;
  name: string | null;
  active_language_pair_id: string | null;
};

const ProfilePage = () => {
  const { token } = useAuth();
  const [profile, setProfile] = useState<UserProfile>({
    email: "",
    username: "",
    name: null,
    active_language_pair_id: null,
  });
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await axios.get<UserProfile>("/api/v1/me/profile", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setProfile(res.data);
      } catch (err) {
        console.error("Failed to load profile:", err);
        setMessage("Failed to load profile.");
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchProfile();
    }
  }, [token]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.put("/api/v1/me/profile", profile, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setMessage("Profile updated successfully!");
    } catch (err) {
      console.error("Update failed:", err);
      setMessage("Update failed.");
    }
  };

  if (loading) return <div className="text-center mt-10">Loading...</div>;

  return (
    <div className="max-w-3xl mx-auto mt-12 p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-2xl font-bold text-blue-600 mb-6">User Profile</h1>

      {message && (
        <div className="mb-4 text-center text-sm text-green-600">{message}</div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-gray-700">Email</label>
          <input
            type="email"
            name="email"
            value={profile.email}
            onChange={handleChange}
            placeholder="Enter your email"
            className="w-full mt-1 px-4 py-2 border rounded-md"
          />
        </div>

        <div>
          <label className="block text-gray-700">Username</label>
          <input
            type="text"
            name="username"
            value={profile.username}
            onChange={handleChange}
            placeholder="Choose a username"
            className="w-full mt-1 px-4 py-2 border rounded-md"
          />
        </div>

        <div>
          <label className="block text-gray-700">Name</label>
          <input
            type="text"
            name="name"
            value={profile.name ?? ""}
            onChange={handleChange}
            placeholder="Please enter your name"
            className="w-full mt-1 px-4 py-2 border rounded-md"
          />
        </div>

        <div>
          <label className="block text-gray-700">Active Language Pair ID</label>
          <input
            type="number"
            name="active_language_pair_id"
            value={profile.active_language_pair_id ?? ""}
            onChange={handleChange}
            placeholder="Enter your preferred language pair ID"
            className="w-full mt-1 px-4 py-2 border rounded-md"
          />
        </div>

        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Save
        </button>
      </form>
    </div>
  );
};

export default ProfilePage;
