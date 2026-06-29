// Sumber kebenaran tunggal untuk konten homepage.
// Edit di sini → otomatis berlaku di /  (ID) dan /en/  (EN).
// Jangan tulis teks langsung di index.astro atau en/index.astro.

export const home = {
  id: {
    hero: {
      title:    'Salido, Enklave Emas Kolonial',
      subtitle: 'Sejarah tambang emas Nagari Salido dan batas kemampuan VOC di Pesisir Minangkabau — abad ke-17 hingga ke-20.',
      cta:      'Mulai membaca ↓',
      ctaHref:  '/sejarah',
    },
    intro: {
      heading: 'Nagari Salido',
      p1: 'Salido — atau Sillida dalam ejaan VOC — adalah sebuah nagari kecil di pantai barat Sumatra yang pernah mencuri perhatian dua kekuatan kolonial besar. Cadangan emas di kaki Gunung Arum menjadi taruhan yang tidak pernah terbayar.',
      p2: 'Portal ini mengumpulkan riset, dokumen arsip, dan peta interaktif untuk merekonstruksi sejarah yang terlupakan dari eksperimen kolonial yang gagal.',
      cta:     'Baca sejarahnya',
      ctaHref: '/sejarah',
      imgAlt:  'Bentangan alam Kampung Tambang, kaki Gunung Arum, Nagari Salido',
      imgCaption: 'Kampung Tambang, kaki Gunung Arum',
    },
    teaser: {
      quote: '...banyak persediaan emas yang sangat halus dari Monancabo, dan dari sini diyakini sebagai emas yang dicari Sulaiman untuk pembangunan Bait Suci.',
      cite:  '— Relação da Viagem e Naufrágio da Nao S. Paulo, abad ke-16',
      body:  'Salido adalah salah satu titik di pantai barat Sumatra yang disebut menyimpan emas itu. Ketika VOC tiba pada 1681 — membawa insinyur, denah lubang tambang, dan ratusan budak — yang mereka temukan bukan harta legenda.',
      cta:     'Baca prolog — dari Ofir hingga Gunung Arum',
      ctaHref: '/sejarah',
    },
    atlas: {
      heading: 'Atlas Jalur VOC',
      body:    'Lacak 4.700+ pelayaran VOC di Sumatra Barat, 1700–1790. Filter berdasarkan komoditas, arah, dan dekade.',
      cta:     'Buka Atlas',
      ctaHref: '/atlas',
    },
    footer: {
      copy: 'Riset historis Nagari Salido, Pesisir Minangkabau',
    },
  },

  en: {
    hero: {
      title:    'Salido, The Colonial Gold Enclave',
      subtitle: 'History of the Salido gold mines and the limits of VOC power on the Minangkabau Coast — 17th to 20th century.',
      cta:      'Start reading ↓',
      ctaHref:  '/en/history',
    },
    intro: {
      heading: 'Nagari Salido',
      p1: 'Salido — or Sillida in VOC spelling — is a small village on the west coast of Sumatra that once attracted the attention of two major colonial powers. The gold deposits at the foot of Mount Arum became a wager that was never repaid.',
      p2: 'This portal gathers research, archival documents, and interactive maps to reconstruct the forgotten history of a failed colonial experiment.',
      cta:     'Read the history',
      ctaHref: '/en/history',
      imgAlt:  'Kampung Tambang, the old mining village at the foot of Mount Arum',
      imgCaption: 'Kampung Tambang, foot of Mount Arum',
    },
    teaser: {
      quote: '...there is a great supply of very fine gold from Monancabo, and from here it is believed to be the gold sought by Solomon for the building of the Temple.',
      cite:  '— Relação da Viagem e Naufrágio da Nao S. Paulo, 16th century',
      body:  'Salido was one of the points on the west coast of Sumatra said to hold this gold. When the VOC arrived in 1681 — bringing engineers, mine shaft blueprints, and hundreds of enslaved workers — what they found was not legendary treasure.',
      cta:     'Read the prologue — from Ophir to Mount Arum',
      ctaHref: '/en/history',
    },
    atlas: {
      heading: 'VOC Trade Atlas',
      body:    'Track 4,700+ VOC voyages in West Sumatra, 1700–1790. Filter by commodity, direction, and decade.',
      cta:     'Open Atlas',
      ctaHref: '/atlas',
    },
    footer: {
      copy: 'Historical research — Nagari Salido, Minangkabau Coast',
    },
  },
} as const;
