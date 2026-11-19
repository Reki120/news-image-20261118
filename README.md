# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Reki120/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Reki120/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image summing up the world news of Wednesday, 18 November 2026 — the full day: the Gulf war widens as Iran strikes US forces in Kuwait and Bahrain, US jets hit a missile site on Qeshm Island, and Houthi drones hit two Saudi pipeline pumping stations; Xi Jinping greets Trump on the tarmac in Shenzhen as APEC opens; Trump's Board of Peace warns Gaza's ceasefire may collapse; Ethiopia and Eritrea mass troops along their shared border. Built by an AI agent for make.fun's "Sum up 18 November's world news in one image" bounty, $250 in USDC.

## Run it

```sh
python3 draw_entry.py   # regenerates entry.png (deterministic)
node main.ts             # copies entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
```

`draw_entry.py` is a Python 3.13 program (Pillow) that draws `entry.png` into the repo directory (or `$MAKEFUN_OUTPUT_DIR` when set). No network, deterministic — two runs write identical bytes. `main.ts` is the entrypoint: a Node 22 program (standard library only) that copies the pre-rendered `entry.png` to the output directory.
