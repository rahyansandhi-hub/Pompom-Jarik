#!/usr/bin/env python3
"""Pompom & Jarik — EP08 "GABAN" final edit (9:16, 1080x1920, ~60 s, English captions + score).

Run inside the Higgsfield sandbox: python3 build.py  (ffmpeg, numpy, Pillow, Montserrat)
Output: out/ep08_gaban.mp4 (native SFX + music), out/ep08_gaban_no_music.mp4
"""
import os, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CDN = "https://d8j0ntlcm91z4.cloudfront.net/user_3JZP8inL1bd2xvdj2gSu8glteSA/hf_"
FONT = "/usr/share/fonts/truetype/higgsfield/Montserrat-ExtraBold.ttf"
W, H, FPS = 1080, 1920, 30
S = W / 720  # layout is written in 720-wide units and scaled to the output size
YELLOW, RED, BLUE = (255, 212, 0), (235, 40, 60), (40, 150, 255)

# shot, source clip, captions: (start, end, kind, text) relative to the shot
#   kind: "cap" caption, "say:NAME" dialogue, "big" big centre title, "name" name card, "score", "follow"
FLASHBACK_LOOK = ("eq=saturation=0.55:brightness=0.03:contrast=0.95,"
                  "colorchannelmixer=.9:.25:.05:0:.2:.8:.1:0:.15:.2:.7,vignette=PI/4.5")
SHOTS = [
    # 0: flashback from EP07 — Pom-Pom flies with the laundry basket and traps Jimothy
    (0, "20260928_011241_1f39a12d-bc51-4364-aa31-94df7cdb7df9",
     [(0.0, 4.7, "ep", "PREVIOUSLY ON EPISODE 07"), (0.4, 4.6, "cap", "Pom-Pom caught Jimothy...|with a laundry basket!")],
     {"ss": 0.2, "take": 5.5, "speed": 1.1, "look": FLASHBACK_LOOK, "flash_out": True, "vol": 0.7}),
    (1, "20260930_050858_f5e32b7d-2b70-4ac1-bed1-a6d7530f8f31",
     [(0.0, 5.0, "ep", "EPISODE 08 · GABAN"), (0.2, 2.6, "cap", "He lost in Episode 7..."),
      (2.6, 5.0, "cap", "...so he brought|FRIENDS.")]),
    (2, "20260930_050530_566186e6-9b63-433b-8533-5205ba3ae439",
     [(0.4, 5.9, "say:JIMOTHY", "Revenge...|and snacks.")]),
    (3, "20260930_050530_43269443-fcfe-43c4-895b-55b1144c80d7",
     [(0.6, 3.2, "cap", "Pom-Pom charges..."), (3.2, 5.9, "cap", "2 vs 3...|TRAPPED.")]),
    (4, "20260930_050530_cd8abc6d-b6ef-44e1-a243-b32eaed35e5c",
     [(0.4, 3.6, "say:POM-POM", "GABAN...|I need you. NOW."), (3.8, 5.9, "say:GABAN (on the phone)", "Brrrp.")]),
    (5, "20260930_050530_e34fdbab-ae12-43ab-9f9a-2dcb4c1bb4a0",
     [(2.4, 5.9, "big", "THIS IS MY|TERRITORY NOW.")]),
    (6, "20260930_051314_c03ce66d-3fdb-4d59-9b73-748d9042e400",
     [(0.2, 3.2, "name", "GABAN|Maine Coon · Pom-Pom's childhood friend"), (3.3, 5.9, "say:POM-POM", "GABAAAN!")]),
    (7, "20260930_050936_67ae5065-e15a-4b36-964b-90e8e9019b56",
     [(0.3, 4.9, "say:GABAN", "Raccoons love water.|Pond. Together. Ayuh.")]),
    (8, "20260930_050936_14da67a9-72e8-43a4-909b-cfe3cac4c282",
     [(0.2, 4.9, "big", "3 VS 3")]),
    (9, "20260930_052317_df234a8a-b9c3-46d9-9978-49469b429f6e",
     [(0.3, 3.4, "cap", "Grab the shiny bell..."), (6.2, 7.9, "big", "TEAMWORK!")]),
    (10, "20260930_051215_f82605bc-1dbd-4ab9-9854-4d9e34fc7faf",
     [(0.3, 2.8, "say:POM-POM", "We... WON?!"), (2.9, 7.0, "score", ""), (5.2, 7.0, "follow", "@pompomjarik")]),
]


