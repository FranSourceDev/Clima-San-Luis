import { useTheme } from '../contexts/ThemeContext';
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
  
  // Obtener valores de variables CSS según el tema
  const borderColor = getCSSVariable('--border-color');
  const textPrimary = getCSSVariable('--text-primary');
  const textSecondary = getCSSVariable('--text-secondary');
  const textMuted = getCSSVariable('--text-muted');
  const accentBlue = getCSSVariable('--accent-blue');
  
  // Tomar las primeras N estaciones (ya vienen ordenadas por temperatura)
  const data = estaciones.slice(0, maxItems).map(est => ({
    ...est,
    // Acortar nombres largos
    nombreCorto: est.nombre.length > 18 
      ? est.nombre.substring(0, 16) + '...' 
      : est.nombre
  }));

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
          data={data}
          layout="vertical"
          margin={{ top: 10, right: 30, left: 100, bottom: 10 }}
        >
          <CartesianGrid 
            strokeDasharray="3 3" 
            stroke={borderColor}
            horizontal={true}
            vertical={false}
          />
          <XAxis 
            type="number" 
            domain={[0, 'auto']}
            stroke={textMuted}
            tick={{ fill: textSecondary, fontSize: 12 }}
            axisLine={{ stroke: borderColor }}
            tickFormatter={(value) => `${value}°`}
          />
          <YAxis 
            type="category" 
            dataKey="nombreCorto"
            stroke={textMuted}
            tick={{ fill: textPrimary, fontSize: 11, fontWeight: 500 }}
            axisLine={{ stroke: borderColor }}
            width={95}
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
