import { useMemo } from 'preact/hooks';
import type { LinimasaEvent, EventType } from '../../lib/types';
import { YEAR_MIN, YEAR_MAX } from '../../lib/types';

interface Props {
  events: LinimasaEvent[];
  activeId: number | null;
  onSelect: (id: number) => void;
}

const TYPE_COLOR: Record<EventType, string> = {
  suksesi: 'var(--evt-suksesi)',
  perjanjian: 'var(--evt-perjanjian)',
  konflik: 'var(--evt-konflik)',
  diplomasi: 'var(--evt-diplomasi)',
  administratif: 'var(--evt-administratif)',
};

const W = 1000;
const H = 220;
const PAD = 5;
const AXIS_Y = 110;
const MIN_GAP_PX = 46;

interface PlacedDot {
  id: number;
  cx: number;
  tier: number;
  event_type: EventType;
  year: number;
}

export default function SVGAxis({ events, activeId, onSelect }: Props) {
  const yMin = YEAR_MIN - 2;
  const yMax = YEAR_MAX + 2;

  const x = (y: number) => PAD + (y - yMin) / (yMax - yMin) * (W - PAD * 2);

  const ticks = useMemo(() => {
    const result: { x: number; year: number }[] = [];
    for (let yr = Math.ceil(yMin / 10) * 10; yr <= yMax; yr += 10) {
      result.push({ x: x(yr), year: yr });
    }
    return result;
  }, [yMin, yMax]);

  const placed = useMemo(() => {
    const sorted = [...events]
      .filter(r => r.year != null)
      .sort((a, b) => (a.year ?? 0) - (b.year ?? 0));
    const result: PlacedDot[] = [];
    sorted.forEach(r => {
      const cx = x(r.year!);
      let tier = 0;
      while (result.some(p => p.tier === tier && Math.abs(p.cx - cx) < MIN_GAP_PX)) tier++;
      result.push({ id: r.id, cx, tier, event_type: r.event_type, year: r.year! });
    });
    return result;
  }, [events, yMin, yMax]);

  const esc = (s: string) => s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c] || c));

  return (
    <svg
      viewBox={`0 0 ${W} ${H}`}
      style={{ width: '100%', height: 'auto', display: 'block' }}
      role="img"
      aria-label="Garis waktu peristiwa"
    >
      {/* Main axis line */}
      <line x1="0" y1={AXIS_Y} x2={W} y2={AXIS_Y} stroke="var(--line)" strokeWidth="1" />

      {/* Decade ticks */}
      {ticks.map(t => (
        <g key={t.year}>
          <line x1={t.x} y1={AXIS_Y - 4} x2={t.x} y2={AXIS_Y + 4} stroke="var(--line)" strokeWidth="1" />
          <text x={t.x} y={AXIS_Y + 20} textAnchor="middle" fill="var(--muted)" fontSize="10" fontFamily="var(--sans)">
            {t.year}
          </text>
        </g>
      ))}

      {/* Event dots with stacking */}
      {placed.map(p => {
        const side = p.tier % 2 === 0 ? -1 : 1;
        const level = Math.floor(p.tier / 2) + 1;
        const cy = AXIS_Y + side * (18 * level + 8);
        const color = TYPE_COLOR[p.event_type] || '#999';
        const isActive = p.id === activeId;

        return (
          <g key={p.id} onClick={() => onSelect(p.id)} style={{ cursor: 'pointer' }}>
            {/* Stem line */}
            <line
              x1={p.cx}
              y1={cy > AXIS_Y ? cy - 8 : cy + 8}
              x2={p.cx}
              y2={AXIS_Y}
              stroke="var(--line)"
              strokeWidth="1"
            />
            {/* Dot */}
            <circle
              cx={p.cx}
              cy={cy}
              r={isActive ? 8 : 6.5}
              fill={color}
              stroke={isActive ? 'var(--ink)' : 'none'}
              strokeWidth={isActive ? 2 : 0}
              class="evt-dot"
              data-id={p.id}
            />
            {/* Year label */}
            <text
              x={p.cx}
              y={cy > AXIS_Y ? cy + 16 : cy - 12}
              textAnchor="middle"
              fill="var(--muted)"
              fontSize="9"
              fontFamily="var(--mono)"
              opacity={isActive ? 1 : 0.7}
            >
              {p.year}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
