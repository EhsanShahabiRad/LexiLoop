import { useState } from "react";

type SearchBarProps = {
  onSubmit: (value: string) => void;
};

const SearchBar = ({ onSubmit }: SearchBarProps) => {
  const [searchText, setSearchText] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(searchText);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl relative">
      <input
        type="text"
        className="w-full p-7 text-3xl border-2 border-green-500 rounded-2xl shadow focus:outline-none pr-16 font-bold"
        placeholder="Enter a word to translate..."
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
      />
      <button
        type="submit"
        className="absolute right-4 top-1/2 -translate-y-1/2 text-green-600 hover:text-green-800"
        aria-label="Search"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={2}
          stroke="currentColor"
          className="w-8 h-8"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 104.5 4.5a7.5 7.5 0 0012.15 12.15z"
          />
        </svg>
      </button>
    </form>
  );
};

export default SearchBar;
