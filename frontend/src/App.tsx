import Navbar from './components/layout/Navbar';
import Home from './pages/Home';

function App() {
  return (
    <div className="min-h-screen bg-blue-50">
      <Navbar />
      <main className="p-4">
        <Home />
      </main>
    </div>
  );
}

export default App;
// This is the main entry point of the application.