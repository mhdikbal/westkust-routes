# Runbook Production — www Kanonik + HTTP/3 (salido.my.id)

**Referensi keputusan:** [ADR-001](adr-001-www-http3-redis.md) — www → apex 301,
HTTP/3 hanya di Cloudflare edge (QUIC origin TIDAK diaktifkan).

**Eksekutor:** PO / operator dengan akses Cloudflare + SSH production.
**Sifat:** Langkah MANUAL. Jangan dijalankan oleh agent/CI otomatis.

**Target server:** `ubuntu@103.171.184.94` port `22142` (alias SSH: `westkust-prod`)
**Path config production:** `/etc/nginx/conf.d/salido.conf`
**Sumber config:** `~/salido-web/nginx-prod.conf` (repo lokal, versi terbaru)

---

## Prasyarat

- [ ] `nginx-prod.conf` di repo `~/salido-web` sudah memuat server block
      redirect `www.salido.my.id` → `https://salido.my.id` (301) sesuai ADR-001.
- [ ] Akses login Cloudflare untuk zone `salido.my.id`.
- [ ] SSH key untuk `westkust-prod` tersedia.
- [ ] Simpan salinan config lama sebelum mulai (lihat Langkah 3a).

---

## Langkah 0 — Deploy situs salido-web (konten Wave 2–3)

Dari WSL — build + rsync `dist/` + reload nginx (otomatis via skrip):

```bash
cd ~/salido-web && ./deploy.sh
```

Verifikasi cepat: `curl -s -o /dev/null -w "%{http_code}\n" https://salido.my.id/jurnal/` → 200,
lalu cek https://salido.my.id/sejarah/historiografi di browser.

## Langkah 1 — Cloudflare DNS: CNAME www

1. Login Cloudflare → pilih zone `salido.my.id` → **DNS → Records**.
2. Tambah record:
   - **Type:** `CNAME`
   - **Name:** `www`
   - **Target:** `salido.my.id`
   - **Proxy status:** **Proxied** (orange-cloud) — WAJIB, jangan DNS-only.
3. Save. (Propagasi via Cloudflare instan karena proxied.)

## Langkah 2 — Cloudflare: aktifkan HTTP/3

1. Dashboard Cloudflare zone `salido.my.id` → **Network**.
2. Aktifkan toggle **"HTTP/3 (with QUIC)"**.
3. Catatan: ini HANYA edge. Sesuai ADR-001, JANGAN mengaktifkan
   `listen 443 quic` / buka UDP 443 di origin.

## Langkah 3 — Deploy config Nginx ke origin

### 3a. Backup config lama (WAJIB sebelum overwrite)

```bash
ssh westkust-prod
sudo cp /etc/nginx/conf.d/salido.conf /etc/nginx/conf.d/salido.conf.bak-$(date +%Y%m%d-%H%M)
exit
```

### 3b. Salin config baru dari repo lokal

Dari mesin lokal (WSL), di direktori `~/salido-web`:

```bash
scp -P 22142 ~/salido-web/nginx-prod.conf ubuntu@103.171.184.94:/tmp/salido.conf
# atau, dengan alias SSH:
scp ~/salido-web/nginx-prod.conf westkust-prod:/tmp/salido.conf
```

### 3c. Pasang, test, reload

```bash
ssh westkust-prod
sudo mv /tmp/salido.conf /etc/nginx/conf.d/salido.conf
sudo nginx -t && sudo systemctl reload nginx
```

Jika `nginx -t` GAGAL: JANGAN reload. Lanjut ke bagian Rollback.

## Langkah 4 — Verifikasi

Dari mesin lokal:

```bash
# (a) www → apex 301, path dipertahankan
curl -sI https://www.salido.my.id/x
#   Harus: HTTP/2 301 (atau HTTP/3 301)
#   Header: location: https://salido.my.id/x

# (b) Alt-Svc mengiklankan h3 (disuntik Cloudflare edge)
curl -sI https://salido.my.id | grep -i alt-svc
#   Harus memuat: h3=":443"
```

Di browser (Chrome/Edge):

1. Buka DevTools → tab **Network** → klik kanan header kolom → centang **Protocol**.
2. Muat `https://salido.my.id` dua kali (kunjungan pertama bisa masih h2;
   browser pindah h3 setelah membaca Alt-Svc).
3. Kolom Protocol harus menampilkan **h3** untuk request dokumen utama.

Sanity check tambahan:

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://salido.my.id/          # 200
curl -s -o /dev/null -w "%{http_code}\n" https://salido.my.id/api/voyages/  # 200
```

---

## Rollback

Jika ada 5xx / redirect loop / `nginx -t` gagal setelah deploy:

```bash
ssh westkust-prod
sudo cp /etc/nginx/conf.d/salido.conf.bak-<timestamp> /etc/nginx/conf.d/salido.conf
sudo nginx -t && sudo systemctl reload nginx
```

- Rollback DNS: record CNAME `www` boleh dibiarkan (aman — server block lama
  sudah melayani www), atau hapus record jika ingin kembali persis ke kondisi awal.
- Rollback HTTP/3: matikan toggle "HTTP/3 (with QUIC)" di Cloudflare Network
  (tidak memengaruhi origin; browser otomatis kembali ke h2).
- Verifikasi pasca-rollback: `curl -sI https://salido.my.id` → 200.
