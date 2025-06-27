import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { AuthProvider } from "./context/AuthProvider.tsx";

const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
if (!clientId) {
  throw new Error("VITE_GOOGLE_CLIENT_ID is not defined in .env file");
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId={clientId}>
      <AuthProvider>
        <App />
      </AuthProvider>
    </GoogleOAuthProvider>
  </React.StrictMode>
);

//ساختن یک فایل AuthContext.tsx برای نگه داشتن وضعیت کاربر

//ذخیره‌ی JWT داخلی در localStorage بعد از لاگین موفق

//استفاده از useContext(AuthContext) در Navbar برای نشون دادن دکمه Login/Profile

//ساختن یک PrivateRoute ساده (بعداً) برای routeهایی که نیاز به login دارن