def sh(cmd):
    subprocess.run(cmd, shell=True, check=True)


def probe(path):
    return float(subprocess.check_output(
        f"ffprobe -v error -show_entries format=duration -of csv=p=0 {path}", shell=True))


# ---------------------------------------------------------------- overlays
def font(size):
    return ImageFont.truetype(FONT, int(size * S))


def fit(text, maxsize, maxw):
    s = maxsize
    while s > 20 and font(s).getlength(text) > maxw * S:
        s -= 2
    return font(s)


def ctext(d, y, text, f, fill="white", stroke=6):
    d.text(((W - f.getlength(text)) / 2, y * S), text, font=f, fill=fill, stroke_width=int(stroke * S), stroke_fill="black")


def pill(d, yc, text, size, bg, fg):
    f = font(size)
    tw = f.getlength(text)
    a, b = f.getbbox(text)[1], f.getbbox(text)[3]
    yc, px, py = yc * S, 22 * S, 14 * S
    x0 = (W - tw) / 2 - px
    d.rounded_rectangle([x0, yc - (b - a) / 2 - py, x0 + tw + 2 * px, yc + (b - a) / 2 + py],
                        radius=(b - a) / 2 + py, fill=bg, outline="black", width=int(4 * S))
    d.text(((W - tw) / 2, yc - (b - a) / 2 - a), text, font=f, fill=fg)


def lines_block(d, text, bottom, maxsize=50, maxw=600, fill="white"):
    ls = text.split("|")
    f = min((fit(l, maxsize, maxw) for l in ls), key=lambda f: f.size)
    lh = f.size * 1.22 / S
    y = bottom - lh * len(ls)
    for l in ls:
        ctext(d, y, l, f, fill=fill)
        y += lh
    return bottom - lh * len(ls)


def overlay(kind, text, path):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if kind == "ep":
        pill(d, 175, text, 30, YELLOW, "black")
    elif kind == "cap":
        lines_block(d, text, 1010)
    elif kind.startswith("say:"):
        ls = text.split("|")
        ls[0] = '"' + ls[0]
        ls[-1] = ls[-1] + '"'
        top = lines_block(d, "|".join(ls), 1010)
        pill(d, top - 38, kind[4:], 26, YELLOW, "black")
    elif kind == "big":
        ls = text.split("|")
        f = min((fit(l, 96, 640) for l in ls), key=lambda f: f.size)
        y = 250
        for l in ls:
            ctext(d, y, l, f, fill=YELLOW, stroke=9)
            y += f.size * 1.15 / S
    elif kind == "name":
        name, sub = text.split("|")
        ctext(d, 820, name, fit(name, 120, 620), fill=YELLOW, stroke=9)
        ctext(d, 960, sub, fit(sub, 34, 640), stroke=5)
    elif kind == "score":
        d.rounded_rectangle([110 * S, 190 * S, 610 * S, 470 * S], radius=28 * S, fill=(0, 0, 0, 170), outline=YELLOW, width=int(6 * S))
        ctext(d, 212, "SCORE", font(40), fill=YELLOW, stroke=4)
        ctext(d, 280, "POM-POM  +1", font(62), stroke=6)
        ctext(d, 365, "JARIK  +1", font(62), stroke=6)
    elif kind == "follow":
        ctext(d, 900, "Follow", font(48))
        ctext(d, 965, text, fit(text, 80, 620), fill=YELLOW, stroke=8)
    im.save(path)


