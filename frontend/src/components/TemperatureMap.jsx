import { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, CircleMarker, Tooltip, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.heat';

// Componente para el heatmap layer
function HeatmapLayer({ estaciones }) {
  const map = useMap();
  const heatLayerRef = useRef(null);

  useEffect(() => {
    if (!map || estaciones.length === 0) return;

    // Remover layer anterior si existe
    if (heatLayerRef.current) {
      map.removeLayer(heatLayerRef.current);
    }

    // Crear puntos para el heatmap
    // [lat, lng, intensidad] - intensidad basada en temperatura normalizada
    const heatPoints = estaciones
      .filter(est => est.latitud && est.longitud && est.temperatura !== null)
      .map(est => {
        // Normalizar temperatura a un rango 0-1 para intensidad
        // Considerando rango de -5°C a 45°C
        const minTemp = -5;
        const maxTemp = 45;
        const intensity = Math.max(0, Math.min(1, (est.temperatura - minTemp) / (maxTemp - minTemp)));
        return [est.latitud, est.longitud, intensity];
      });

    // Crear el heatmap layer con gradiente personalizado
    // Radio muy grande para cubrir toda la provincia de San Luis
    heatLayerRef.current = L.heatLayer(heatPoints, {
      radius: 200,
      blur: 100,
      maxZoom: 15,
      max: 1.0,
      minOpacity: 0.7,
      gradient: {
        0.0: '#8b5cf6',   // Violeta - muy frío (<10°C)
        0.2: '#3b82f6',   // Azul - frío (10-15°C)
        0.35: '#06b6d4',  // Cyan - fresco (15-20°C)
        0.5: '#22c55e',   // Verde - templado (20-25°C)
        0.65: '#eab308',  // Amarillo - cálido (25-30°C)
        0.8: '#f97316',   // Naranja - caliente (30-35°C)
        1.0: '#ef4444'    // Rojo - muy caliente (>35°C)
      }
    }).addTo(map);

    return () => {
      if (heatLayerRef.current) {
        map.removeLayer(heatLayerRef.current);
      }
    };
  }, [map, estaciones]);

  return null;
}

const getTemperatureColor = (temp) => {
  if (temp >= 35) return '#ef4444';
  if (temp >= 30) return '#f97316';
  if (temp >= 25) return '#eab308';
  if (temp >= 20) return '#22c55e';
  if (temp >= 15) return '#06b6d4';
  if (temp >= 10) return '#3b82f6';
  return '#8b5cf6';
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
        Mapa de Calor - Temperaturas en Tiempo Real
      </h2>
      <div className="map-wrapper">
        <MapContainer
          center={center}
          zoom={8}
          scrollWheelZoom={true}
          className="leaflet-map"
        >
          {/* Mapa base con estilo claro para mejor contraste con heatmap */}
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
          />
          
          {/* Capa de heatmap */}
          <HeatmapLayer estaciones={estacionesValidas} />
          
          {/* Marcadores pequeños con nombre de estación */}
          {estacionesValidas.map((estacion) => (
            <CircleMarker
              key={estacion.id}
              center={[estacion.latitud, estacion.longitud]}
              radius={6}
              pathOptions={{
                fillColor: '#ffffff',
                fillOpacity: 0.9,
                color: getTemperatureColor(estacion.temperatura),
                weight: 3,
                opacity: 1
              }}
            >
              <Tooltip 
                direction="top" 
                offset={[0, -8]} 
                opacity={1}
                className="temp-tooltip"
                permanent={false}
              >
                <div className="tooltip-content">
                  <strong>{estacion.nombre}</strong>
                  <span className="tooltip-temp" style={{ color: getTemperatureColor(estacion.temperatura) }}>
                    {estacion.temperatura}°C
                  </span>
                  <span className="tooltip-label">{getTemperatureLabel(estacion.temperatura)}</span>
                </div>
              </Tooltip>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>
      
      <div className="map-legend">
        <span className="legend-title">Escala de temperatura:</span>
        <div className="legend-items">
          <span className="legend-item">
            <span className="legend-color" style={{ background: '#8b5cf6' }}></span>
            &lt;10°C
          </span>
          <span className="legend-item">
            <span className="legend-color" style={{ background: '#3b82f6' }}></span>
            10-15°C
          </span>
          <span className="legend-item">
            <span className="legend-color" style={{ background: '#06b6d4' }}></span>
            15-20°C
          </span>
          <span className="legend-item">
            <span className="legend-color" style={{ background: '#22c55e' }}></span>
            20-25°C
          </span>
          <span className="legend-item">
            <span className="legend-color" style={{ background: '#eab308' }}></span>
            25-30°C
          </span>
          <span className="legend-item">
            <span className="legend-color" style={{ background: '#f97316' }}></span>
            30-35°C
          </span>
          <span className="legend-item">
            <span className="legend-color" style={{ background: '#ef4444' }}></span>
            &gt;35°C
          </span>
        </div>
      </div>
    </div>
  );
}
