import { GoogleLogin } from "@react-oauth/google";
import { useAuth } from "../../context/useAuth";
import type { CredentialResponse } from "@react-oauth/google";

const Login = () => {
  const { login } = useAuth();

  const handleSuccess = async (credentialResponse: CredentialResponse) => {
    const id_token = credentialResponse?.credential;
    if (!id_token) return;

    try {
      const res = await fetch(
        "http://localhost:8000/api/v1/auth/google-login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id_token }),
        }
      );

      if (!res.ok) {
        throw new Error("Login failed");
      }

      const data = await res.json();
      login(data.access_token);
      alert("Login successful!");

      // You can redirect user if needed
      // window.location.href = "/";
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
