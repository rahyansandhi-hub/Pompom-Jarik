# Trailer Pompom & Jarik — EP01 s/d EP07

Trailer vertikal (9:16, 720×1280, 30fps, ±78 detik) untuk diposting di **@rahyansandhi**, mengarahkan penonton ke **@pompomjarik**.

| File | Link |
|---|---|
| Trailer (dengan musik) | https://d2ol7oe51mr4n9.cloudfront.net/user_3JZP8inL1bd2xvdj2gSu8glteSA/91399d70-8e06-4fbf-b37b-2c55fd405405.mp4 |
| Trailer tanpa musik tambahan (untuk pakai sound trending di TikTok/IG) | https://d2ol7oe51mr4n9.cloudfront.net/user_3JZP8inL1bd2xvdj2gSu8glteSA/8ba8061d-47d7-4a80-b242-255a80f7615b.mp4 |
| Cover / thumbnail | https://d2ol7oe51mr4n9.cloudfront.net/user_3JZP8inL1bd2xvdj2gSu8glteSA/ca4909ca-c537-4a9b-979c-d061891b48e0.jpg |

Semua klip diambil dari generasi Higgsfield yang sudah ada; tidak ada generasi baru (0 kredit). Musik latar disintesis secara prosedural di `build.py` (bebas royalti).

## Storyboard

| Waktu | Bagian | Teks di layar |
|---|---|---|
| 0:00 | Hook (Pom-Pom nyungsep ke kue) | 1 KUCING. 1 TIKUS. → NOL KEMENANGAN buat si kucing. |
| 0:03 | Judul (salam penonton di sirkus) | SERIES KOMEDI ANIMASI · POMPOM & JARIK |
| 0:06 | EP01 Toko Roti | Jarik nemu ceri raksasa… / Jebakan tepung? Kena sendiri. / Ngumpet di mixer… ikut diaduk. |
| 0:15 | EP02 Sirkus | Salaman damai… tapi jarinya nyilang. / Jebakan sirkus makan tuan. / Yang masuk kandang: Pom-Pom. |
| 0:24 | EP03 Supermarket | Susu ramuan bikin Jarik… BEROTOT?! / Pom-Pom dibanting. / Nyoba ramuannya… malah menciut. |
| 0:32 | EP04 Robot Penyedot | Beli robot pemburu tikus… / …robotnya dibajak Jarik. / Yang kesedot? Pom-Pom. |
| 0:40 | EP05 Balas Dendam | Benteng bantal? Disedot habis. / Kabur ke kulkas… tetap kesedot. / Meledak dari kantong debu! |
| 0:47 | EP06 Jebakan Gelas | Akhirnya… KETANGKEP! / Eh… Jarik punya ide. / Kalah lagi. |
| 0:57 | EP07 Tamu Tengah Malam (terbaru) | Tengah malam… ada tamu. / Pai-nya dihabisin. / Mangkok kesayangan diembat! / Kucing & tikus… GENCATAN SENJATA?! / Operasi rebut mangkok dimulai! |
| 1:12 | Cliffhanger (layar hitam) | Berhasil nggak, ya…? |
| 1:13 | End card | 7 EPISODE SUDAH TAYANG · Tonton series lengkapnya di @pompomjarik · FOLLOW SEKARANG |

Judul episode (Toko Roti, Sirkus, dst.) adalah judul deskriptif; ganti di `EPISODES` pada `build.py` bila judul resminya berbeda, lalu render ulang.

## Caption posting (@rahyansandhi)

```
7 episode, 1 kucing, 1 tikus… dan Pom-Pom BELUM PERNAH MENANG 😭🐭🐱
Episode 07 baru tayang — kali ini mereka terpaksa kerja sama?!

Tonton series lengkapnya (EP01–EP07) di @pompomjarik 👉 follow biar nggak ketinggalan episode berikutnya!

#pompomjarik #animasi #kartun #kucingvstikus #animasiindonesia #fyp
```

Tips: tag/collab @pompomjarik di postingan, dan sematkan komentar "Full episode ada di @pompomjarik 👆".

## Render ulang

Butuh ffmpeg, numpy, Pillow, dan font Montserrat ExtraBold (path di `FONT`). Script mengunduh klip dari CDN Higgsfield:

```
python3 build.py   # hasil di out/
```
