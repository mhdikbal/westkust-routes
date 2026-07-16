import { useSignal, useComputed } from '@preact/signals';
import { useEffect } from 'preact/hooks';
import type { LinimasaEvent, Era, PortName, EventType } from '../../lib/types';
import { portOf, EVENT_TYPE_LABELS, EVENT_TYPE_ICONS } from '../../lib/types';
import { fetchLinimasa } from '../../lib/api';
import SVGAxis from './SVGAxis';
import Scrubber from './Scrubber';
import PortMap from './PortMap';
import EventPanel from './EventPanel';

interface Props {
  events: LinimasaEvent[];
  eras: Era[];
}

const TREATY_TITLE = 'Traktat Painan: pasal-pasal VOC-Songypagouers, akhiri kekuasaan Atjeh';
const EVENT_TYPES: EventType[] = ['suksesi', 'perjanjian', 'konflik', 'diplomasi', 'administratif'];

export default function ChronicleController({ events: initialEvents, eras }: Props) {
  const activeIndex = useSignal(0);
  const showStage = useSignal(true);
  const typeFilter = useSignal<EventType | ''>('');
  const events = useSignal<LinimasaEvent[]>(initialEvents);
  const loading = useSignal(initialEvents.length === 0);
  const error = useSignal('');

  // Client-side fetch on mount
  useEffect(() => {
    if (initialEvents.length > 0) return; // already have data from SSR
    let cancelled = false;
    (async () => {
      try {
        const data = await fetchLinimasa();
        if (!cancelled) {
          events.value = data.items ?? [];
          loading.value = false;
        }
      } catch (e) {
        if (!cancelled) {
          error.value = 'Backend tidak terjangkau. Pastikan backend berjalan.';
          loading.value = false;
        }
      }
    })();
    return () => { cancelled = true; };
  }, []);

  const sorted = useComputed(() => [...events.value].sort((a, b) => (a.year || 0) - (b.year || 0)));
  const filtered = useComputed(() =>
    typeFilter.value ? sorted.value.filter(e => e.event_type === typeFilter.value) : sorted.value
  );

  const activeEvent = useComputed(() => filtered.value[activeIndex.value] ?? null);
  const isClimax = useComputed(() => activeEvent.value?.title === TREATY_TITLE);
  const eraLabel = useComputed(() => {
    const ev = activeEvent.value;
    if (!ev) return '';
    const era = eras.find(e => e.slug === ev.era_slug);
    return era ? `${era.label} \u00b7 ${era.range}` : '';
  });

  const setActive = (i: number) => {
    activeIndex.value = Math.max(0, Math.min(filtered.value.length - 1, i));
  };

  const handleSelectPort = (port: PortName) => {
    const idx = filtered.value.findIndex(ev => portOf(ev) === port);
    if (idx >= 0) setActive(idx);
  };

  const toggleFilter = (t: EventType | '') => {
    typeFilter.value = typeFilter.value === t ? '' : t;
    activeIndex.value = 0;
  };

  // Global keyboard navigation
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); setActive(activeIndex.value - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); setActive(activeIndex.value + 1); }
      if (e.key === 'Escape') { showStage.value = false; }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  return (
    <div class="chr-stage" data-era={activeEvent.value?.era_slug || ''}>
      {/* Loading / error states */}
      {loading.value && (
        <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--muted)' }}>
          <p>Memuat data dari backend...</p>
        </div>
      )}
      {error.value && (
        <div class="caveat error" style={{ marginBottom: '1rem' }}>
          <h2>API tidak tersedia</h2>
          <p>{error.value}</p>
        </div>
      )}

      {/* Type filter pills */}
      <div class="chr-filter-pills">
        <button
          type="button"
          class={`chr-pill ${typeFilter.value === '' ? 'active' : ''}`}
          onClick={() => toggleFilter('')}
        >
          Semua
        </button>
        {EVENT_TYPES.map(t => (
          <button
            key={t}
            type="button"
            class={`chr-pill ${typeFilter.value === t ? 'active' : ''}`}
            onClick={() => toggleFilter(t)}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d={EVENT_TYPE_ICONS[t]} />
            </svg>
            {EVENT_TYPE_LABELS[t]}
          </button>
        ))}
      </div>

      {/* View toggle */}
      <div class="chr-toolbar" style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: '12px',
        flexWrap: 'wrap',
        gap: '8px',
      }}>
        <span id="chrEratag" class="chr-eratag mono" style={{
          fontSize: '0.75rem',
          color: 'var(--muted-dark)',
          fontWeight: 600,
        }}>
          {eraLabel.value}
        </span>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span id="chrCount" class="chr-count mono" style={{
            fontSize: '0.75rem',
            color: 'var(--muted)',
          }}>
            {activeIndex.value + 1} / {filtered.value.length}
          </span>
          <button
            type="button"
            class="view-toggle"
            onClick={() => { showStage.value = !showStage.value; }}
            aria-pressed={showStage.value ? 'false' : 'true'}
            aria-label="Ganti ke tampilan daftar"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 12px',
              borderRadius: '20px',
              fontSize: '0.8rem',
              fontWeight: 600,
              background: 'var(--panel)',
              color: 'var(--ink)',
              border: '1px solid var(--line)',
              cursor: 'pointer',
            }}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: '14px', height: '14px' }}>
              {showStage.value ? (
                <>
                  <line x1="8" y1="6" x2="21" y2="6" /><line x1="8" y1="12" x2="21" y2="12" /><line x1="8" y1="18" x2="21" y2="18" />
                  <line x1="3" y1="6" x2="3.01" y2="6" /><line x1="3" y1="12" x2="3.01" y2="12" /><line x1="3" y1="18" x2="3.01" y2="18" />
                </>
              ) : (
                <>
                  <rect x="3" y="3" width="7" height="18" rx="1" /><rect x="14" y="3" width="7" height="18" rx="1" />
                </>
              )}
            </svg>
            {showStage.value ? 'Tampilan daftar' : 'Tampilan panggung'}
          </button>
        </div>
      </div>

      {/* Chronicle 3-column stage */}
      {showStage.value && (
        <div class="chr-layout" style={{
          display: 'grid',
          gridTemplateColumns: '180px 1fr 320px',
          gap: '16px',
          minHeight: '500px',
        }}>
          {/* Col 1: Era sidebar */}
          <nav id="chrNav" class="chr-nav" aria-label="Navigasi era" style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '4px',
            position: 'sticky',
            top: '80px',
            alignSelf: 'start',
          }}>
            {eras.map(era => {
              const isActive = activeEvent.value?.era_slug === era.slug;
              return (
                <button
                  key={era.slug}
                  type="button"
                  class={`chr-era ${isActive ? 'active' : ''}`}
                  data-slug={era.slug}
                  onClick={() => {
                    const idx = filtered.value.findIndex(ev => ev.era_slug === era.slug);
                    if (idx >= 0) setActive(idx);
                  }}
                  style={{
                    display: 'block',
                    width: '100%',
                    textAlign: 'left',
                    padding: '8px 10px',
                    borderRadius: '8px',
                    border: 'none',
                    cursor: 'pointer',
                    background: isActive ? 'var(--panel-2)' : 'transparent',
                    borderLeft: isActive ? '3px solid var(--voc-copper)' : '3px solid transparent',
                    transition: 'background 0.15s, border-color 0.15s',
                  }}
                >
                  <span class="mono" style={{ fontSize: '10px', color: 'var(--muted)', display: 'block' }}>{era.range}</span>
                  <span style={{ fontFamily: 'var(--serif)', fontWeight: 600, fontSize: '12px', color: isActive ? 'var(--ink)' : 'var(--muted-dark)', display: 'block', marginTop: '2px' }}>{era.label}</span>
                  <span style={{ fontSize: '10px', color: 'var(--muted)', display: 'block', marginTop: '2px', lineHeight: 1.3 }}>{era.headline}</span>
                </button>
              );
            })}
          </nav>

          {/* Col 2: Maritime map + scrubber */}
          <div class="chr-maritime" style={{ position: 'relative', minHeight: '400px' }}>
            {/* Background map image */}
            <div style={{
              position: 'relative',
              width: '100%',
              height: '100%',
              borderRadius: '12px',
              overflow: 'hidden',
              background: 'var(--paper-deep)',
            }}>
              <img
                src="/img/amh-5147-na.jpg"
                alt="Peta VOC pantai barat Sumatra"
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                  filter: 'grayscale(60%) brightness(0.7)',
                  position: 'absolute',
                  inset: 0,
                }}
              />
              {/* Port map overlay */}
              <PortMap activeEvent={activeEvent.value} onSelectPort={handleSelectPort} />
            </div>

            {/* SVG Axis */}
            <div style={{ marginTop: '12px' }}>
              <SVGAxis
                events={filtered.value}
                activeId={activeEvent.value?.id ?? null}
                onSelect={setActive}
              />
            </div>

            {/* Scrubber */}
            <Scrubber
              events={filtered.value}
              activeIndex={activeIndex.value}
              onSelect={setActive}
            />

            {/* Prev / Next buttons */}
            <div style={{ display: 'flex', gap: '8px', justifyContent: 'center', marginTop: '8px' }}>
              <button
                type="button"
                id="chrPrev"
                onClick={() => setActive(activeIndex.value - 1)}
                disabled={activeIndex.value === 0}
                style={{
                  padding: '6px 16px',
                  borderRadius: '6px',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  background: 'var(--panel)',
                  color: 'var(--ink)',
                  border: '1px solid var(--line)',
                  cursor: activeIndex.value === 0 ? 'not-allowed' : 'pointer',
                  opacity: activeIndex.value === 0 ? 0.4 : 1,
                }}
              >
                &larr; Sebelumnya
              </button>
              <button
                type="button"
                id="chrNext"
                onClick={() => setActive(activeIndex.value + 1)}
                disabled={activeIndex.value === filtered.value.length - 1}
                style={{
                  padding: '6px 16px',
                  borderRadius: '6px',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  background: 'var(--accent)',
                  color: 'var(--ink)',
                  border: 'none',
                  cursor: activeIndex.value === filtered.value.length - 1 ? 'not-allowed' : 'pointer',
                  opacity: activeIndex.value === filtered.value.length - 1 ? 0.4 : 1,
                }}
              >
                Selanjutnya &rarr;
              </button>
            </div>

            {/* Legend */}
            <div class="chr-legend" style={{
              display: 'block',
              marginTop: '12px',
              padding: '8px 12px',
              background: 'var(--panel)',
              borderRadius: '8px',
              fontSize: '11px',
              color: 'var(--muted-dark)',
            }}>
              {activeEvent.value && (
                <>
                  <span style={{ display: 'inline-block', width: '8px', height: '8px', borderRadius: '50%', background: '#f3ead9', verticalAlign: 'middle', marginRight: '6px' }} />
                  {portOf(activeEvent.value)}
                  <br />
                </>
              )}
              <span style={{ display: 'inline-block', width: '16px', height: 0, borderTop: '2px solid #5a8a8d', verticalAlign: 'middle', marginRight: '6px' }} />
              Rute kekuasaan
              <br />
              <span style={{ display: 'inline-block', width: '16px', height: 0, borderTop: '2px dashed #a04a35', verticalAlign: 'middle', marginRight: '6px' }} />
              Rute VOC
            </div>
          </div>

          {/* Col 3: Event panel */}
          {activeEvent.value && (
            <EventPanel
              event={activeEvent.value}
              index={activeIndex.value}
              total={filtered.value.length}
              eraLabel={eraLabel.value}
              isClimax={isClimax.value}
            />
          )}
        </div>
      )}

      {/* Hidden — list view is handled by parent linimasa.astro */}
    </div>
  );
}
