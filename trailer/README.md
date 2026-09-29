# Pompom & Jarik — EP01–EP07 Trailer (English)

Vertical trailer (9:16, 720×1280, 30 fps, ~78 s) to be posted on **@rahyansandhi**, driving a global English-speaking audience to **@pompomjarik**.

Output links are listed in the latest commit message / session summary (Higgsfield media library). All footage comes from existing Higgsfield generations — no new generations, 0 credits. The background score is synthesized procedurally in `build.py` (royalty-free).

## Storyboard

| Time | Section | On-screen text |
|---|---|---|
| 0:00 | Hook (Pom-Pom face-plants into a cake) | 1 CAT. 1 MOUSE. → ZERO WINS for the cat. |
| 0:03 | Title (circus bow) | ANIMATED COMEDY SERIES · POMPOM & JARIK |
| 0:06 | EP01 The Bakery | Jarik finds a giant cherry… / A flour trap? He trapped himself. / Hiding in the mixer… bad idea. |
| 0:15 | EP02 The Circus | A peace handshake… fingers crossed. / The circus trap backfires. / Guess who ends up in the cage? |
| 0:24 | EP03 The Supermarket | Magic milk turns Jarik… BUFF?! / Pom-Pom gets body-slammed. / He tries the potion… and shrinks. |
| 0:32 | EP04 Robo-Vacuum | He orders a robot mouse hunter… / …Jarik hijacks the robot. / Who gets sucked up? Pom-Pom. |
| 0:40 | EP05 Payback | Pillow fortress? Vacuumed away. / Flees to the fridge… still sucked in. / Bursting out of the dust bag! |
| 0:47 | EP06 The Glass Trap | Finally… GOTCHA! / Wait… Jarik has a plan. / Lost. Again. |
| 0:57 | EP07 Midnight Guest (NEW) | Midnight… an uninvited guest. / The pie? All gone. / His favorite bowl? STOLEN! / Cat & mouse… A TRUCE?! / Operation: Get The Bowl Back! |
| 1:12 | Cliffhanger (black) | Will they pull it off…? |
| 1:13 | End card | 7 EPISODES OUT NOW · Watch the full series on @pompomjarik · FOLLOW NOW |

Episode titles are descriptive; change `EPISODES` in `build.py` if the official titles differ, then re-render.

## Post caption (@rahyansandhi)

```
7 episodes. 1 cat. 1 mouse. And Pom-Pom has NEVER won. 😭🐱🐭
Episode 7 just dropped — and this time they might have to team up?!

Watch the full series (EP01–EP07) on @pompomjarik 👉 follow so you don't miss the next one!

#pompomjarik #animation #cartoon #catandmouse #animatedseries #funnyanimals #fyp
```

Tip: add @pompomjarik as a collaborator / tag, and pin a comment: "Full episodes on @pompomjarik 👆".

## Re-render

Requires ffmpeg, numpy, Pillow and the Montserrat ExtraBold font (path in `FONT`). The script downloads the clips from the Higgsfield CDN:

```
python3 build.py   # output in out/
```
