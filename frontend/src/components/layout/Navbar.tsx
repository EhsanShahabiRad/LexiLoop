import React from "react";

const Navbar: React.FC = () => {
  return (
    <nav className="bg-blue-600 text-white px-6 py-4 shadow-md">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <div className="text-2xl font-bold tracking-wide">LexiLoop</div>
        <div className="space-x-4">
          <button className="bg-white text-blue-600 px-4 py-2 rounded-md hover:bg-blue-100 transition">
            Home
          </button>
          <button className="bg-white text-blue-600 px-4 py-2 rounded-md hover:bg-blue-100 transition">
            Login
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
