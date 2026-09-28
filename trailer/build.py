#!/usr/bin/env python3
"""Pompom & Jarik — trailer EP01-EP07 (9:16, untuk diposting @rahyansandhi).

Menjalankan: python3 build.py   (butuh ffmpeg, numpy, Pillow, font Montserrat ExtraBold)
Output: out/trailer_pompomjarik.mp4, out/trailer_tanpa_musik.mp4, out/cover.jpg
"""
import json, os, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CDN = "https://d8j0ntlcm91z4.cloudfront.net/user_3JZP8inL1bd2xvdj2gSu8glteSA/hf_"
FONT = "/usr/share/fonts/truetype/higgsfield/Montserrat-ExtraBold.ttf"
W, H, FPS = 720, 1280, 30
YELLOW, RED = (255, 212, 0), (235, 40, 60)

EPISODES = {
    1: "TOKO ROTI", 2: "SIRKUS", 3: "SUPERMARKET", 4: "ROBOT PENYEDOT",
    5: "BALAS DENDAM", 6: "JEBAKAN GELAS", 7: "TAMU TENGAH MALAM",
}

# name, source clip, start (s), duration (s), keep native audio, episode, caption ("|" = line break)
EDL = [
    ("hookA", "20260921_053419_4d64eda4-e275-4e95-8a49-710b66d57630", 1.2, 1.6, 0, 0, ""),
    ("hookB", "20260921_053419_4d64eda4-e275-4e95-8a49-710b66d57630", 2.8, 1.7, 0, 0, ""),
    ("title", "20260921_235917_7e917414-23a9-4f95-ae54-be6c312b1ab5", 0.3, 3.2, 0, 0, ""),
    ("e1a", "20260921_051324_6621759a-01a6-46a2-9f3f-a919e9030e23", 1.5, 2.6, 0, 1, "Jarik nemu ceri|raksasa..."),
    ("e1b", "20260921_053419_3fa4785a-80d5-482d-b370-9ece9cb8bf30", 1.6, 3.0, 0, 1, "Jebakan tepung?|Kena sendiri."),
    ("e1c", "20260921_053729_7808c3d2-167d-45e9-811b-90a5ae72f62a", 2.0, 3.0, 0, 1, "Ngumpet di mixer...|ikut diaduk."),
    ("e2a", "20260921_235918_2d697d2f-f907-41c7-8d54-e22d29a70edc", 1.2, 2.6, 0, 2, "Salaman damai...|tapi jarinya nyilang."),
    ("e2b", "20260922_001009_bb05a27f-ca77-48f9-b451-cd6cde60c7ec", 2.3, 3.6, 0, 2, "Jebakan sirkus|makan tuan."),
    ("e2c", "20260921_235917_c4f265e2-f00e-42d0-843b-44aee6b72f94", 0.6, 2.6, 0, 2, "Yang masuk kandang:|Pom-Pom."),
    ("e3a", "20260922_121446_40836902-e5b7-435d-87f3-bbdccc8287bc", 1.8, 2.8, 0, 3, "Susu ramuan bikin|Jarik... BEROTOT?!"),
    ("e3b", "20260922_121446_06f9ffd2-1a2b-4828-9f0f-d5613273fdeb", 1.6, 2.8, 0, 3, "Pom-Pom|dibanting."),
    ("e3c", "20260922_122056_4e685712-81e0-4854-88a5-6f734f288969", 1.0, 2.8, 0, 3, "Nyoba ramuannya...|malah menciut."),
    ("e4a", "20260924_150900_9bc8b31c-4a55-4c6c-a36f-dabf2cd29774", 5.6, 2.8, 0, 4, "Beli robot|pemburu tikus..."),
    ("e4b", "20260924_150900_26bbe8fa-4ed2-4285-b6fd-c81b93422c4e", 0.0, 1.6, 0, 4, "...robotnya|dibajak Jarik."),
    ("e4c", "20260924_150900_26bbe8fa-4ed2-4285-b6fd-c81b93422c4e", 4.4, 3.0, 0, 4, "Yang kesedot?|Pom-Pom."),
    ("e5a", "20260925_095652_17dbecd8-3c34-457c-928c-059117a0aab5", 3.2, 2.2, 1, 5, "Benteng bantal?|Disedot habis."),
    ("e5b", "20260925_095653_2d8cc21e-a046-4d11-aad3-ef6cfba690ed", 6.8, 3.0, 1, 5, "Kabur ke kulkas...|tetap kesedot."),
    ("e5c", "20260925_103050_9218d04f-8b60-4370-9a62-59e6912b798e", 3.3, 2.4, 1, 5, "Meledak dari|kantong debu!"),
    ("e6a", "20260926_193925_731fdac4-03d2-43e7-bce5-48d60cbbbc93", 7.8, 3.8, 1, 6, "Akhirnya...|KETANGKEP!"),
    ("e6b", "20260926_195025_906b70f4-8250-4f5c-af2e-648843ea3739", 5.2, 2.6, 1, 6, "Eh... Jarik|punya ide."),
    ("e6c", "20260926_194732_8a89ceda-1b90-46b5-9d77-97030586de76", 2.2, 2.8, 1, 6, "Kalah lagi."),
    ("e7a", "20260928_011259_ab133fde-0462-40d8-94e7-0a891ddaf4ce", 0.2, 3.4, 1, 7, "Tengah malam...|ada tamu."),
    ("e7b", "20260928_011241_e7cfb403-17ee-44c6-9928-8e1f4958c07a", 1.7, 3.2, 1, 7, "Pai-nya|dihabisin."),
    ("e7c", "20260928_011259_ab133fde-0462-40d8-94e7-0a891ddaf4ce", 7.6, 2.4, 1, 7, "Mangkok kesayangan|diembat!"),
    ("e7d", "20260928_012312_cd580b1c-49eb-4659-8fd8-6b061517f92e", 1.0, 3.6, 1, 7, "Kucing & tikus...|GENCATAN SENJATA?!"),
    ("e7e", "20260928_011241_1f39a12d-bc51-4364-aa31-94df7cdb7df9", 0.2, 2.8, 1, 7, "Operasi rebut|mangkok dimulai!"),
    ("cliff", None, 0, 1.2, 0, 0, ""),
    ("end", "20260928_020107_f088e908-3f45-4e8f-bd07-c1e6f5147359", 3.2, 4.8, 0, 0, ""),
]


