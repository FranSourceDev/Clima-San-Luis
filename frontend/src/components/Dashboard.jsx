import { useState, useEffect } from 'react';
import axios from 'axios';
import TemperatureChart from './TemperatureChart';
import TemperatureMap from './TemperatureMap';
import StationCard from './StationCard';

const API_URL = 'http://localhost:5000/api';

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
        <div className="error-icon">⚠️</div>
        <h2>Error de Conexión</h2>
        <p>{error}</p>
        <button onClick={fetchData} className="retry-button">
          Reintentar
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
            <span className="header-icon">🌤️</span>
            Clima San Luis
          </h1>
          <p className="header-subtitle">Red de Estaciones Meteorológicas</p>
        </div>
        <div className="header-right">
          <p className="header-date">{formatDate()}</p>
          {lastUpdate && (
            <p className="header-update">
              Actualizado: {formatTime(lastUpdate)}
            </p>
          )}
        </div>
      </header>

      {/* Alerta meteorológica */}
      {clima?.alerta_meteorologica && (
        <div className="alert-banner">
          <span className="alert-icon">⚠️</span>
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
          icon="❄️"
          subtitle="Pronóstico hoy"
        />
        <StationCard
          title="Temperatura Máxima"
          value={resumen?.temperatura_maxima ?? '--'}
          unit="°C"
          icon="🔥"
          subtitle="Pronóstico hoy"
          highlight={resumen?.temperatura_maxima >= 30}
        />
        <StationCard
          title="Promedio Actual"
          value={resumen?.temperatura_promedio ?? '--'}
          unit="°C"
          icon="🌡️"
          subtitle={`${resumen?.total_estaciones ?? 0} estaciones`}
        />
        <StationCard
          title="Rango Actual"
          value={`${resumen?.temperatura_actual_min ?? '--'} - ${resumen?.temperatura_actual_max ?? '--'}`}
          unit="°C"
          icon="📊"
          subtitle="Min - Max registrado"
        />
      </div>

      {/* Estado actual */}
      {clima?.estado_actual && (
        <div className="estado-actual">
          <h2 className="section-title">
            <span className="section-icon">📍</span>
            Estado Actual
          </h2>
          <div className="estado-content">
            {clima.estado_actual.cielo && (
              <p className="estado-item">
                <span className="estado-icon">🌥️</span>
                {clima.estado_actual.cielo}
              </p>
            )}
            {clima.estado_actual.viento && (
              <p className="estado-item">
                <span className="estado-icon">💨</span>
                {clima.estado_actual.viento}
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
            <span className="section-icon">📆</span>
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
