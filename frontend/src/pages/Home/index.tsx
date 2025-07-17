import SearchBar from "../../components/SearchBar";

const Home = () => {
  const handleSearch = (value: string) => {
    // API call will be added later
    console.log("Search:", value);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-green-50">
      <h1 className="text-4xl font-bold text-green-800 mb-4">LexiLoop Home</h1>
      <SearchBar onSubmit={handleSearch} />
      {/* TranslateBox removed */}
    </div>
  );
};

export default Home;
