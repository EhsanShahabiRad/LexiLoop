import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/useAuth'

const Navbar: React.FC = () => {
  const { isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="bg-blue-600 text-white px-6 py-4 shadow-md">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <div className="text-xl font-bold tracking-wide">LexiLoop</div>
        <div className="space-x-4">
          <Link to="/" className="bg-white text-blue-600 px-4 py-2 rounded-md hover:bg-blue-100 transition">
            Home
          </Link>

          {!isAuthenticated && (
            <Link to="/login" className="bg-white text-blue-600 px-4 py-2 rounded-md hover:bg-blue-100 transition">
              Login
            </Link>
          )}

          {isAuthenticated && (
            <>
              <Link to="/profile" className="bg-white text-blue-600 px-4 py-2 rounded-md hover:bg-blue-100 transition">
                Profile
              </Link>
              <button
                onClick={handleLogout}
                className="bg-white text-red-600 px-4 py-2 rounded-md hover:bg-red-100 transition"
              >
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar
