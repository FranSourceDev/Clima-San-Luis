import { MapContainer, TileLayer, CircleMarker, Tooltip, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const getTemperatureColor = (temp) => {
  if (temp >= 35) return '#ef4444';      // Rojo - muy caliente
  if (temp >= 30) return '#f97316';      // Naranja - caliente
  if (temp >= 25) return '#eab308';      // Amarillo - cálido
  if (temp >= 20) return '#22c55e';      // Verde - templado
  if (temp >= 15) return '#06b6d4';      // Cyan - fresco
  if (temp >= 10) return '#3b82f6';      // Azul - frío
  return '#8b5cf6';                       // Violeta - muy frío
};

const getTemperatureLabel = (temp) => {
  if (temp >= 35) return 'Muy caliente';
  if (temp >= 30) return 'Caliente';
  if (temp >= 25) return 'Cálido';
  if (temp >= 20) return 'Templado';
  if (temp >= 15) return 'Fresco';
  if (temp >= 10) return 'Frío';
  return 'Muy frío';
};

export default function TemperatureMap({ estaciones }) {
  // Centro de San Luis provincia
  const center = [-33.3, -66.3];
  
  // Filtrar estaciones con coordenadas válidas
  const estacionesValidas = estaciones.filter(
    est => est.latitud && est.longitud && est.temperatura !== null
  );

  return (
    <div className="map-container">
      <h2 className="map-title">
        <span className="map-icon">🗺️</span>
        Mapa de Temperaturas
      </h2>
      <div className="map-wrapper">
        <MapContainer
          center={center}
          zoom={8}
          scrollWheelZoom={true}
          className="leaflet-map"
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          />
          
          {estacionesValidas.map((estacion) => (
            <CircleMarker
              key={estacion.id}
              center={[estacion.latitud, estacion.longitud]}
              radius={12}
              pathOptions={{
                fillColor: getTemperatureColor(estacion.temperatura),
                fillOpacity: 0.9,
                color: '#ffffff',
                weight: 2,
                opacity: 0.8
              }}
            >
              <Tooltip 
                direction="top" 
                offset={[0, -10]} 
                opacity={1}
                className="temp-tooltip"
              >
                <div className="tooltip-content">
                  <strong>{estacion.nombre}</strong>
                  <span className="tooltip-temp">{estacion.temperatura}°C</span>
                </div>
              </Tooltip>
              
              <Popup className="temp-popup">
                <div className="popup-content">
                  <h3 className="popup-title">{estacion.nombre}</h3>
                  <div className="popup-temp">
                    <span 
                      className="temp-badge"
                      style={{ backgroundColor: getTemperatureColor(estacion.temperatura) }}
                    >
                      {estacion.temperatura}°C
                    </span>
                    <span className="temp-label">
                      {getTemperatureLabel(estacion.temperatura)}
                    </span>
                  </div>
                  {estacion.precipitacion > 0 && (
                    <p className="popup-precip">
                      🌧️ Precipitación: {estacion.precipitacion} mm
                    </p>
                  )}
                  <p className="popup-coords">
                    📍 {estacion.latitud.toFixed(4)}, {estacion.longitud.toFixed(4)}
                  </p>
                </div>
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>
      
      <div className="map-legend">
        <span className="legend-title">Escala de temperatura:</span>
        <div className="legend-items">
          <span className="legend-item">
            <span className="legend-color" style={{ background: '#8b5cf6' }}></span>
            &lt;10°
          </span>
          <span className="legend-item">
            <span className="legend-color" style={{ background: '#3b82f6' }}></span>
            10-15°
          </span>
          <span className="legend-item">
            <span className="legend-color" style={{ background: '#06b6d4' }}></span>
            15-20°
          </span>
          <span className="legend-item">
            <span className="legend-color" style={{ background: '#22c55e' }}></span>
            20-25°
          </span>
          <span className="legend-item">
            <span className="legend-color" style={{ background: '#eab308' }}></span>
            25-30°
          </span>
          <span className="legend-item">
            <span className="legend-color" style={{ background: '#f97316' }}></span>
            30-35°
          </span>
          <span className="legend-item">
            <span className="legend-color" style={{ background: '#ef4444' }}></span>
            &gt;35°
          </span>
        </div>
      </div>
    </div>
  );
}

