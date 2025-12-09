import { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import TemperatureChart from './TemperatureChart';
import TemperatureMap from './TemperatureMap';
import StationCard from './StationCard';
import ThemeToggle from './ThemeToggle';

// URL de la API - configurable mediante variable de entorno
// En desarrollo: usa localhost, en producción: usa URL relativa o VITE_API_URL
const getApiUrl = () => {
  // Si hay VITE_API_URL configurada, usarla
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  // En producción (no localhost), usar URL relativa
  if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
    return '/api';
  }
  // Desarrollo local
  return 'http://localhost:5000/api';
};

const API_URL = getApiUrl();

// SVG Icons
const SunCloudIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>
    <circle cx="12" cy="12" r="4"/>
  </svg>
);

const SnowflakeIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="2" x2="12" y2="22"/>
    <path d="M20 16l-4-4 4-4"/>
    <path d="M4 8l4 4-4 4"/>
    <path d="M16 4l-4 4-4-4"/>
    <path d="M8 20l4-4 4 4"/>
  </svg>
);

const FlameIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>
  </svg>
);

const ThermometerIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>
  </svg>
);

const ChartIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="18" y1="20" x2="18" y2="10"/>
    <line x1="12" y1="20" x2="12" y2="4"/>
    <line x1="6" y1="20" x2="6" y2="14"/>
  </svg>
);

const MapPinIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/>
    <circle cx="12" cy="10" r="3"/>
  </svg>
);

const CloudIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>
  </svg>
);

const WindIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"/>
    <path d="M9.6 4.6A2 2 0 1 1 11 8H2"/>
    <path d="M12.6 19.4A2 2 0 1 0 14 16H2"/>
  </svg>
);

const CalendarIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect width="18" height="18" x="3" y="4" rx="2" ry="2"/>
    <line x1="16" x2="16" y1="2" y2="6"/>
    <line x1="8" x2="8" y1="2" y2="6"/>
    <line x1="3" x2="21" y1="10" y2="10"/>
  </svg>
);

const AlertTriangleIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
    <line x1="12" x2="12" y1="9" y2="13"/>
    <line x1="12" x2="12.01" y1="17" y2="17"/>
  </svg>
);

const RefreshIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
    <path d="M3 3v5h5"/>
    <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>
    <path d="M16 16h5v5"/>
  </svg>
);

