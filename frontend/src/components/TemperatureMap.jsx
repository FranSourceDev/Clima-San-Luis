import { useState, useMemo } from 'react';
import { MapContainer, TileLayer, CircleMarker, Tooltip } from 'react-leaflet';
import { useTheme } from '../contexts/ThemeContext';
import 'leaflet/dist/leaflet.css';

// Map Icon SVG
const MapIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/>
    <line x1="9" x2="9" y1="3" y2="18"/>
    <line x1="15" x2="15" y1="6" y2="21"/>
  </svg>
);

// Vercel-style temperature colors para el borde del marcador
const getTemperatureColor = (temp, theme) => {
  if (temp >= 35) return theme === 'dark' ? '#ef4444' : '#ee0000';
  if (temp >= 30) return theme === 'dark' ? '#fb923c' : '#ff6b35';
  if (temp >= 25) return theme === 'dark' ? '#f59e0b' : '#f5a623';
  if (temp >= 20) return '#0cce6b';
  if (temp >= 15) return '#00b4d8';
  if (temp >= 10) return '#0070f3';
  return theme === 'dark' ? '#a855f7' : '#7928ca';
};

export default function TemperatureMap({ estaciones }) {
  const { theme } = useTheme();
  // Centro de San Luis provincia
  const center = [-33.3, -66.3];
  const [hoveredStation, setHoveredStation] = useState(null);
  
  // Filtrar estaciones con coordenadas válidas
  const estacionesValidas = estaciones.filter(
    est => est.latitud && est.longitud && est.temperatura !== null
  );
  
  // Seleccionar tiles según el tema
  const tileUrl = useMemo(() => {
    return theme === 'dark'
      ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
      : 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png';
  }, [theme]);

  return (
    <div className="map-container">
      <h2 className="map-title">
        <span className="map-icon">
          <MapIcon />
        </span>
        Mapa de Estaciones - Temperaturas en Tiempo Real
      </h2>
      <div className="map-wrapper">
        <MapContainer
          center={center}
          zoom={8}
          scrollWheelZoom={true}
          className="leaflet-map"
        >
          {/* Mapa base - cambia según el tema */}
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url={tileUrl}
            key={theme} // Forzar re-render cuando cambie el tema
          />
          
          {/* Marcadores de estaciones con nombre y temperatura */}
          {estacionesValidas.map((estacion) => {
            const isHovered = hoveredStation === estacion.id;
            
            return (
              <CircleMarker
                key={estacion.id}
                center={[estacion.latitud, estacion.longitud]}
                radius={6}
                pathOptions={{
                  fillColor: theme === 'dark' ? '#1a1a1a' : '#ffffff',
                  fillOpacity: 0.95,
                  color: getTemperatureColor(estacion.temperatura, theme),
                  weight: 3,
                  opacity: 1
                }}
                eventHandlers={{
                  mouseenter: () => setHoveredStation(estacion.id),
                  mouseleave: () => setHoveredStation(null)
                }}
              >
                <Tooltip 
                  direction="top" 
                  offset={[0, -8]} 
                  className={`temp-tooltip-hover ${isHovered ? 'tooltip-hovered' : ''}`}
                  permanent={true}
                >
                  <div className="tooltip-hover-content">
                    <strong className="tooltip-name-hover">{estacion.nombre}</strong>
                    <span className="tooltip-temp-hover" style={{ color: getTemperatureColor(estacion.temperatura, theme) }}>
                      {estacion.temperatura}°C
                    </span>
                  </div>
                </Tooltip>
              </CircleMarker>
            );
          })}
        </MapContainer>
      </div>
    </div>
  );
}
