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

const getTemperatureColor = (temp) => {
  if (temp >= 35) return '#ef4444';      // Rojo - muy caliente
  if (temp >= 30) return '#f97316';      // Naranja - caliente
  if (temp >= 25) return '#eab308';      // Amarillo - cálido
  if (temp >= 20) return '#22c55e';      // Verde - templado
  if (temp >= 15) return '#06b6d4';      // Cyan - fresco
  if (temp >= 10) return '#3b82f6';      // Azul - frío
  return '#8b5cf6';                       // Violeta - muy frío
};

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="custom-tooltip">
        <p className="tooltip-name">{data.nombre}</p>
        <p className="tooltip-temp">{data.temperatura}°C</p>
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
        <span className="chart-icon">🌡️</span>
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
            stroke="#30363d"
            horizontal={true}
            vertical={false}
          />
          <XAxis 
            type="number" 
            domain={[0, 'auto']}
            stroke="#8b949e"
            tick={{ fill: '#8b949e', fontSize: 12 }}
            axisLine={{ stroke: '#30363d' }}
            tickFormatter={(value) => `${value}°`}
          />
          <YAxis 
            type="category" 
            dataKey="nombreCorto"
            stroke="#8b949e"
            tick={{ fill: '#c9d1d9', fontSize: 11 }}
            axisLine={{ stroke: '#30363d' }}
            width={95}
          />
          <Tooltip 
            content={<CustomTooltip />}
            cursor={{ fill: 'rgba(88, 166, 255, 0.1)' }}
          />
          <Bar 
            dataKey="temperatura" 
            radius={[0, 4, 4, 0]}
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
  );
}