export default function Dashboard() {
  const [clima, setClima] = useState(null);
  const [estaciones, setEstaciones] = useState([]);
  const [resumen, setResumen] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);

  const fetchData = async () => {
    try {
      setError(null);
      
      const [climaRes, estacionesRes, resumenRes] = await Promise.all([
        axios.get(`${API_URL}/pronostico`),
        axios.get(`${API_URL}/estaciones`),
        axios.get(`${API_URL}/resumen`)
      ]);

      if (climaRes.data.exito) {
        setClima(climaRes.data);
      }

      if (estacionesRes.data.exito) {
        setEstaciones(estacionesRes.data.estaciones);
      }

      if (resumenRes.data.exito) {
        setResumen(resumenRes.data);
      }

      setLastUpdate(new Date());
      setLoading(false);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Error al conectar con el servidor. Asegúrate de que el backend está corriendo.');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    
    // Auto-refresh cada 5 minutos
    const interval = setInterval(fetchData, 5 * 60 * 1000);
    
    return () => clearInterval(interval);
  }, []);

  // Función helper para buscar estación por nombre
  const buscarEstacionPorNombre = (nombreBuscar, listaEstaciones) => {
    if (!listaEstaciones || listaEstaciones.length === 0) return null;
    
    const nombreLower = nombreBuscar.toLowerCase().trim();
    
    // Primero buscar coincidencias exactas o más específicas
    // Priorizar "Ciudad de San Luis" sobre "San Luis Rural" u otras variaciones
    const coincidenciasExactas = listaEstaciones.filter(est => {
      const nombreEst = est.nombre.toLowerCase();
      return nombreEst === nombreLower || 
             nombreEst === `ciudad de ${nombreLower}` ||
             nombreEst.includes(`ciudad de ${nombreLower}`);
    });
    
    if (coincidenciasExactas.length > 0) {
      // Priorizar la que tenga "Ciudad de" en el nombre
      const ciudadDe = coincidenciasExactas.find(est => 
        est.nombre.toLowerCase().includes('ciudad de')
      );
      return ciudadDe || coincidenciasExactas[0];
    }
    
    // Si no hay coincidencia exacta, buscar parcial
    for (const estacion of listaEstaciones) {
      const nombreEst = estacion.nombre.toLowerCase();
      if (nombreEst.includes(nombreLower) || nombreLower.includes(nombreEst.split(' ')[0])) {
        return estacion;
      }
    }
    
    return null;
  };

  // Obtener estación de Aeropuerto San Luis
  const estacionAeropuertoSanLuis = useMemo(() => {
    return buscarEstacionPorNombre('aeropuerto san luis', estaciones);
  }, [estaciones]);

  const formatDate = () => {
    const now = new Date();
    const options = { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    };
    return now.toLocaleDateString('es-AR', options);
  };

  const formatTime = (date) => {
    if (!date) return '';
    return date.toLocaleTimeString('es-AR', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Cargando datos del clima...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-icon">
          <AlertTriangleIcon />
        </div>
        <h2>Error de Conexión</h2>
        <p>{error}</p>
        <button onClick={fetchData} className="retry-button">
          <RefreshIcon /> Reintentar
        </button>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-left">
          <h1 className="header-title">
            <span className="header-icon">
              <SunCloudIcon />
            </span>
            Clima San Luis
          </h1>
          <p className="header-subtitle">Red de Estaciones Meteorológicas</p>
        </div>
        <div className="header-right">
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div>
              <p className="header-date">{formatDate()}</p>
              {lastUpdate && (
                <p className="header-update">
                  Actualizado: {formatTime(lastUpdate)}
                </p>
              )}
            </div>
            <ThemeToggle />
          </div>
        </div>
      </header>

      {/* Alerta meteorológica */}
      {clima?.alerta_meteorologica && (
        <div className="alert-banner">
          <span className="alert-icon">
            <AlertTriangleIcon />
          </span>
          <div className="alert-content">
            <strong>Alerta Meteorológica</strong>
            {clima.alerta_meteorologica.zona_afectada && (
              <p>Zona: {clima.alerta_meteorologica.zona_afectada}</p>
            )}
          </div>
        </div>
      )}

      {/* Cards de resumen */}
      <div className="cards-grid">
        <StationCard
          title="Temperatura Mínima"
          value={resumen?.temperatura_minima ?? '--'}
          unit="°C"
          icon={<SnowflakeIcon />}
          iconClass="temp-cold"
          subtitle="Pronóstico hoy"
        />
        <StationCard
          title="Temperatura Máxima"
          value={resumen?.temperatura_maxima ?? '--'}
          unit="°C"
          icon={<FlameIcon />}
          iconClass="temp-hot"
          subtitle="Pronóstico hoy"
          highlight={resumen?.temperatura_maxima >= 30}
        />
        <StationCard
          title="Temperatura Actual"
          value={estacionAeropuertoSanLuis?.temperatura ?? '--'}
          unit="°C"
          icon={<ThermometerIcon />}
          iconClass="temp-avg"
          subtitle={estacionAeropuertoSanLuis?.nombre || "Aeropuerto San Luis"}
        />
        <StationCard
          title="Rango Actual"
          value={`${resumen?.temperatura_actual_min ?? '--'} - ${resumen?.temperatura_actual_max ?? '--'}`}
          unit="°C"
          icon={<ChartIcon />}
          iconClass="temp-range"
          subtitle="Min - Max registrado"
        />
      </div>

      {/* Pronóstico para Hoy */}
      {clima?.pronostico_hoy && (
        <div className="estado-actual">
          <h2 className="section-title">
            <span className="section-icon">
              <CalendarIcon />
            </span>
            Pronóstico para Hoy
          </h2>
          <div className="estado-content">
            {clima.pronostico_hoy.descripcion && (
              <p className="pronostico-hoy-descripcion">
                {clima.pronostico_hoy.descripcion}
              </p>
            )}
            
            {/* Cielo */}
            {clima.pronostico_hoy.cielo && (
              <p className="estado-item">
                <span className="estado-icon">
                  <CloudIcon />
                </span>
                {clima.pronostico_hoy.cielo}
              </p>
            )}
            
            {/* Viento */}
            {clima.pronostico_hoy.viento && (
              <p className="estado-item">
                <span className="estado-icon">
                  <WindIcon />
                </span>
                {clima.pronostico_hoy.viento}
              </p>
            )}
          </div>
        </div>
      )}

      {/* Gráfico de temperaturas */}
      {estaciones.length > 0 && (
        <TemperatureChart estaciones={estaciones} maxItems={25} />
      )}

      {/* Mapa de temperaturas */}
      {estaciones.length > 0 && (
        <TemperatureMap estaciones={estaciones} />
      )}

      {/* Pronóstico extendido */}
      {clima?.pronostico_extendido && clima.pronostico_extendido.length > 0 && (
        <div className="pronostico-extendido">
          <h2 className="section-title">
            <span className="section-icon">
              <CalendarIcon />
            </span>
            Pronóstico Extendido
          </h2>
          <div className="pronostico-grid">
            {clima.pronostico_extendido.map((dia, index) => (
              <div key={index} className="pronostico-card">
                <h3 className="pronostico-dia">{dia.dia}</h3>
                <p className="pronostico-fecha">{dia.fecha}</p>
                {dia.temperatura_minima !== null && (
                  <p className="pronostico-temp">
                    <span className="temp-min">{dia.temperatura_minima}°</span>
                    <span className="temp-separator">/</span>
                    <span className="temp-max">{dia.temperatura_maxima}°</span>
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="dashboard-footer">
        <p>
          Datos obtenidos de{' '}
          <a href="https://clima.sanluis.gob.ar/" target="_blank" rel="noopener noreferrer">
            clima.sanluis.gob.ar
          </a>
          {' '}— REM Gobierno de San Luis
        </p>
      </footer>
    </div>
  );
}
