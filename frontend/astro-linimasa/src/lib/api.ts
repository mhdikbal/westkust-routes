import type { LinimasaResponse } from './types';

// Client-side: use relative URL (goes through nginx proxy)
// SSR/build-time: use internal Docker URL if needed
const API_BASE = (typeof window === 'undefined')
  ? (import.meta.env?.PUBLIC_API_BASE_URL || 'http://backend:8000')
  : '';

export async function fetchLinimasa(): Promise<LinimasaResponse> {
  const res = await fetch(`${API_BASE}/api/research/linimasa`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function fetchLinimasaFiltered(
  params: { event_type?: string; year_from?: number; year_to?: number } = {}
): Promise<LinimasaResponse> {
  const qs = new URLSearchParams();
  if (params.event_type) qs.set('event_type', params.event_type);
  if (params.year_from != null) qs.set('year_from', String(params.year_from));
  if (params.year_to != null) qs.set('year_to', String(params.year_to));
  const res = await fetch(`${API_BASE}/api/research/linimasa?${qs}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}
