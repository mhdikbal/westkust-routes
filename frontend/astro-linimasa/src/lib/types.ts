export interface LinimasaEvent {
  id: number;
  source_document: string;
  source_page: number;
  book_page: string | null;
  event_date_raw: string | null;
  year: number | null;
  event_type: EventType;
  ruler_actor: string | null;
  title: string;
  era_slug: string | null;
  text_asli: string;
  confidence_flag: string;
  notes: string | null;
}

export type EventType = 'suksesi' | 'perjanjian' | 'konflik' | 'diplomasi' | 'administratif';

export interface Era {
  slug: string;
  label: string;
  range: string;
  headline: string;
  summary: string;
}

export interface EraWithEvents extends Era {
  events: LinimasaEvent[];
}

export interface LinimasaMeta {
  n_items: number;
  by_event_type: Record<EventType, number>;
  year_min: number | null;
  year_max: number | null;
}

export interface LinimasaResponse {
  items: LinimasaEvent[];
  meta: LinimasaMeta;
}

export const EVENT_TYPE_LABELS: Record<EventType, string> = {
  suksesi: 'Suksesi',
  perjanjian: 'Perjanjian',
  konflik: 'Konflik',
  diplomasi: 'Diplomasi',
  administratif: 'Administratif',
};

export const EVENT_TYPE_ICONS: Record<EventType, string> = {
  suksesi: 'M12 2l2.09 6.26L20 9.27l-4.91 3.82L16.18 20 12 16.77 7.82 20l1.09-6.91L4 9.27l5.91-1.01z',
  perjanjian: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M16 13H8M16 17H8',
  konflik: 'M14.5 17.5L3 6V3h3l11.5 11.5M13 19l6-6M16 16l4 4M19 21l2-2',
  diplomasi: 'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2zM9 7a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75',
  administratif: 'M3 4h18v18H3zM16 2v4M8 2v4M3 10h18',
};

/* ── Chronicle 3-column types ── */

export type PortName =
  | 'Aceh' | 'Barus' | 'Singkil' | 'Nias' | 'Natal'
  | 'Air Bangis' | 'Tiku' | 'Pariaman' | 'Padang' | 'Bayang'
  | 'Salido' | 'Painan' | 'Air Haji' | 'Inderapura';

export interface PortPosition {
  yPct: number;
  xPct: number;
}

export const PORT_POSITIONS: Record<PortName, PortPosition> = {
  'Aceh':        { yPct: 5.0,  xPct: 13.2 },
  'Barus':       { yPct: 43.7, xPct: 43.9 },
  'Singkil':     { yPct: 41.3, xPct: 37.9 },
  'Nias':        { yPct: 52.4, xPct: 36.1 },
  'Natal':       { yPct: 60.6, xPct: 51.1 },
  'Air Bangis':  { yPct: 64.4, xPct: 53.8 },
  'Tiku':        { yPct: 71.1, xPct: 59.4 },
  'Pariaman':    { yPct: 73.6, xPct: 61.2 },
  'Padang':      { yPct: 77.2, xPct: 63.5 },
  'Bayang':      { yPct: 78.7, xPct: 65.2 },
  'Salido':      { yPct: 81.1, xPct: 66.0 },
  'Painan':      { yPct: 82.4, xPct: 66.8 },
  'Air Haji':    { yPct: 85.8, xPct: 68.2 },
  'Inderapura':  { yPct: 88.9, xPct: 69.5 },
};

export const PORT_ORDER: PortName[] = [
  'Aceh', 'Barus', 'Singkil', 'Nias', 'Natal',
  'Air Bangis', 'Tiku', 'Pariaman', 'Padang', 'Bayang',
  'Salido', 'Painan', 'Air Haji', 'Inderapura',
];

export const VOC_ROUTES: [PortName, PortName][] = [
  ['Aceh', 'Barus'], ['Barus', 'Singkil'], ['Singkil', 'Natal'],
  ['Natal', 'Air Bangis'], ['Air Bangis', 'Tiku'], ['Tiku', 'Pariaman'],
  ['Pariaman', 'Padang'], ['Padang', 'Salido'], ['Salido', 'Painan'],
  ['Painan', 'Air Haji'], ['Air Haji', 'Inderapura'],
];

export const ACEH_ORBIT_PORTS: PortName[] = ['Barus', 'Padang', 'Inderapura'];

export const PORT_KEYS: [RegExp, PortName][] = [
  [/barus|baros/i, 'Barus'],
  [/priaman|pariaman/i, 'Pariaman'],
  [/\btiku|ticou|tycou|tikoe/i, 'Tiku'],
  [/padang/i, 'Padang'],
  [/salida|sillida|cillida|salido|cingkuak|chinco|zillida/i, 'Salido'],
  [/painan|pynang|peynang/i, 'Painan'],
  [/indrapoura|indrapura|inderapura|indrapoera/i, 'Inderapura'],
  [/air ?bangis|ayerbang/i, 'Air Bangis'],
  [/natal|natter/i, 'Natal'],
  [/singkil|sinkel|cinkel|chincol|sinckel/i, 'Singkil'],
  [/nias|sillibo|hinako|gomboe|lahomi/i, 'Nias'],
  [/air ?haji|ajerhadj/i, 'Air Haji'],
  [/bayang|bajang/i, 'Bayang'],
  [/atjeh|aceh|atchin|aetchin/i, 'Aceh'],
];

export function portOf(ev: LinimasaEvent): PortName | null {
  const hay = `${ev.title || ''} ${ev.ruler_actor || ''}`;
  for (const [re, port] of PORT_KEYS) if (re.test(hay)) return port;
  return null;
}

export interface ChronicleState {
  activeIndex: number;
  events: LinimasaEvent[];
  eras: Era[];
  yearMin: number;
  yearMax: number;
}

export const YEAR_MIN = 1600;
export const YEAR_MAX = 1775;

export const CONFIDENCE_MAP: Record<string, { text: string; icon: string }> = {
  unverified: {
    text: 'Belum diverifikasi silang',
    icon: 'M12 8v4M12 16h.01',
  },
  verified: {
    text: 'Terverifikasi silang',
    icon: 'M22 11.08V12a10 10 0 1 1-5.93-9.14M22 4L12 14.01l-3-3',
  },
  partial: {
    text: 'Sebagian terverifikasi',
    icon: 'M22 11.08V12a10 10 0 1 1-5.93-9.14M22 4L12 14.01l-3-3',
  },
};
