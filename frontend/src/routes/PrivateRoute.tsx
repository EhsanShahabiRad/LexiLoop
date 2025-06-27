import { useAuth } from '@/context/useAuth'
import { Navigate } from 'react-router-dom'

type Props = {
  children: React.ReactNode
}

const PrivateRoute = ({ children }: Props) => {
  const { isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

export default PrivateRoute