# ---------------------------------------------------------------- music (procedural, royalty-free)
SR = 44100
rng = np.random.default_rng(8)


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tt(dur):
    return np.arange(int(dur * SR)) / SR


def ks(m, dur=0.5, decay=0.995):
    p = max(2, int(SR / mtof(m)))
    n = int(dur * SR)
    y = np.zeros(n + p + 2)
    nz = rng.uniform(-1, 1, p + 1)
    y[:p + 1] = 0.5 * (nz + np.roll(nz, 1))
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
    return np.sin(2 * np.pi * np.cumsum(45 + 90 * np.exp(-t * 28)) / SR) * np.exp(-t * 9)


def snare():
    t = tt(0.25)
    return 0.55 * np.diff(rng.standard_normal(len(t)), prepend=0) / 2 * np.exp(-t * 22) + \
        0.4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30)


def hat():
    t = tt(0.06)
    return np.diff(np.diff(rng.standard_normal(len(t) + 2))) / 4 * np.exp(-t * 70)


def bass(m, dur=0.4):
    t = tt(dur)
    f = mtof(m)
    env = np.minimum(1, t / 0.005) * np.exp(-t * 4)
    env[-300:] *= np.linspace(1, 0, 300)
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t)) * env


def brass(m, dur):
    t = tt(dur)
    ph = 2 * np.pi * np.cumsum(mtof(m) * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * t))) / SR
    env = np.minimum(1, t / 0.05) * np.clip((dur - t) / 0.15, 0, 1)
    return sum(np.sin(k * ph) / k ** 1.25 for k in range(1, 10)) * env * 0.35


def pad(ms, dur):
    t = tt(dur)
    env = np.minimum(1, t / 0.6) * np.clip((dur - t) / 0.6, 0, 1)
    return sum(np.sin(2 * np.pi * mtof(m) * t) + 0.3 * np.sin(4 * np.pi * mtof(m) * t) for m in ms) * env * 0.25


def whistle(m, dur):
    t = tt(dur)
    f = mtof(m) * (1 + 0.006 * np.sin(2 * np.pi * 6 * t) * (t > 0.1))
    env = np.minimum(1, t / 0.05) * np.clip((dur - t) / 0.1, 0, 1)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env * 0.5


def noise_sweep(dur, up=True):
    n = int(dur * SR)
    x, y, acc = rng.standard_normal(n), np.zeros(n), 0.0
    a = np.linspace(0.01, 0.5, n) if up else np.linspace(0.4, 0.01, n)
    for i in range(n):
        acc += a[i] * (x[i] - acc)
        y[i] = acc
    return y / (np.abs(y).max() + 1e-9) * (np.linspace(0, 1, n) ** 2 if up else np.sin(np.pi * np.arange(n) / n))


def crash(dur=1.6):
    t = tt(dur)
    return np.diff(rng.standard_normal(len(t)), prepend=0) / 2 * np.exp(-t * 2.2)


