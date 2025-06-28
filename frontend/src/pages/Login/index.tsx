import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import { useAuth } from "@/context/useAuth";
import type { CredentialResponse } from "@react-oauth/google";
import axios from "axios";

type GoogleLoginResponse = {
  access_token: string;
  token_type: string;
};

const Login = () => {
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
      navigate("/");
    }
  }, [isAuthenticated, navigate]);

  if (isAuthenticated) return null;

  const handleSuccess = async (credentialResponse: CredentialResponse) => {
    console.log("📡 Sending request to:", axios.defaults.baseURL + "/api/v1/auth/google-login");

    const id_token = credentialResponse?.credential;
    if (!id_token) return;

    try {
      const res = await axios.post<GoogleLoginResponse>("/api/v1/auth/google-login", {
        id_token,
      });

      login(res.data.access_token);
      alert("Login successful!");
    } catch (err) {
      console.error("❌ Login error:", err);
      alert("Login failed.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-blue-50">
      <h1 className="text-3xl font-bold mb-6 text-blue-800">
        Login with Google
      </h1>
      <GoogleLogin
        onSuccess={handleSuccess}
        onError={() => alert("Login Failed")}
      />
    </div>
  );
};

export default Login;
