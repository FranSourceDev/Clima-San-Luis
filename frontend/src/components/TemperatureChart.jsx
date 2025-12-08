import { useTheme } from '../contexts/ThemeContext';
import { useMemo, useState, useEffect } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';

// Helper para obtener valores de variables CSS
const getCSSVariable = (variableName) => {
  return getComputedStyle(document.documentElement)
    .getPropertyValue(variableName)
    .trim();
};

// Vercel-style temperature colors - usa variables CSS cuando sea posible
const getTemperatureColor = (temp, theme) => {
  if (temp >= 35) return theme === 'dark' ? '#ef4444' : '#ee0000';
  if (temp >= 30) return theme === 'dark' ? '#fb923c' : '#ff6b35';
  if (temp >= 25) return theme === 'dark' ? '#f59e0b' : '#f5a623';
  if (temp >= 20) return '#0cce6b';
  if (temp >= 15) return '#00b4d8';
  if (temp >= 10) return '#0070f3';
  return theme === 'dark' ? '#a855f7' : '#7928ca';
};

// Thermometer Icon SVG
const ThermometerIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>
  </svg>
);

const CustomTooltip = ({ active, payload, theme }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="custom-tooltip">
        <p className="tooltip-name">{data.nombre}</p>
        <p className="tooltip-temp" style={{ color: getTemperatureColor(data.temperatura, theme) }}>
          {data.temperatura}°C
        </p>
        {data.precipitacion > 0 && (
          <p className="tooltip-precip">Precip: {data.precipitacion} mm</p>
        )}
      </div>
    );
  }
  return null;
};

export default function TemperatureChart({ estaciones, maxItems = 20 }) {
  const { theme } = useTheme();
  const [chartColors, setChartColors] = useState(() => ({
    borderColor: getCSSVariable('--border-color') || '#eaeaea',
    textPrimary: getCSSVariable('--text-primary') || '#171717',
    textSecondary: getCSSVariable('--text-secondary') || '#666666',
    textMuted: getCSSVariable('--text-muted') || '#999999',
    accentBlue: getCSSVariable('--accent-blue') || '#0070f3'
  }));
  
  // Actualizar colores cuando cambie el tema - usar requestAnimationFrame para asegurar que las CSS se actualizaron
  useEffect(() => {
    const updateColors = () => {
      requestAnimationFrame(() => {
        setChartColors({
          borderColor: getCSSVariable('--border-color') || (theme === 'dark' ? '#2a2a2a' : '#eaeaea'),
          textPrimary: getCSSVariable('--text-primary') || (theme === 'dark' ? '#ededed' : '#171717'),
          textSecondary: getCSSVariable('--text-secondary') || (theme === 'dark' ? '#a0a0a0' : '#666666'),
          textMuted: getCSSVariable('--text-muted') || (theme === 'dark' ? '#707070' : '#999999'),
          accentBlue: getCSSVariable('--accent-blue') || '#0070f3'
        });
      });
    };
    
    updateColors();
  }, [theme]); // Recalcular cuando cambie el tema
  
  // Función para limpiar y formatear nombres de estaciones
  const limpiarNombre = (nombre) => {
    // Eliminar prefijos comunes innecesarios
    let nombreLimpio = nombre
      .replace(/^Estación\s+/i, '')
      .replace(/^Est\.\s+/i, '')
      .replace(/^EST\.\s+/i, '')
      .trim();
    
    // Capitalizar correctamente (primera letra de cada palabra)
    nombreLimpio = nombreLimpio
      .split(' ')
      .map(palabra => {
        if (palabra.length === 0) return palabra;
        return palabra.charAt(0).toUpperCase() + palabra.slice(1).toLowerCase();
      })
      .join(' ');
    
    return nombreLimpio || nombre; // Si queda vacío, usar el original
  };

  // Tomar las primeras N estaciones (ya vienen ordenadas por temperatura)
  const data = useMemo(() => {
    return estaciones.slice(0, maxItems).map(est => ({
      ...est,
      nombre: limpiarNombre(est.nombre)
    }));
  }, [estaciones, maxItems]);

  return (
    <div className="chart-container">
      <h2 className="chart-title">
        <span className="chart-icon">
          <ThermometerIcon />
        </span>
        Temperaturas por Estación
      </h2>
      <ResponsiveContainer width="100%" height={500}>
        <BarChart
          key={`chart-${theme}`}
          data={data}
          layout="vertical"
          margin={{ top: 10, right: 30, left: 140, bottom: 10 }}
        >
          <CartesianGrid 
            strokeDasharray="3 3" 
            stroke={chartColors.borderColor}
            horizontal={true}
            vertical={false}
          />
          <XAxis 
            type="number" 
            domain={[0, 'auto']}
            stroke={chartColors.textMuted}
            tick={{ fill: chartColors.textSecondary, fontSize: 12 }}
            axisLine={{ stroke: chartColors.borderColor }}
            tickFormatter={(value) => `${value}°`}
          />
          <YAxis 
            type="category" 
            dataKey="nombre"
            stroke={chartColors.textMuted}
            tick={{ fill: chartColors.textPrimary, fontSize: 11, fontWeight: 500 }}
            axisLine={{ stroke: chartColors.borderColor }}
            width={130}
            tickFormatter={(value) => value && value.length > 25 ? value.substring(0, 22) + '...' : value}
          />
          <Tooltip 
            content={<CustomTooltip theme={theme} />}
            cursor={{ fill: theme === 'dark' ? 'rgba(0, 112, 243, 0.1)' : 'rgba(0, 112, 243, 0.05)' }}
          />
          <Bar 
            dataKey="temperatura" 
            radius={[0, 6, 6, 0]}
            barSize={18}
          >
            {data.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={getTemperatureColor(entry.temperatura, theme)}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="chart-legend">
        <span className="legend-item">
          <span className="legend-color" style={{ background: getTemperatureColor(5, theme) }}></span>
          &lt;10°
        </span>
        <span className="legend-item">
          <span className="legend-color" style={{ background: getTemperatureColor(12, theme) }}></span>
          10-15°
        </span>
        <span className="legend-item">
          <span className="legend-color" style={{ background: getTemperatureColor(17, theme) }}></span>
          15-20°
        </span>
        <span className="legend-item">
          <span className="legend-color" style={{ background: getTemperatureColor(22, theme) }}></span>
          20-25°
        </span>
        <span className="legend-item">
          <span className="legend-color" style={{ background: getTemperatureColor(27, theme) }}></span>
          25-30°
        </span>
        <span className="legend-item">
          <span className="legend-color" style={{ background: getTemperatureColor(32, theme) }}></span>
          30-35°
        </span>
        <span className="legend-item">
          <span className="legend-color" style={{ background: getTemperatureColor(37, theme) }}></span>
          &gt;35°
        </span>
      </div>
    </div>
  );
}
