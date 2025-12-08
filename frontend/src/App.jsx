import { ThemeProvider } from './contexts/ThemeContext'
import Dashboard from './components/Dashboard'
import './styles/dashboard.css'

function App() {
  return (
    <ThemeProvider>
      <Dashboard />
    </ThemeProvider>
  )
}

export default App
