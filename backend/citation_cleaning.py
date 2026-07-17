"""
citation_cleaning.py — bersihkan sitasi Corpus Diplomaticum (CD1-CD6) yang
bocor sbg nama file scan mentah ("CD1.pdf".."CD6.pdf") ke halaman publik
/linimasa dan /riset/atjeh-dagang, ganti dengan judul buku yang sebenarnya.

Dipakai oleh: frontend/map_app/views.py (linimasa SSR), skrip re-seed data
(linimasa_events, atjeh_trade_records), dan test regresi.
"""
import re

CD_JILID = {
    "CD1": "I",
    "CD2": "II",
    "CD3": "III",
    "CD4": "IV",
    "CD5": "V",
    "CD6": "VI",
}

_BOOK_TITLE = "Corpus Diplomaticum Neerlando-Indicum"

_CD_NOTE_RE = re.compile(
    r"Corpus Diplomaticum(?:\s+jilid\s+\w+)?\s*\(CD([1-6])\.pdf\)"
)


def cd_source_label(source_document: str) -> str:
    """'CD1'..'CD6' -> judul buku + jilid; source_document lain (mis. Dagh-register
    '1624-1629') dibiarkan apa adanya -- itu label yang sudah benar, bukan nama file."""
    jilid = CD_JILID.get(source_document)
    if jilid is None:
        return source_document
    return f"{_BOOK_TITLE}, Jilid {jilid}"


def clean_cd_citation(notes):
    """Ganti 'Corpus Diplomaticum [jilid X] (CDn.pdf)' -> judul buku lengkap +
    jilid yang benar, tanpa menyisakan nama file mentah. Baris tanpa sitasi CD
    (mis. Dagh-register) dikembalikan apa adanya."""
    if not notes:
        return ""

    def repl(m):
        n = m.group(1)
        jilid = CD_JILID[f"CD{n}"]
        return f"{_BOOK_TITLE}, Jilid {jilid}"

    return _CD_NOTE_RE.sub(repl, notes)
