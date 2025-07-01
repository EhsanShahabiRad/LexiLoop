import { useEffect, useState } from "react";
import axiosInstance from "@/utils/axiosInstance";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useAuth } from "@/context/useAuth";
import { profileSchema } from "./validationSchema";
import type { ProfileFormData } from "./types";

type LanguagePair = {
  id: number;
  source_language_name: string;
  target_language_name: string;
};

type UpdateProfileResponse = {
  access_token: string;
  token_type: string;
  profile: {
    email: string;
    username: string;
    name: string | null;
    active_language_pair_id: number | null;
    created_at: string;
    id: number;
  };
};

const ProfilePage = () => {
  const { token } = useAuth();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isValid },
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    mode: "onChange",
    defaultValues: {
      email: "",
      username: "",
      name: "",
      active_language_pair_id: "",
    },
  });

  const [languagePairs, setLanguagePairs] = useState<LanguagePair[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [profileRes, languageRes] = await Promise.all([
          axiosInstance.get<ProfileFormData>("/api/v1/me/profile", {
            headers: { Authorization: `Bearer ${token}` },
          }),
          axiosInstance.get<LanguagePair[]>("/api/v1/language-pairs"),
        ]);

        setLanguagePairs(languageRes.data);

        reset({
          email: profileRes.data.email,
          username: profileRes.data.username,
          name: profileRes.data.name ?? "",
          active_language_pair_id: profileRes.data.active_language_pair_id
            ? String(profileRes.data.active_language_pair_id)
            : "",
        });
      } catch (err) {
        console.error("Failed to load profile or language pairs:", err);
        setMessage("Failed to load profile.");
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchData();
    }
  }, [token, reset]);

  const { login } = useAuth();

  const onSubmit = async (data: ProfileFormData) => {
    try {
      const res = await axiosInstance.put<UpdateProfileResponse>(
        "/api/v1/me/profile",
        data,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (res.data.access_token) {
        login(res.data.access_token);
      }

      reset({
        email: res.data.profile.email,
        username: res.data.profile.username,
        name: res.data.profile.name ?? "",
        active_language_pair_id: res.data.profile.active_language_pair_id
          ? String(res.data.profile.active_language_pair_id)
          : "",
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

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <input
            type="email"
            {...register("email")}
            readOnly
            className="w-full mt-1 px-4 py-2 border rounded-md bg-gray-100 cursor-not-allowed"
          />
        </div>

        <div>
          <label className="block text-gray-700">Username</label>
          <input
            type="text"
            {...register("username")}
            className="w-full mt-1 px-4 py-2 border rounded-md"
          />
          {errors.username && (
            <p className="text-red-500 text-sm">{errors.username.message}</p>
          )}
        </div>

        <div>
          <label className="block text-gray-700">Name</label>
          <input
            type="text"
            {...register("name")}
            className="w-full mt-1 px-4 py-2 border rounded-md"
          />
          {errors.name && (
            <p className="text-red-500 text-sm">{errors.name.message}</p>
          )}
        </div>

        <div>
          <label className="block text-gray-700">Language Pair</label>
          <select
            {...register("active_language_pair_id")}
            className="w-full mt-1 px-4 py-2 border rounded-md"
          >
            <option value="">Select language pair</option>
            {languagePairs.map((pair) => (
              <option key={pair.id} value={String(pair.id)}>
                {pair.source_language_name} → {pair.target_language_name}
              </option>
            ))}
          </select>
          {errors.active_language_pair_id && (
            <p className="text-red-500 text-sm">
              {errors.active_language_pair_id.message}
            </p>
          )}
        </div>

        <button
          type="submit"
          disabled={!isValid}
          className={`px-4 py-2 rounded text-white ${
            isValid
              ? "bg-blue-600 hover:bg-blue-700"
              : "bg-gray-400 cursor-not-allowed"
          }`}
        >
          Save
        </button>
      </form>
    </div>
  );
};

export default ProfilePage;