def sh(cmd):
    subprocess.run(cmd, shell=True, check=True)


# ---------------------------------------------------------------- overlays
def font(size):
    return ImageFont.truetype(FONT, size)


def fit(text, maxsize, maxw):
    s = maxsize
    while s > 20 and font(s).getlength(text) > maxw:
        s -= 2
    return font(s)


def ctext(d, y, text, f, fill="white", stroke=6):
    x = (W - f.getlength(text)) / 2
    d.text((x, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill="black")


def pill(d, yc, text, size, bg, fg):
    f = font(size)
    tw = f.getlength(text)
    a, b = f.getbbox(text)[1], f.getbbox(text)[3]
    padx, pady = 22, 14
    x0 = (W - tw) / 2 - padx
    d.rounded_rectangle([x0, yc - (b - a) / 2 - pady, x0 + tw + 2 * padx, yc + (b - a) / 2 + pady],
                        radius=(b - a) / 2 + pady, fill=bg, outline="black", width=4)
    d.text(((W - tw) / 2, yc - (b - a) / 2 - a), text, font=f, fill=fg)


def caption(d, cap, bottom=985, maxw=560):
    lines = cap.split("|")
    f = min((fit(l, 50, maxw) for l in lines), key=lambda f: f.size)
    lh = int(f.size * 1.22)
    y = bottom - lh * len(lines)
    for l in lines:
        ctext(d, y, l, f)
        y += lh


def make_overlay(name, ep, cap):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if ep:
        tag = "EPISODE %02d" % ep + ("  ·  TERBARU" if ep == 7 else "")
        pill(d, 190, tag, 28, YELLOW, "black")
        ctext(d, 240, EPISODES[ep], fit(EPISODES[ep], 62, 600))
        caption(d, cap)
    elif name == "hookA":
        ctext(d, 250, "1 KUCING.", font(78))
        ctext(d, 345, "1 TIKUS.", font(78))
    elif name == "hookB":
        ctext(d, 250, "NOL KEMENANGAN", fit("NOL KEMENANGAN", 78, 600), fill=YELLOW)
        ctext(d, 345, "buat si kucing.", fit("buat si kucing.", 60, 560))
    elif name == "title":
        pill(d, 175, "SERIES KOMEDI ANIMASI", 28, YELLOW, "black")
        ctext(d, 220, "POMPOM", fit("POMPOM", 130, 620), stroke=8)
        ctext(d, 360, "& JARIK", fit("& JARIK", 130, 620), fill=YELLOW, stroke=8)
    elif name == "cliff":
        ctext(d, 560, "Berhasil nggak, ya...?", fit("Berhasil nggak, ya...?", 56, 600))
    elif name == "end":
        pill(d, 330, "7 EPISODE SUDAH TAYANG", 32, YELLOW, "black")
        ctext(d, 420, "Tonton series", font(60))
        ctext(d, 500, "lengkapnya di", font(60))
        ctext(d, 610, "@pompomjarik", fit("@pompomjarik", 92, 560), fill=YELLOW, stroke=8)
        pill(d, 800, "FOLLOW SEKARANG", 40, RED, "white")
        ctext(d, 880, "EP 01 – EP 07", font(34), stroke=4)
    im.save("ovl/%s.png" % name)


# ---------------------------------------------------------------- video segments
def render_segment(i, seg):
    name, src, ss, dur, keep_audio, ep, cap = seg
    out = "seg/%02d_%s.mp4" % (i, name)
    enc = "-r %d -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -ar 48000 -ac 2 -b:a 192k -t %.3f" % (FPS, dur)
    base = "scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,fps=%d,setsar=1" % (W, H, W, H, FPS)
    first_of_ep = ep and EDL[i - 1][5] != ep
    flash = ",fade=in:st=0:d=0.18:color=white" if first_of_ep else ""
    ovl = "[1:v]format=rgba,fade=in:st=0:d=0.2:alpha=1[o]"
    if name == "cliff":
        sh(f"ffmpeg -nostdin -loglevel error -y -f lavfi -i color=black:s={W}x{H}:r={FPS}:d={dur} "
           f"-loop 1 -t {dur} -i ovl/{name}.png -f lavfi -t {dur} -i anullsrc=r=48000:cl=stereo "
           f"-filter_complex \"{ovl};[0:v][o]overlay=0:0[v]\" -map [v] -map 2:a {enc} {out}")
    elif name == "end":
        sh(f"ffmpeg -nostdin -loglevel error -y -ss {ss} -i src/{src}.mp4 -frames:v 1 end_bg.png")
        sh(f"ffmpeg -nostdin -loglevel error -y -loop 1 -t {dur} -i end_bg.png -loop 1 -t {dur} -i ovl/{name}.png "
           f"-f lavfi -t {dur} -i anullsrc=r=48000:cl=stereo -filter_complex "
           f"\"[0:v]{base},boxblur=18:2,eq=brightness=-0.22:saturation=1.1[b];"
           f"[1:v]format=rgba,fade=in:st=0.1:d=0.35:alpha=1[o];[b][o]overlay=0:0,fade=in:st=0:d=0.15:color=white[v]\" "
           f"-map [v] -map 2:a {enc} {out}")
    else:
        vf = f"[0:v]{base},eq=saturation=1.08:contrast=1.03[b];{ovl};[b][o]overlay=0:0{flash}[v]"
        if keep_audio:
            extra = ""
            vf += ";[0:a]aresample=48000,aformat=channel_layouts=stereo,apad[a]"
            amap = "-map [a]"
        else:
            extra = f"-f lavfi -t {dur} -i anullsrc=r=48000:cl=stereo"
            amap = "-map 2:a"
        sh(f"ffmpeg -nostdin -loglevel error -y -ss {ss} -t {dur + 0.2} -i src/{src}.mp4 -loop 1 -t {dur} "
           f"-i ovl/{name}.png {extra} -filter_complex \"{vf}\" -map [v] {amap} {enc} {out}")
    return out


# ---------------------------------------------------------------- music (procedural, royalty-free)
SR = 44100
rng = np.random.default_rng(7)


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tt(dur):
    return np.arange(int(dur * SR)) / SR


def ks(m, dur=0.5, decay=0.995, soft=1):
    p = max(2, int(SR / mtof(m)))
    n = int(dur * SR)
    y = np.zeros(n + p + 2)
    nz = rng.uniform(-1, 1, p + 1)
    for _ in range(soft):
        nz = 0.5 * (nz + np.roll(nz, 1))
    y[:p + 1] = nz
    k = p + 1
    while k < len(y):
        e = min(len(y), k + p)
        y[k:e] = decay * 0.5 * (y[k - p:e - p] + y[k - p - 1:e - p - 1])
        k = e
    y = y[:n]
    y[-200:] *= np.linspace(1, 0, 200)
    return y


def kick():
    t = tt(0.35)
    f = 45 + 90 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def snare():
    t = tt(0.25)
    nz = np.diff(rng.standard_normal(len(t)), prepend=0) / 2
    return 0.55 * nz * np.exp(-t * 22) + 0.4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30)


