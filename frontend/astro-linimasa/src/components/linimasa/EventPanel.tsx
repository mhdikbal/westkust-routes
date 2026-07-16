import { useSignal } from '@preact/signals';
import type { LinimasaEvent, EventType } from '../../lib/types';
import { EVENT_TYPE_LABELS, CONFIDENCE_MAP } from '../../lib/types';

interface Props {
  event: LinimasaEvent;
  index: number;
  total: number;
  eraLabel?: string;
  isClimax?: boolean;
}

const TYPE_COLORS: Record<EventType, string> = {
  suksesi: '#e8a040',
  perjanjian: '#6bab90',
  konflik: '#c05a3c',
  diplomasi: '#7b8ec2',
  administratif: '#a086c0',
};

export default function EventPanel({ event: ev, index, total, eraLabel, isClimax }: Props) {
  const showTranscript = useSignal(false);

  const counter = `PERISTIWA ${String(index + 1).padStart(2, '0')} / ${String(total).padStart(2, '0')}`;
  const subtitle = [EVENT_TYPE_LABELS[ev.event_type], ev.ruler_actor].filter(Boolean).join(' \u00b7 ');
  const confidence = CONFIDENCE_MAP[ev.confidence_flag] || { text: ev.confidence_flag || 'Belum diverifikasi silang', icon: '' };

  return (
    <div class={`chr-panel ${isClimax ? 'climax' : ''}`}>
      <p class="chr-counter mono" style="color: var(--muted); font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase;">
        {counter}
      </p>
      <p class="chr-year mono" style="font-size: 2.5rem; font-weight: 700; color: var(--ink); line-height: 1;">
        {ev.year ?? '\u2014'}
      </p>
      <hr class="chr-divider" style="border: none; border-top: 1px solid var(--line); margin: 12px 0;" />
      <h3 class="chr-title" style="font-family: var(--serif); font-size: 1.1rem; font-weight: 600; color: var(--ink); margin: 0 0 4px;">
        {ev.title}
      </h3>
      {isClimax && (
        <p class="chr-climax" style="font-family: var(--serif); font-style: italic; color: var(--voc-copper); font-size: 0.9rem; margin: 4px 0 8px;">
          &ldquo;Arus tidak lagi menuju satu pusat.&rdquo;
        </p>
      )}
      {subtitle && (
        <p class="chr-subtitle" style="font-size: 0.8rem; color: var(--muted-dark); margin: 0 0 4px;">
          {subtitle}
        </p>
      )}
      <p class="chr-meta mono" style="font-size: 0.75rem; color: var(--muted); margin: 0 0 12px;">
        {ev.event_date_raw || '\u2014'}
      </p>

      <div class="chr-quote" style={{
        fontFamily: 'var(--serif)',
        fontStyle: 'italic',
        fontSize: '0.85rem',
        color: 'var(--muted-dark)',
        lineHeight: 1.6,
        borderLeft: `2px solid ${TYPE_COLORS[ev.event_type] || '#888'}`,
        paddingLeft: '12px',
        marginBottom: '12px',
      }}>
        &ldquo;{ev.text_asli}&rdquo;
      </div>

      {ev.notes && (
        <div class="chr-notes" style={{
          fontSize: '0.75rem',
          color: 'var(--muted)',
          marginBottom: '12px',
          lineHeight: 1.5,
        }}>
          {ev.notes}
        </div>
      )}

      <details class="chr-source" style={{
        background: 'var(--panel)',
        borderRadius: '8px',
        padding: '8px 12px',
        marginBottom: '12px',
      }}>
        <summary style={{
          cursor: 'pointer',
          fontSize: '0.75rem',
          fontWeight: 600,
          color: 'var(--muted-dark)',
          letterSpacing: '0.05em',
          textTransform: 'uppercase',
        }}>
          Sumber Primer
        </summary>
        <div style={{ marginTop: '8px', fontSize: '0.75rem', color: 'var(--muted)' }}>
          <p style={{ margin: '0 0 4px' }}>Arsip {ev.source_document || '\u2014'}</p>
          <p style={{ margin: '0 0 4px' }}>
            Halaman {ev.source_page || '\u2014'}{ev.book_page ? `, baris ${ev.book_page}` : ''}
          </p>
          {confidence.icon ? (
            <span class="chr-status" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', marginTop: '4px', fontSize: '0.7rem' }}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style={{ width: '12px', height: '12px' }}>
                <path d={confidence.icon} />
              </svg>
              {confidence.text}
            </span>
          ) : (
            <span style={{ fontSize: '0.7rem', marginTop: '4px', display: 'block' }}>{confidence.text}</span>
          )}
        </div>
      </details>

      <div class="chr-actions" style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
        {ev.notes && (
          <button
            type="button"
            class="chr-btn chr-btn--solid"
            onClick={() => { showTranscript.value = !showTranscript.value; }}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 12px',
              borderRadius: '6px',
              fontSize: '0.8rem',
              fontWeight: 600,
              background: showTranscript.value ? 'var(--ink)' : 'var(--accent)',
              color: showTranscript.value ? 'var(--paper)' : 'var(--ink)',
              border: 'none',
              cursor: 'pointer',
            }}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: '14px', height: '14px' }}>
              <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
              <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
            </svg>
            {showTranscript.value ? 'Tutup transkrip' : 'Baca transkrip'}
          </button>
        )}
        <a
          class="chr-btn chr-btn--line"
          href="../"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            padding: '6px 12px',
            borderRadius: '6px',
            fontSize: '0.8rem',
            fontWeight: 600,
            background: 'transparent',
            color: 'var(--muted-dark)',
            border: '1px solid var(--line)',
            textDecoration: 'none',
            cursor: 'pointer',
          }}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: '14px', height: '14px' }}>
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
            <circle cx="8.5" cy="8.5" r="1.5" />
            <path d="M21 15l-5-5L5 21" />
          </svg>
          Tampilkan pada peta
        </a>
      </div>
    </div>
  );
}
