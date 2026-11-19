# gta6-meme-x

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/isnalestari09/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/isnalestari09/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 meme for the make.fun bounty "Post a GTA 6 meme on X". The joke: the make.fun ghost has been waiting on a Vice City beach for GTA 6 since 2013 — and it is still waiting. The picture is drawn in code (`scripts/make_meme.py`, Python + PIL): a synthwave sunset, a neon skyline, a beach umbrella, and the official make.fun ghost mascot (from the make.fun press kit) standing on the sand. No Rockstar logo or official GTA artwork is used.

The meme is posted on X from the public account [@Kancilxyz](https://x.com/Kancilxyz), with make.fun and the play code in the post text. `POST.json` at the repository root names the post; `main.ts` copies it to `/output` for the gate.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Regenerate the meme

```sh
python3 scripts/make_meme.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=7fcw42xg&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
