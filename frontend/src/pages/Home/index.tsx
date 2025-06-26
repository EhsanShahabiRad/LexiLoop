import React from "react";

const Home: React.FC = () => {
  return (
    <section className="max-w-4xl mx-auto mt-12 p-6 bg-white shadow-md rounded-lg">
      <h1 className="text-3xl font-bold text-blue-700 mb-4">Welcome to LexiLoop</h1>
      <p className="text-gray-700 text-lg">
        Your personalized language learning assistant. Start exploring words, build flashcards, and improve your skills!
      </p>
    </section>
  );
};

export default Home;
