import type { LinimasaEvent } from '../../lib/types';
import { YEAR_MIN, YEAR_MAX } from '../../lib/types';

interface Props {
  events: LinimasaEvent[];
  activeIndex: number;
  onSelect: (index: number) => void;
}

const MARKERS = [YEAR_MIN, 1650, 1700, 1750, YEAR_MAX];

export default function Scrubber({ events, activeIndex, onSelect }: Props) {
  const pct = (year: number) => ((year - YEAR_MIN) / (YEAR_MAX - YEAR_MIN)) * 100;

  return (
    <div
      class="chr-scrubber"
      role="slider"
      aria-label="Garis waktu peristiwa"
      aria-valuemin={YEAR_MIN}
      aria-valuemax={YEAR_MAX}
      aria-valuenow={events[activeIndex]?.year ?? YEAR_MIN}
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'ArrowLeft') { e.preventDefault(); onSelect(Math.max(0, activeIndex - 1)); }
        if (e.key === 'ArrowRight') { e.preventDefault(); onSelect(Math.min(events.length - 1, activeIndex + 1)); }
      }}
      style={{
        position: 'relative',
        width: '100%',
        height: '32px',
        margin: '8px 0',
      }}
    >
      {/* Year markers */}
      {MARKERS.map(yr => (
        <span
          key={yr}
          class="yr"
          style={{
            position: 'absolute',
            left: `${pct(yr)}%`,
            transform: 'translateX(-50%)',
            fontSize: '10px',
            color: 'var(--muted)',
            fontFamily: 'var(--mono)',
            bottom: '100%',
            marginBottom: '2px',
            userSelect: 'none',
          }}
        >
          {yr}
        </span>
      ))}

      {/* Track line */}
      <div style={{
        position: 'absolute',
        top: '50%',
        left: 0,
        right: 0,
        height: '1px',
        background: 'var(--line)',
      }} />

      {/* Event dots */}
      {events.map((ev, i) => {
        const year = ev.year ?? YEAR_MIN;
        const isActive = i === activeIndex;
        return (
          <button
            key={ev.id}
            type="button"
            class={`chr-dot ${isActive ? 'active' : ''}`}
            aria-label={`${ev.year ?? '\u2014'}: ${ev.title}`}
            onClick={() => onSelect(i)}
            style={{
              position: 'absolute',
              left: `${pct(year)}%`,
              top: '50%',
              transform: 'translate(-50%, -50%)',
              width: isActive ? '10px' : '6px',
              height: isActive ? '10px' : '6px',
              borderRadius: '50%',
              background: isActive ? 'var(--ink)' : 'var(--muted)',
              border: isActive ? '2px solid var(--accent)' : '1px solid var(--line)',
              cursor: 'pointer',
              padding: 0,
              transition: 'width 0.15s, height 0.15s, background 0.15s',
              zIndex: isActive ? 2 : 1,
            }}
          />
        );
      })}
    </div>
  );
}