def hat(dur=0.06):
    t = tt(dur)
    nz = np.diff(np.diff(rng.standard_normal(len(t) + 2))) / 4
    return nz * np.exp(-t * (70 if dur < 0.1 else 18))


def bass(m, dur=0.4):
    t = tt(dur)
    f = mtof(m)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
    env = np.minimum(1, t / 0.005) * np.exp(-t * 4)
    env[-300:] *= np.linspace(1, 0, 300)
    return s * env


def brass(m, dur):
    t = tt(dur)
    f = mtof(m) * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * t) * (t > 0.15))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = sum(np.sin(k * ph) / k ** 1.25 for k in range(1, 11))
    env = np.minimum(1, t / 0.04) * (0.85 + 0.15 * np.exp(-t * 6))
    env *= np.clip((dur - t) / 0.12, 0, 1)
    return s * env * 0.35


def lp_sweep(n, a0, a1, a2=None):
    x = rng.standard_normal(n)
    a = np.linspace(a0, a1, n) if a2 is None else np.concatenate([np.linspace(a0, a1, n // 2), np.linspace(a1, a2, n - n // 2)])
    y = np.zeros(n)
    acc = 0.0
    for i in range(n):
        acc += a[i] * (x[i] - acc)
        y[i] = acc
    return y / (np.abs(y).max() + 1e-9)


def whoosh(dur=0.45):
    n = int(dur * SR)
    return lp_sweep(n, 0.01, 0.35, 0.01) * np.sin(np.pi * np.arange(n) / n) ** 2


def crash(dur=1.8):
    t = tt(dur)
    return np.diff(rng.standard_normal(len(t)), prepend=0) / 2 * np.exp(-t * 2.2)


def riser(dur):
    t = tt(dur)
    f = 150 * (8 ** (t / dur))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return (0.6 * lp_sweep(len(t), 0.01, 0.6) + 0.3 * tone) * (t / dur) ** 2


def build_music(tl):
    total = tl["total"]
    out = np.zeros(int((total + 2) * SR))

    def add(sig, t, g=1.0):
        i = int(t * SR)
        if 0 <= i < len(out):
            j = min(len(out), i + len(sig))
            out[i:j] += g * sig[:j - i]

    def impact(t, g=1.0):
        add(kick(), t, 1.0 * g)
        add(crash(), t, 0.35 * g)
        add(bass(36, 0.8), t, 0.6 * g)

    # 1) hook: tik-tok tension + chromatic pizzicato
    t0, hook_end = 0.0, tl["hook_end"]
    k = 0
    while t0 + k * 0.25 < hook_end - 0.05:
        add(hat(), t0 + k * 0.25, 0.25 if k % 2 else 0.4)
        if k % 2 == 0:
            add(ks(48 + k // 4, 0.3, 0.99), t0 + k * 0.25, 0.8)
        k += 1
    add(riser(0.8), hook_end - 0.8, 0.35)
    impact(hook_end)

    # 2) title fanfare
    te = tl["title_end"]
    for j, m in enumerate([60, 64, 67]):
        add(brass(m, 0.2), hook_end + j * 0.16, 0.9)
    for m in [60, 64, 67, 72]:
        add(brass(m, te - hook_end - 0.75), hook_end + 0.5, 0.55)
    for j in range(12):
        add(snare(), te - 0.75 + j * 0.0625, 0.15 + 0.5 * j / 12)
    add(whoosh(), te - 0.3, 0.5)

    # 3) main groove C-Am-F-G until EP07
    chords = [(48, [72, 76, 79, 76, 74, 72, 67, None]), (45, [69, 72, 76, 72, 74, 76, 72, None]),
              (41, [77, 76, 72, 69, 72, 74, 76, None]), (43, [79, 77, 76, 74, 71, 74, 67, None])]

    gain = tl["gain"]  # < 1 where the clips carry their own score: keep only drums there

    def groove_bar(tb, root, mel, stop):
        for (dt, fn, gg) in [(0, kick, 0.9), (1.0, kick, 0.9), (1.75, kick, 0.5), (0.5, snare, 0.6), (1.5, snare, 0.6)]:
            if tb + dt < stop:
                add(fn(), tb + dt, gg * gain(tb + dt))
        for e in range(8):
            if tb + e * 0.25 < stop:
                add(hat(), tb + e * 0.25, (0.28 if e % 2 else 0.18) * gain(tb + e * 0.25))
        for dt, iv in [(0, 0), (0.5, 7), (1.0, 12), (1.5, 7)]:
            if tb + dt < stop and gain(tb + dt + 0.42) >= 1:
                add(bass(root + iv, 0.42), tb + dt, 0.55)
        for e, m in enumerate(mel):
            if m and tb + e * 0.25 < stop - 0.1 and gain(tb + e * 0.25 + 0.45) >= 1:
                add(ks(m, 0.45, 0.994), tb + e * 0.25, 0.5)

    tb, bar, ep7 = te, 0, tl["ep_starts"][6]
    while tb < ep7 - 0.1:
        groove_bar(tb, *chords[bar % 4], stop=ep7 - 0.05)
        tb += 2.0
        bar += 1
    for s in tl["ep_starts"][1:]:
        add(whoosh(), s - 0.25, 0.45)
        add(crash(1.0), s, 0.12)

    # 4) EP07 heist groove (A minor) until the slow-mo shot, then riser
    impact(ep7, 0.8)
    heist = [[45, 45, 48, 50, 52, 52, 55, 52], [45, 45, 48, 50, 52, 52, 55, 52],
             [50, 50, 53, 55, 57, 57, 60, 57], [52, 52, 56, 59, 52, 52, 56, 59]]
    rs = tl["riser_start"]
    tb, bar = ep7, 0
    while tb < rs - 0.05:
        g = gain(tb)
        for e, m in enumerate(heist[bar % 4]):
            t = tb + e * 0.25
            if t < rs:
                if g >= 1:
                    add(bass(m - 12 if m > 50 else m, 0.22), t, 0.6)
                add(hat(), t, (0.3 if e % 2 else 0.15) * g)
        for dt, fn, gg in [(0, kick, 0.9), (0.75, kick, 0.6), (1.0, kick, 0.9), (0.5, snare, 0.6), (1.5, snare, 0.6)]:
            if tb + dt < rs:
                add(fn(), tb + dt, gg * g)
        for dt in [0.25, 1.25]:
            if tb + dt < rs and g >= 1:
                for m in ([69, 72, 76] if bar % 4 < 2 else [62, 65, 69] if bar % 4 == 2 else [64, 68, 71]):
                    add(ks(m, 0.2, 0.98), tb + dt, 0.3 * g)
        tb += 2.0
        bar += 1
    add(riser(tl["ep7_end"] - rs), rs, 0.55)
    add(ks(88, 1.2, 0.998), tl["ep7_end"] + 0.1, 0.25)   # "ting" di layar hitam

    # 5) end card: stinger + theme + final chord
    ce = tl["cliff_end"]
    impact(ce, 1.0)
    tb = ce + 0.1
    for c in [chords[0], chords[3]]:
        groove_bar(tb, *c, stop=total - 1.4)
        tb += 2.0
    for m in [60, 64, 67, 72]:
        add(brass(m, 1.3), total - 1.4, 0.55)
    add(crash(), total - 1.4, 0.3)
    add(kick(), total - 1.4, 0.9)

    out = out[:int(total * SR)]
    fade = int(0.35 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)
    out = np.tanh(out / (np.abs(out).max() + 1e-9) * 1.4)
    out = out / np.abs(out).max() * 0.89
    pcm = (np.repeat(out[:, None], 2, axis=1) * 32767).astype(np.int16)
    with wave.open("music.wav", "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


# ---------------------------------------------------------------- main
def main():
    for dname in ["src", "ovl", "seg", "out"]:
        os.makedirs(dname, exist_ok=True)
    srcs = sorted({s[1] for s in EDL if s[1]})
    with open("dl.txt", "w") as f:
        f.write("\n".join(srcs))
    sh(f"xargs -P 8 -I{{}} sh -c '[ -s src/{{}}.mp4 ] || curl -sfL -o src/{{}}.mp4 {CDN}{{}}.mp4' < dl.txt")

    segs = []
    for i, seg in enumerate(EDL):
        make_overlay(seg[0], seg[5], seg[6])
        segs.append(render_segment(i, seg))
    with open("list.txt", "w") as f:
        f.write("".join("file '%s'\n" % s for s in segs))
    sh("ffmpeg -nostdin -loglevel error -y -f concat -safe 0 -i list.txt -c:v copy -c:a aac -b:a 192k all.mp4")

    # timeline (from EDL durations)
    starts, t = {}, 0.0
    for seg in EDL:
        starts[seg[0]] = t
        t += seg[3]
    total = t
    ep_starts = [starts["e%da" % e] for e in range(1, 8)]
    native = (starts["e5a"], starts["cliff"])
    tl = {
        "total": total, "hook_end": starts["title"], "title_end": starts["e1a"], "ep_starts": ep_starts,
        "riser_start": starts["e7e"], "ep7_end": starts["cliff"], "cliff_end": starts["end"],
        "gain": lambda x: 0.5 if native[0] - 0.2 <= x < native[1] else 1.0,
    }
    build_music(tl)
    json.dump({k: v for k, v in tl.items() if k != "gain"}, open("out/timeline.json", "w"), indent=1)

    loud = "loudnorm=I=-14:TP=-1.5:LRA=11"
    sh("ffmpeg -nostdin -loglevel error -y -i all.mp4 -i music.wav -filter_complex "
       f"\"[0:a]volume=1.1[a0];[1:a]volume=0.8[a1];[a0][a1]amix=inputs=2:normalize=0:duration=first,{loud}[a]\" "
       "-map 0:v -map [a] -c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart out/trailer_pompomjarik.mp4")
    sh(f"ffmpeg -nostdin -loglevel error -y -i all.mp4 -af {loud} -c:v copy -c:a aac -b:a 192k -ar 48000 "
       "-movflags +faststart out/trailer_tanpa_musik.mp4")
    sh("ffmpeg -nostdin -loglevel error -y -ss %.2f -i out/trailer_pompomjarik.mp4 -frames:v 1 -q:v 2 out/cover.jpg"
       % (starts["title"] + 2.0))
    print("TOTAL %.2fs" % total)


if __name__ == "__main__":
    main()
