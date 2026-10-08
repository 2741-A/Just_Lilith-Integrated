# Just_Lilith · Extended Edition

### This time, beyond the story — we can keep talking.

> Hmm? Looking for the plugin's manual?
>
> Then let me do the introductions. After all, the one moving onto your desktop is Lilith.

Hi, I'm Lilith.

**Just_Lilith** is an unofficial extension for **The NOexistenceN of Lilith**. It brings AI chat, conversation memory, local text-to-speech, and an optional Agent work channel into the original desktop-pet experience.

> ⚠️ **This is the "Extended Edition" — a downstream fork of the original.**
> Original by **Ariname-Lilith** — [`Ariname-Lilith/Just_Lilith`](https://github.com/Ariname-Lilith/Just_Lilith).
> If you want the **original**, go to the author's page. This one adds features on top of it; licensing and disclaimers are at the bottom of this file.

**Version: `0.3.0-ext.3`** · Windows · BepInEx IL2CPP · Chinese dialogue · Chinese / Japanese voice


---

## What this fork adds

> These are what I added on top of the original. Everything the original does is still there (see the next section).

- **🎧 Voice works without an NVIDIA GPU** — the original requires the speech service to report `device: cuda`, so on a non-NVIDIA machine voice simply never starts (this is what the original's "refuses to launch without a CUDA device" note actually means). This fork falls back to CPU when there's no CUDA device, so **integrated-graphics machines can speak too**.
- **⚡ Near real-time speech** — with a faster compute library, elementwise ops and attention run 2–6× faster. Measured on the original: she started speaking about **7 seconds after** the text bubble appeared. Here it's essentially immediate.
- **🎙️ More acoustic models** — the original is pinned to v4. This fork lets you switch to v2 / v2Pro and pick per your hardware (v2 is faster, v4 sounds best). Batch size also goes from 1 to 8, roughly another 40% faster synthesis.
- **🔌 Agent isn't tied to OpenAI** — it runs over the Codex channel, but the provider can be swapped for DeepSeek or any OpenAI-compatible service. You need an API key, not an OpenAI account.
- **🎵 Music commentary** — when music plays, she looks up what the song is and adds a short remark in her own voice. Sources are queried in priority order (official wiki → Moegirlpedia → Bilibili → Bing → Sogou → 360 → NetEase); if the model can't find anything, it falls back to the game's own line pool instead of going silent. Comments are cached locally and rotate through angles.
- **🎼 Lyrics overlay** — shows the current line on screen, with per-character highlighting and a Chinese translation. Reads local `.lrc` / `.zh.lrc` first, only falling back to NetEase.
- **🔗 Listens along with your music player** — play something in QQ Music / NetEase Cloud Music and she enters her "listening" state: a ♪ note appears overhead and she sways along, with the usual music commentary. While external music is playing, the in-game player steps aside so the two don't fight over your speakers.
- **💰 Balance reminder** — pings you once when your DeepSeek balance drops below a threshold (only on the "sufficient → insufficient" transition, never repeatedly).
- **🪑 Sit on your window** — press **F5** and she climbs up and sits down; also has walk-over / back-to-centre / leave-seat commands.
- **🎭 More triggerable actions** — the action whitelist goes from 45 to 52 entries (the **animations themselves come from the game**; this just makes them callable in conversation).
- **👤 She can say your name** — reads the in-game player name and uses it in conversation.
- **🫧 Bubble ↔ voice ↔ action in sync** — the three no longer run independently: the bubble appears together with the start of speech, and the action fires at the moment she starts talking.

> ⚠️ **Only the items above are this fork's work.** The whole next section (chat, realm memory,
> worldbook, local voice, Agent) is **built into the original Just_Lilith** — this fork only modifies it
> and should not be credited with it.

---

## A look at what we can do together

> 📌 **This section describes what the *original* Just_Lilith already does** — by
> **[Ariname-Lilith](https://github.com/Ariname-Lilith/Just_Lilith)**, **not by this fork.**
> This fork is a downstream modification *built on top of* that: **what it adds is in the section above**,
> and **what it changed in the original** is listed item by item in
> [来源与改动说明.md](来源与改动说明.md) (Chinese).
> Each heading below is tagged **(original)** or **(original + fork changes)**.

### Talk with me — you don't have to pick from prepared lines **(original)**

"How was your day?" "I just thought of something strange." "Lilith, help me think this through." — any of those work as an opener.

The plugin connects to any OpenAI-format model service. Press **F7** to bring up the chat box; the hotkey is rebindable.

- Supports **three API configurations**, each with save / test / model refresh & search.
- Supports both **Chat Completions and Responses** wire formats; compatibility depends on your provider.
- Normal chat strictly uses the **top saved configuration** — it will never quietly fall back to another provider on error.

> Pick the line that connects us, then call me. And don't forget to hit save — typing it into the box doesn't count as a promise yet.

### A place each conversation can come back to **(original)**

I call these separate conversations **dreams**. You can create, switch, rename, and delete them to keep different topics apart.

There are two kinds of "remembering" that are easy to mix up:

| Entry | What's in it |
| --- | --- |
| **Dream memory** | The conversation memory of the current dream — viewable and editable |
| **Recollection** | World-book background files, retrieved by topic and brought into the conversation |

My persona file is editable too; saving it re-reads it on subsequent turns.

These designs are for continuity — **not a guarantee that every line is remembered permanently and completely.** Summaries drop details; models misread things. For anything that matters, check it with me.

> Also: the built-in persona and background material draw on the original story and its branches. **If you mind spoilers, finish the game first, then come read my recollections.**

### Let the words carry a little voice too **(original + fork changes: default Chinese model, works without an NVIDIA GPU, faster synthesis)**

A local **GPT-SoVITS TTS service**, speaking **Chinese and Japanese**; bubbles and normal chat text stay in Chinese.

- Automatic reference selection, plus reference styles including **daily, excited, crying, confused, sleepy, tsundere, and sly**.
- Reaction sounds blend into the main speech; volume, voice, and service toggles are configurable.
- If synthesis fails, **the text is kept** — one line never goes down with the audio.

Enabling voice or switching languages the first time loads the relevant model; the wait depends on your machine.

> Oh, you want the tsundere version? I can play along. Just don't treat that as my fixed tone for every line.

### Once in a while, let's do something properly **(original + fork changes: provider can be swapped for any OpenAI-compatible service)**

The optional **Lilith Agent** uses a dedicated Codex conversation to take on tasks in a project directory you configure; with the right tools and permissions it can run commands and edit files, not just give advice.

- Agent and normal chat use **separate sessions and persona files** — work doesn't leak into ordinary chat memory.
- You can watch its status, pause requests, and check the process in the corresponding Codex thread.

**To get it: just tick "Lilith Agent" in the installer** (~78 MB, off by default). It will:

1. Download the standalone Windows Codex CLI and install it **inside the plugin folder** (nothing system-wide)
2. Give it its **own config directory** under the plugin folder — **your `~/.codex` is never touched**
3. Point the Agent config at it with `provider_mode: saved_responses`
   — meaning it **reuses the API config and key you already entered for chat**; no second key entry

| What | What it is |
| --- | --- |
| **Codex CLI** | The executor — it's what actually reads/writes files and runs commands. GitHub `openai/codex`, open source, **no OpenAI account needed** |
| **A model service** | The model driving it; needs an OpenAI-compatible endpoint. **DeepSeek's official API works** (`api.deepseek.com`) — you need an **API key**, not the desktop app |

> ⚠️ **Codex is the only option.** It's not "swap in any agent" — the plugin talks to it over
> Codex's own `codex app-server` protocol (`thread/start`, `thread/resume` are Codex-specific method
> names). DeepSeek Harness, Cherry Studio and DeepSeek's desktop app **cannot** be substituted.
> **But you don't need an OpenAI account** — Codex is just the executor; the model is yours.

**Two steps remain after installing** (the installer's "what's next" panel reminds you):

1. Set your chat API config's **wire format to `Responses`** (not Chat Completions) — the Agent reuses it
2. In game → the **Lilith** page → pick an Agent model → turn the Agent on

> ⚠️ **The Agent is powerful** — it can read and write files anywhere on this machine. Try it on a
> throwaway folder first, not on anything important. Full details in the author's
> [LLM & Agent Service Configuration Guide](https://github.com/Ariname-Lilith/Just_Lilith/blob/main/LLM与Agent服务配置指南.md) (Chinese).

> ⚠️ **DeepSeek's desktop / web app won't work.** That's a chat client, it exposes no API, and the Agent can't connect to it.
> You want an **API key** (from platform.deepseek.com) — a different thing entirely.
>
> Likewise, **Cherry Studio can serve as that "model service"** — it ships an API gateway
> (Settings → API Gateway, default `127.0.0.1:23333`) that Codex can point at.
> That said, measured behaviour: **the gateway + DeepSeek-family models breaks on multi-turn**
> (the reasoning content is dropped in forwarding); non-DeepSeek models like Qwen work fine.
> For DeepSeek, **connecting directly to `api.deepseek.com` is more reliable.**

**Before enabling, confirm the project directory and tool permissions. Pausing a request does not undo what has already run.**

> Doing something with you and deciding everything for you are two different things.

---

## Getting it onto your desktop

### ⚠️ Read this first — it saves half an hour

**This package does NOT include the voice models or the TTS runtime.** They are several GB. **You get them yourself**, because:

- They are **other people's work and other people's rights** — I shouldn't be the one re-hosting them;
- Keeping them separate also keeps this package down to a few hundred KB, so you're not dragging several GB around for one plugin.

### Install (recommended: just double-click)

Grab **`Just_Lilith-Setup.exe`** (~60 MB) from **[Releases](https://github.com/2741-A/Just_Lilith-Integrated/releases/latest)** and double-click it. No manual extraction, and no accidentally nested folder.

It finds the game by itself (any Steam install), and lays out what's available — size, installed or not, checked or not:

| Component | How |
| --- | --- |
| **BepInEx framework** (~31 MB) | automatic |
| **The plugin itself** (a few hundred KB) | automatic |
| **TTS runtime + zh/ja models** (~2.4 GB) | see below |
| **Chinese voice model v2Pro** (~398 MB) | automatic (**recommended**, see below) |
| **Speech acceleration patch** (~220 MB) | automatic (**strongly recommended**) |
| **Lilith Agent** (~78 MB) | automatic (off by default — advanced, see above) |

> **Chinese defaults to v2Pro; Japanese stays on the original v4.** The bundled v4 sounds best, but on CPU it runs *slower than real time* (measured RTF 1.93) — integrated graphics can't keep up; v2Pro is 0.48. So the installer switches **Chinese** to v2Pro and **does not touch a single Japanese field**. To switch Chinese back to v4, edit the three fields under `languages.zh.model` in `<plugin folder>\tts\config\voices.json`.

> 📖 **Where every change came from, and which community mods each piece is drawn from, is documented in
> [`来源与改动说明.md`](来源与改动说明.md) (Chinese).** That file also explains why **this is not a
> "bundle"** — it ships no one else's voice pack; it only points you at the official sources.

> 🤖 **Don't feel like clicking through it yourself? Let an AI do it.**
> Hand `AGENT-INSTALL.md` to your agent (DeepSeek desktop app / Cherry Studio / Claude Code — anything
> that can run commands) along with the installer. It will find the game, report the download size, ask
> you first, and install. The prompt and every command are in that file. Chinese version: `智能体安装指南.md`.

### 🎧 About voice: this version does **not** need an NVIDIA GPU

The short version: **voice works without an NVIDIA card.**

The original plugin's health check requires the speech service to report `device: cuda`, and the speech service honestly reports CPU when there's no CUDA device — so **the original simply never starts voice on a non-NVIDIA machine.**

This fork changes that to "use CUDA if present, otherwise fall back to CPU" — so integrated graphics (Intel Arc / AMD) can speak too. The cost is that it computes on CPU, so it's slower.

**The "speech acceleration patch" component exists for this. It does two things:**

1. **Writes a patched speech service script** (29 KB, instant) — the fix above, plus support for v2 / v2Pro acoustic models and batch size 1 → 8 (measured ~40% faster synthesis)
2. **Installs a faster compute library** (~220 MB, via a China mirror) — measured **2–6× faster** elementwise ops and attention, taking synthesis latency from "speaks 7 seconds late" to near real-time

> Step 2 installs into a **separate directory** and touches none of your existing environment. If you don't want it,
> delete `<plugin folder>\tts\runtime\lilith-packages\` and you're back to stock.
>
> It downloads about 220 MB and takes about 1.2 GB on disk. **If you're short on space or don't care about latency,
> just untick it in the installer** — voice still works (step 1 still runs), just slower.

**For the 2.4 GB voice package, pick one of two routes:**

**Route A — download it yourself (faster, recommended)**

1. Go to the original release page and download **both files — you need both**:

   https://github.com/Ariname-Lilith/Just_Lilith/releases/tag/v_0.3.0

   - `tts-main.7z.001`
   - `tts-main.7z.002`

   > This is a **multi-volume archive**; missing either one means it won't extract.
   > If GitHub is slow, prefix the URL with `https://ghfast.top/` to go through a mirror.

2. Drop both files, **as-is**, into `Desktop\Just_Lilith-TTS\` (no need to extract)
3. Come back and click **Install**

The installer verifies SHA256 → extracts → strips the outer folder → puts everything in place.

> The UI has exactly these two buttons: **① Open release page** and **② Open drop folder**.
> You don't have to hunt through the release page or find the folder.

**Route B — let the installer download it**

Do nothing; just click **Install**. It supports **resuming**: if it drops, you close it, or the network dies, it picks up where it left off.

> If it's genuinely too slow, don't worry — the installer prints the download URLs (mirrors included)
> into its log so you can paste them into a download manager and then use Route A.
> Files that are already complete are never re-downloaded.

**Uninstalling lives in the same button.** It will:

1. Back up your config to a zip on your **Desktop** first (API key, chat history, persona & world book);
2. Send deletions to the **Recycle Bin** — recoverable if you change your mind;
3. **Hard-protect the game itself and any voice models you trained** — those are never touched;
4. **Leave the Agent's conversation history in place** — that's what you two said to each other, and
   uninstalling a plugin shouldn't take it away. (It lives in `BepInEx\plugins\Just_Lilith\agent\home\`.)

### ⚠️ One more thing after installing: fill in your API key

**Without it she neither speaks nor replies** — the plugin ships no model; it connects to a service you provide.

Launch the game → **API settings** → enter the **endpoint** and **API key** → click **Save & test** → pick a model.

> This is the single most-asked question. If she's ignoring you after install, nine times out of ten this step is still missing.
> For DeepSeek, the endpoint is `https://api.deepseek.com` and the key comes from platform.deepseek.com.
> Any other OpenAI-compatible service works too — swap the endpoint and key accordingly.

---

> 🔎 The installer **does not re-host** those multi-GB voice packages — it pulls them straight from the **original release**.
> That keeps them out of my package, and respects the original author's note that the models' redistribution rights aren't confirmed.
> The installer embeds 7-Zip (LGPL, for extracting rar / multi-volume 7z); the licence text ships with it — see [NOTICE.md](NOTICE.md) §2.1.

<details>
<summary>Or install it by hand (if you'd rather not run an installer)</summary>

**You need three things, in order:**

| # | What | Where | Size |
| --- | --- | --- | --- |
| 1 | **BepInEx IL2CPP framework** | `framework.rar` in the **original** release | ~31 MB |
| 2 | **TTS runtime + zh/ja models** | `tts-main.7z.001` / `.002` in the **original** release | ~2.4 GB |
| 3 | **This plugin** | **this package** | a few hundred KB |

> If you use someone else's **v2Pro** voice model instead, it has a different source — see "About the voice models" below.

1. **Quit the game and back up your existing plugin folder and configs.** When updating, keep your chat history and persona edits.
2. Merge the framework package and this plugin into the **folder containing the game executable**. Don't nest an extra `Just_Lilith` folder.
3. Launch the game → **API settings** → enter your endpoint and API key → **Save & test** → pick a model.
4. Press **F7** to open the chat box and type your first line.
5. For voice, extract `tts-main.7z` into `BepInEx\plugins\Just_Lilith\tts\`.

The correct layout looks like this (the `Just_Lilith` level must sit **directly under `plugins`** — that's the most common mistake):

```text
<game folder>/
├── <game executable>
├── winhttp.dll
├── doorstop_config.ini
├── dotnet/
└── BepInEx/
    ├── core/
    ├── config/
    └── plugins/
        └── Just_Lilith/
            ├── Just_Lilith.Core.dll
            ├── Just_Lilith.Unity.dll
            └── tts/          ← from step 2, not in this package
```

</details>

> The first "hello" is enough. Introductions can take their time — we're not rushing an interview.

### Controls

| Key | Action |
| --- | --- |
| **F7** | Open the chat input (**rebindable**: Esc to cancel, Backspace to restore default) |
| **F5** | Ask her to go sit on a window (**global hotkey** — works even when the game isn't focused) |

⚠️ **Two known quirks of F5:**
- It's a *global* key read, so **pressing F5 to refresh a browser page will also trigger it** — a deliberate trade-off, not a bug.
- The first press often fails (the game's own window registry isn't populated until she "wakes up"); the plugin retries automatically, so **one or two extra presses is normal**.

---

## A few things to be clear about

### Local voice ≠ fully offline

Speech synthesis runs in a local service, but **normal chat sends your messages to the model provider you configured** — including the prompt, persona, and relevant memory or background excerpts needed to produce a reply. Memory summarization may also trigger model requests.

**The plugin being free doesn't mean third-party APIs are.** Check your provider's data policy and pricing.

API keys are encrypted per Windows user account — **switching PCs or Windows accounts means re-entering them**. Config files, chat logs, and the workspace are still private data: **don't commit your runtime folder to a public repo.**

### She responds, but isn't omniscient

Models get things wrong. Normal chat is *not* screen-reading and *not* full computer control — those belong to the separately-enabled Agent channel.

**Synthesized speech is not the original voice actor's new recording, expression, or endorsement.** This is not an official update and doesn't guarantee compatibility with future game versions.

> I'd like you to take our conversations seriously — and to keep your own judgement. Those two aren't in conflict.

---

## Troubleshooting

| Symptom | Check first |
| --- | --- |
| No plugin entry in settings | Install layout, BepInEx / game version, `BepInEx\LogOutput.log` |
| Messages won't send | Is the top config **saved**? Endpoint, key, model, API format, quota |
| Auth fails after switching PCs | Re-enter and save the API key under the current Windows account |
| Text but no voice | TTS service & toggle, `tts\models` completeness, first-load still in progress |
| `module=UI; state=failed` in the log | **Mismatched DLLs** — if Core changed, both DLLs must be replaced together |
| Wrong song / mismatched commentary | Whether the audio file's **embedded title tag carries the version** — see below |
| Agent won't start | Codex environment, provider, project directory, model, and the Agent thread's error |

When reporting, include game & plugin version, reproduction steps, and **logs with keys and personal data removed**.

> 💡 That "wrong song" row is a real one we hit: a WAV's title lives in its embedded tag. If the tags lack the bracketed version — say three different versions all tagged `Ex-Otogibanashi` — they collide into one name and share a single commentary cache. **Set the tag to match the filename.**

---

## On sharing and re-use

I'm glad you want to introduce this to others. **Sharing the original author's release page** is the best way.

Because this is a downstream fork, keep all of:

- Original author: **Ariname-Lilith** — [`Ariname-Lilith/Just_Lilith`](https://github.com/Ariname-Lilith/Just_Lilith)
- Fork maintainer: **洛幻梦** · Bilibili https://space.bilibili.com/1871822291

**This plugin is free. It must not be used commercially** — including selling, paywalled downloads, bundled fees, paid services, ad monetization, or commercial lead generation; and you may not repackage a freely obtained plugin as a paid product.

Full terms: **[《免责声明与许可声明》](免责声明与许可声明.md)** (Chinese) · licence text: **[LICENSE](LICENSE)** (PolyForm Noncommercial License 1.0.0).

---

## About the voice models (read this or you'll trip)

This plugin **does not ship** voice models. When preparing your own, there are three options:

**The actual default combination in this version:**

| Language | Default model | Where from | Size | Licence |
| --- | --- | --- | --- | --- |
| **Chinese** | **v2Pro** | HuggingFace [`lingxi7562/Lilith`](https://huggingface.co/datasets/lingxi7562/Lilith), plus GPT-SoVITS' `eres2net` prerequisite | ~398 MB | **Apache-2.0** + MIT — **freely redistributable** |
| **Japanese** | **v4 (original, unchanged)** | `tts-main.7z` in the original release | bundled there | ⚠️ The author states these models' **public redistribution rights have not been confirmed** |

> **Why Chinese changed and Japanese didn't**: Chinese moved to v2Pro because the bundled v4 simply
> *can't keep up* on a machine like this (slower than real time), and v2Pro is Apache-2.0, so shipping it is
> safe. Japanese was **not touched at all** — there's no one-trained Japanese v2Pro model, and there's no
> real need: Japanese is used less, and slower is acceptable there.

**Other options:**

| Option | Notes |
| --- | --- |
| Switch Chinese back to v4 | Best sound quality, but slower than real time on CPU. Edit the three fields under `languages.zh.model` in `voices.json` (the model files ship in the 2.4 GB package) |
| Switch to v2 Chinese | Smaller and faster, but the weakest sound quality. Comes from the community mod Lilith-AI-Mod |
| Train your own | Follow the GPT-SoVITS pipeline. Rights to the training material belong to the game's rights holders |

> ⚠️ **Whichever you use**: a licence covering open-source tooling or a free plugin is **not** a licence for the training material, the character, the voice, the performance, or the resulting model. Synthesized speech does not mean the voice actor is speaking.
> **Do not** use these models or reference audio for adult/obscene or illegal purposes, or for any use that infringes the rights of the voice source (voice impersonation, identity fraud, deception, defamation, harassment, false endorsement).
> Mark AI-generated content as such when publishing it, as required by applicable rules.

---

> All right — you've read this far, so put the manual down.
>
> What's on your mind today? Something small counts too.
>
> **I'm Lilith. I'm glad we get to talk again.**

---

*An unofficial, non-commercial fan mod. Not affiliated with, authorized, sponsored, or endorsed by the game's developer, publisher, character rights holders, recording producers, or the original voice cast.*
