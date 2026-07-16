import type { LinimasaEvent, PortName } from '../../lib/types';
import {
  PORT_POSITIONS, PORT_ORDER, VOC_ROUTES, ACEH_ORBIT_PORTS, portOf,
} from '../../lib/types';

interface Props {
  activeEvent: LinimasaEvent | null;
  onSelectPort: (port: PortName) => void;
}

const LBL_END = new Set(['Nias', 'Singkil', 'Bayang', 'Painan']);

export default function PortMap({ activeEvent, onSelectPort }: Props) {
  const activePort = activeEvent ? portOf(activeEvent) : null;
  const activeIdx = activePort ? PORT_ORDER.indexOf(activePort) : -1;

  const relatedPorts = new Set<PortName>();
  if (activeIdx >= 0) {
    if (activeIdx > 0) relatedPorts.add(PORT_ORDER[activeIdx - 1]);
    if (activeIdx < PORT_ORDER.length - 1) relatedPorts.add(PORT_ORDER[activeIdx + 1]);
  }
  relatedPorts.delete('Aceh');

  return (
    <div class="chr-map-overlay" style={{
      position: 'absolute',
      inset: 0,
      pointerEvents: 'none',
      zIndex: 2,
    }}>
      {/* Route SVG */}
      <svg
        viewBox="0 0 100 100"
        preserveAspectRatio="none"
        style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 1 }}
      >
        {/* VOC routes (dashed copper) */}
        {VOC_ROUTES.map(([from, to]) => {
          const fromPos = PORT_POSITIONS[from];
          const toPos = PORT_POSITIONS[to];
          return (
            <line
              key={`${from}-${to}`}
              x1={fromPos.xPct} y1={fromPos.yPct}
              x2={toPos.xPct} y2={toPos.yPct}
              stroke="var(--route-voc)"
              strokeWidth="0.3"
              strokeDasharray="1 1.5"
              opacity={0.35}
            />
          );
        })}
        {/* Aceh orbit lines (solid teal) */}
        {ACEH_ORBIT_PORTS.map(port => {
          const toPos = PORT_POSITIONS[port];
          const acehPos = PORT_POSITIONS['Aceh'];
          return (
            <line
              key={`aceh-${port}`}
              x1={acehPos.xPct} y1={acehPos.yPct}
              x2={toPos.xPct} y2={toPos.yPct}
              stroke="var(--route-aceh)"
              strokeWidth="0.25"
              strokeDasharray="0.8 1.2"
              opacity={0.3}
            />
          );
        })}
      </svg>

      {/* Port dots */}
      {PORT_ORDER.map(name => {
        const pos = PORT_POSITIONS[name];
        const isActive = name === activePort;
        const isRelated = relatedPorts.has(name);
        const isAceh = name === 'Aceh';
        const anchor = LBL_END.has(name);

        let coreSize = isAceh ? 13 : 9;
        let coreOpacity = 1;
        let lblOpacity = 1;
        let borderColor = 'rgba(243,234,217,0)';
        let borderWidth = 2;

        if (isActive) {
          coreSize = isAceh ? 17 : 13;
          borderColor = 'rgba(90,138,141,.7)';
        } else if (isRelated) {
          coreSize = 10;
          coreOpacity = 0.7;
          lblOpacity = 0.7;
        } else if (!isAceh) {
          coreSize = 6;
          coreOpacity = 0.25;
          lblOpacity = 0;
        }

        return (
          <div
            key={name}
            data-port={name}
            onClick={() => onSelectPort(name)}
            style={{
              position: 'absolute',
              left: `${pos.xPct}%`,
              top: `${pos.yPct}%`,
              transform: 'translate(-50%, -50%)',
              cursor: 'pointer',
              textAlign: anchor ? 'right' : 'left',
              zIndex: 2,
              pointerEvents: 'auto',
            }}
          >
            {/* Halo ring */}
            <span style={{
              display: 'inline-block',
              width: '20px',
              height: '20px',
              borderRadius: '50%',
              border: `2px solid ${borderColor}`,
              position: 'absolute',
              left: '50%',
              top: '50%',
              transform: 'translate(-50%, -50%)',
              pointerEvents: 'none',
              transition: 'border-color 0.2s',
            }} />
            {/* Core dot */}
            <span class="core" style={{
              display: 'inline-block',
              width: `${coreSize}px`,
              height: `${coreSize}px`,
              borderRadius: '50%',
              background: '#f3ead9',
              border: `${isAceh || isActive ? 2 : 1}px solid #29484b`,
              position: 'relative',
              zIndex: 1,
              opacity: coreOpacity,
              transition: 'width 0.2s, height 0.2s, opacity 0.2s',
            }} />
            {/* Label */}
            <span class="lbl" style={{
              position: 'absolute',
              top: '-18px',
              [anchor ? 'right' : 'left']: 0,
              whiteSpace: 'nowrap',
              font: '600 9px var(--sans)',
              color: '#cfc4ab',
              letterSpacing: '.05em',
              textShadow: '0 1px 4px rgba(8,23,25,.9)',
              pointerEvents: 'none',
              opacity: lblOpacity,
              transition: 'opacity 0.2s',
              fontSize: isActive ? '11px' : '9px',
            }}>
              {name.toUpperCase()}
            </span>
          </div>
        );
      })}
    </div>
  );
}
