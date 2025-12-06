export default function StationCard({ title, value, unit, icon, subtitle, highlight }) {
  return (
    <div className={`station-card ${highlight ? 'highlight' : ''}`}>
      <div className="card-icon">{icon}</div>
      <div className="card-content">
        <h3 className="card-title">{title}</h3>
        <div className="card-value">
          <span className="value">{value}</span>
          {unit && <span className="unit">{unit}</span>}
        </div>
        {subtitle && <p className="card-subtitle">{subtitle}</p>}
      </div>
    </div>
  );
}
