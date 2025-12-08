import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// Aplicar tema inicial antes del primer render para evitar flash
(function() {
  const savedTheme = localStorage.getItem('theme');
  const root = document.documentElement;
  
  if (savedTheme === 'dark') {
    root.classList.add('dark');
  } else if (savedTheme === 'light') {
    root.classList.remove('dark');
  } else {
    // Si no hay preferencia guardada, usar la preferencia del sistema
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      root.classList.add('dark');
    }
  }
})();

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