def build_music(st, total):
    out = np.zeros(int((total + 2) * SR))

    def add(sig, t, g=1.0):
        i = int(t * SR)
        if 0 <= i < len(out):
            j = min(len(out), i + len(sig))
            out[i:j] += g * sig[:j - i]

    def impact(t, g=1.0):
        add(kick(), t, g)
        add(crash(), t, 0.35 * g)
        add(bass(33, 0.9), t, 0.6 * g)

    def drums(t0, t1, busy=False, g=1.0):
        tb = t0
        while tb < t1 - 0.05:
            for dt, fn, gg in [(0, kick, .9), (1, kick, .9), (.5, snare, .55), (1.5, snare, .55)] + \
                    ([(.75, kick, .5), (1.75, snare, .3)] if busy else []):
                if tb + dt < t1:
                    add(fn(), tb + dt, gg * g)
            for e in range(8 if busy else 4):
                dt = e * (0.25 if busy else 0.5)
                if tb + dt < t1:
                    add(hat(), tb + dt, 0.22 * g)
            tb += 2.0

    # 0) flashback: soft music-box memory theme, then a whoosh into the present
    add(pad([48, 55, 64], st[1] - 0.2), 0.0, 0.6)
    t, k = 0.0, 0
    while t < st[1] - 0.6:
        add(ks([72, 76, 79, 84, 79, 76][k % 6], 0.6, 0.997), t, 0.3)
        t += 0.4
        k += 1
    add(noise_sweep(0.6), st[1] - 0.6, 0.3)
    # A) shots 1-2: sneaky heist in A minor (pizzicato + walking bass)
    walk = [45, 48, 50, 52, 45, 48, 51, 52]
    t, k = st[1], 0
    while t < st[3] - 0.1:
        add(bass(walk[k % 8], 0.24), t, 0.55)
        if k % 2 == 0:
            add(ks([69, 72, 76, 72][(k // 2) % 4], 0.25, 0.98), t + 0.25, 0.35)
        add(hat(), t, 0.18)
        t += 0.25 * 2
        k += 1
    # B) shots 3-4: tension drone + ticking, hopeful lift at the end of the call
    add(pad([45, 52, 57], st[5] - st[3] - 1.2), st[3], 0.8)
    t = st[3]
    while t < st[5] - 1.2:
        add(ks(81, 0.08, 0.9), t, 0.25)
        t += 0.5
    add(noise_sweep(1.2), st[5] - 1.2, 0.35)
    # C) shots 5-6: sunrise hero theme (C major brass), ducked under GABAN's yowl
    impact(st[5], 0.8)
    for i, (ms, d) in enumerate([([60, 64, 67], 1.6), ([65, 69, 72], 1.6), ([67, 71, 74], 2.8)]):
        for m in ms:
            add(brass(m, d), st[5] + [0, 1.6, 3.2][i], 0.28)
    impact(st[6], 0.6)
    for i, m in enumerate([67, 72, 76, 79, 76, 72]):
        add(brass(m, 0.9), st[6] + i * 1.0, 0.35)
    add(pad([48, 55, 60, 64], st[7] - st[6]), st[6], 0.7)
    # D) shot 7: team huddle — building drums
    drums(st[7], st[8], g=0.8)
    add(noise_sweep(1.0), st[8] - 1.0, 0.3)
    # E) shot 8: western standoff — lonely whistle over a low drone
    add(pad([40, 47], st[9] - st[8]), st[8], 0.6)
    t = st[8] + 0.3
    for m, d in [(76, .5), (81, .5), (76, .5), (81, 1.2), (79, .4), (77, .4), (76, 1.0)]:
        add(whistle(m, d), t, 0.3)
        t += d
    # F) shot 9: team action groove, impact on the splash
    impact(st[9], 0.9)
    drums(st[9], st[10] - 0.2, busy=True, g=1.0)
    t, k = st[9], 0
    while t < st[10] - 0.3:
        add(bass([45, 45, 48, 50][k % 4], 0.22), t, 0.5)
        t += 0.25
        k += 1
    impact(st[9] + 6.0, 1.0)
    # G) shot 10: victory fanfare + score ding
    impact(st[10], 0.7)
    for i, m in enumerate([60, 64, 67, 72]):
        add(brass(m, 0.25), st[10] + i * 0.18, 0.5)
    for m in [60, 64, 67, 72]:
        add(brass(m, total - st[10] - 1.0), st[10] + 0.8, 0.3)
    add(ks(88, 1.0, 0.998), st[10] + 2.9, 0.5)
    add(ks(91, 1.0, 0.998), st[10] + 3.1, 0.5)

    out = out[:int(total * SR)]
    fade = int(0.8 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)
    out = np.tanh(out / (np.abs(out).max() + 1e-9) * 1.3)
    out = out / np.abs(out).max() * 0.85
    pcm = (np.repeat(out[:, None], 2, axis=1) * 32767).astype(np.int16)
    with wave.open("music.wav", "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


# ---------------------------------------------------------------- main
def main():
    for dn in ["src", "ovl", "seg", "out"]:
        os.makedirs(dn, exist_ok=True)
    with open("dl.txt", "w") as f:
        f.write("\n".join(s[1] for s in SHOTS))
    sh(f"xargs -P 10 -I{{}} sh -c '[ -s src/{{}}.mp4 ] || curl -sfL -o src/{{}}.mp4 {CDN}{{}}.mp4' < dl.txt")

    enc = f"-r {FPS} -c:v libx264 -preset slow -crf 17 -profile:v high -pix_fmt yuv420p -c:a aac -ar 48000 -ac 2 -b:a 192k"
    base = (f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
            f"unsharp=5:5:0.6:5:5:0.0,fps={FPS},setsar=1")
    segs, st, t = [], {}, 0.0
    for n, src, caps, *rest in SHOTS:
        o = rest[0] if rest else {}
        sp = o.get("speed", 1.0)
        dur = o["take"] / sp if "take" in o else probe(f"src/{src}.mp4")
        st[n] = t
        t += dur
        vpre = f"setpts=PTS/{sp}," if sp != 1.0 else ""
        look = "," + o["look"] if "look" in o else ""
        flash = f",fade=out:st={dur - 0.3:.3f}:d=0.3:color=white" if o.get("flash_out") else ""
        apost = (f",atempo={sp}" if sp != 1.0 else "") + f",volume={o.get('vol', 1.0)}"
        cut = f"-ss {o['ss']} -t {o['take']} " if "take" in o else ""
        inputs, chain, last = "", f"[0:v]{vpre}{base}{look}{flash}[v0]", "v0"
        for j, (a, b, kind, text) in enumerate(caps):
            p = f"ovl/{n:02d}_{j}.png"
            overlay(kind, text, p)
            inputs += f" -loop 1 -t {dur:.3f} -i {p}"
            b = min(b, dur - 0.02)
            chain += (f";[{j + 1}:v]format=rgba,fade=in:st={a}:d=0.18:alpha=1,fade=out:st={b - 0.15}:d=0.15:alpha=1[o{j}]"
                      f";[{last}][o{j}]overlay=0:0:enable='between(t,{a},{b})'[v{j + 1}]")
            last = f"v{j + 1}"
        out = f"seg/{n:02d}.mp4"
        sh(f"ffmpeg -nostdin -loglevel error -y {cut}-i src/{src}.mp4{inputs} -filter_complex \"{chain};"
           f"[0:a]aresample=48000,aformat=channel_layouts=stereo{apost}[a]\" -map [{last}] -map [a] {enc} -t {dur:.3f} {out}")
        segs.append(out)
    st[11] = t
    with open("list.txt", "w") as f:
        f.write("".join(f"file '{s}'\n" for s in segs))
    sh("ffmpeg -nostdin -loglevel error -y -f concat -safe 0 -i list.txt -c:v copy -c:a aac -b:a 192k all.mp4")

    build_music(st, t)
    loud = "loudnorm=I=-14:TP=-1.5:LRA=11"
    # native SFX (yowl, splash...) stay on top; music sits under them, lower during the yowl (shot 5)
    duck = f"volume='if(between(t,{st[5]},{st[6]}),0.35,0.55)':eval=frame"
    sh("ffmpeg -nostdin -loglevel error -y -i all.mp4 -i music.wav -filter_complex "
       f"\"[0:a]volume=1.0[a0];[1:a]{duck}[a1];[a0][a1]amix=inputs=2:normalize=0:duration=first,{loud}[a]\" "
       "-map 0:v -map [a] -c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart out/ep08_gaban.mp4")
    sh(f"ffmpeg -nostdin -loglevel error -y -i all.mp4 -af {loud} -c:v copy -c:a aac -b:a 192k -ar 48000 "
       "-movflags +faststart out/ep08_gaban_no_music.mp4")
    print("SHOT STARTS", {k: round(v, 2) for k, v in st.items()})
    print("TOTAL %.2fs" % t)


if __name__ == "__main__":
    main()
