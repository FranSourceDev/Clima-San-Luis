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

// Vercel-style temperature colors
const getTemperatureColor = (temp) => {
  if (temp >= 35) return '#ee0000';      // Rojo - muy caliente
  if (temp >= 30) return '#ff6b35';      // Naranja - caliente
  if (temp >= 25) return '#f5a623';      // Amarillo - cálido
  if (temp >= 20) return '#0cce6b';      // Verde - templado
  if (temp >= 15) return '#00b4d8';      // Cyan - fresco
  if (temp >= 10) return '#0070f3';      // Azul - frío
  return '#7928ca';                       // Violeta - muy frío
};

// Thermometer Icon SVG
const ThermometerIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>
  </svg>
);

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="custom-tooltip">
        <p className="tooltip-name">{data.nombre}</p>
        <p className="tooltip-temp" style={{ color: getTemperatureColor(data.temperatura) }}>
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
            stroke="#eaeaea"
            horizontal={true}
            vertical={false}
          />
          <XAxis 
            type="number" 
            domain={[0, 'auto']}
            stroke="#999999"
            tick={{ fill: '#666666', fontSize: 12 }}
            axisLine={{ stroke: '#eaeaea' }}
            tickFormatter={(value) => `${value}°`}
          />
          <YAxis 
            type="category" 
            dataKey="nombreCorto"
            stroke="#999999"
            tick={{ fill: '#171717', fontSize: 11, fontWeight: 500 }}
            axisLine={{ stroke: '#eaeaea' }}
            width={95}
          />
          <Tooltip 
            content={<CustomTooltip />}
            cursor={{ fill: 'rgba(0, 112, 243, 0.05)' }}
          />
          <Bar 
            dataKey="temperatura" 
            radius={[0, 6, 6, 0]}
            barSize={18}
          >
            {data.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={getTemperatureColor(entry.temperatura)}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="chart-legend">
        <span className="legend-item">
          <span className="legend-color" style={{ background: '#7928ca' }}></span>
          &lt;10°
        </span>
        <span className="legend-item">
          <span className="legend-color" style={{ background: '#0070f3' }}></span>
          10-15°
        </span>
        <span className="legend-item">
          <span className="legend-color" style={{ background: '#00b4d8' }}></span>
          15-20°
        </span>
        <span className="legend-item">
          <span className="legend-color" style={{ background: '#0cce6b' }}></span>
          20-25°
        </span>
        <span className="legend-item">
          <span className="legend-color" style={{ background: '#f5a623' }}></span>
          25-30°
        </span>
        <span className="legend-item">
          <span className="legend-color" style={{ background: '#ff6b35' }}></span>
          30-35°
        </span>
        <span className="legend-item">
          <span className="legend-color" style={{ background: '#ee0000' }}></span>
          &gt;35°
        </span>
      </div>
    </div>
  );
}
