# Let an AI Agent install it for you · Just_Lilith Extended

> This page is for the **agent** (DeepSeek desktop app / DeepSeek Harness / Cherry Studio / Claude Code / Cursor / Qwen …).
> The human only does one thing: **copy the prompt below and send it to their agent.**

---

## 1. The human does one thing

1. Put `Just_Lilith-Setup.exe` in a folder. That is all you need — **the single exe is enough**;
   the manifest, plugin payload and patch are embedded inside it.
   (If `installer.json` / `plugin\` / `patch\` happen to be next to it, they take priority. If they
   are missing, the embedded copies are used.)
2. Open your agent and paste this:

```text
Please install a game mod for me. The installer is in this folder:
[replace with the folder that contains Just_Lilith-Setup.exe]

Read AGENT-INSTALL.md in the same folder first, then follow it.
Important: the download is large (possibly 3 GB+). Before every action, tell me what you plan to do,
how much will be downloaded and roughly how long it takes. Wait for my OK — don't run to the end by yourself.
```

3. The agent asks the questions it needs to ask. You answer, and click the UAC prompt if one appears.

**If your agent cannot run commands** (just a web chat box), see section 7 — do it by hand instead.

---

## 2. Steps for the agent

### Preconditions (check each one first; fix whatever fails)

| Precondition | How to check | If it fails |
|---|---|---|
| Windows 10 / 11 | — | The game is Windows-only; nothing can be done elsewhere |
| PowerShell available | `$PSVersionTable.PSVersion` | Any command execution works — not necessarily PowerShell |
| **`Just_Lilith-Setup.exe`** is present | `Test-Path` | Ask the user for the exe. **That one file is enough** (manifest/plugin/patch are embedded) |
| Game installed | `<GAME>\Lilith.exe` exists | Install the game first |
| Game not running | `Get-Process Lilith` returns nothing | Ask the user to quit |
| Enough free disk | see below | Clean up first — filling the disk mid-install is the messiest failure |

| Plan | Free disk needed |
|---|---|
| Text chat only | ~100 MB |
| Full (with voice) | **~8 GB** (2.4 GB archive + extracted + 1.2 GB acceleration pack) |
| ↳ the voice-runtime step alone | **~6 GB** free (Python + CUDA PyTorch) |

> 💡 **It does not have to be the Steam version.** The only criterion is whether the folder contains
> `Lilith.exe`. A non-Steam copy can't be found via the registry — ask the user for the folder.

### Terminology

`<EXE>` = full path to `Just_Lilith-Setup.exe`, `<GAME>` = the folder the game is installed in.

### Step 0 · Read the usage first, don't guess flags

```powershell
& "<EXE>" --help --report "$env:TEMP\jl-help.txt"
Get-Content "$env:TEMP\jl-help.txt"
```

`--help` writes the usage **plus every component id, size and dependency in this package** into the
report file, then exits immediately (~1 second). **Read it** — it beats trial and error.

> ⚠️ Reports are **UTF-8 with BOM**, so PowerShell's `Get-Content` reads them directly.
> In Python use `encoding='utf-8-sig'`.

### Step 1 · Find the game folder

The game is **The NOexistenceN of Lilith** on Steam (AppID `4643090`); the executable is **`Lilith.exe`**.

In command-line mode the installer **deliberately does not auto-detect** the folder (so it can never
write to the wrong place), so you must supply it:

```powershell
$id  = '4643090'
$key = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App $id"
$game = (Get-ItemProperty -Path $key -ErrorAction SilentlyContinue).InstallLocation
if (-not $game) {
    # fallback: read Steam's library config
    $steam = (Get-ItemProperty 'HKCU:\Software\Valve\Steam' -ErrorAction SilentlyContinue).SteamPath
    if ($steam) {
        $vdf = Join-Path $steam 'steamapps\libraryfolders.vdf'
        # find the block containing "4643090" and take its path (double backslashes — unescape them)
    }
}
$game
```

**Verify** that `Lilith.exe` sits directly inside it:

```powershell
Test-Path (Join-Path $game 'Lilith.exe')     # must be True
```

If you can't find it, ask the user — or have them double-click the exe and use the GUI (it fills this in).

### Step 2 · Read-only probe (writes nothing)

```powershell
& "<EXE>" --dry-run --game "<GAME>" --report "$env:TEMP\jl-dry.txt"
Get-Content "$env:TEMP\jl-dry.txt"
```

The report states whether the game was found, each component's state
(`已装（会跳过）` = already installed / `未装（会执行）` = will be installed), how much will be
downloaded, where to, and which runtime installer this machine's GPU needs. **Nothing touches the disk.**

> ⚠️ **Exit code 0 on `--dry-run` only means "the probe itself ran".** On a fresh machine it will list
> plenty of `未装（会执行）` and still return 0. **Read the report body, not the exit code.**

### Step 3 · Confirm with the user (**never skip this**)

Translate the probe result into plain language and let them choose:

| Plan | `--only` | Download | Result |
|---|---|---|---|
| **Text chat only** | `plugin,framework` | **~32 MB** | She chats, but **stays silent** |
| **Full install (recommended)** | omit `--only` | **~3 GB** | Voice, voice model, near-realtime speech |
| **Full + Agent** | omit `--only`, install the Agent too | ~3.1 GB | She can also read/write files and run commands (**very broad permissions**) |

⚠️ **Always ask before the 3 GB part.** On a typical home connection that range takes anywhere from
tens of minutes to hours — a completely different order of magnitude from 32 MB. Don't decide for them.

If they pick "full", there are **two more small questions** (both detailed in section 5):

**① Which reference voice?** (`tts-voices-mod2`, 41 MB, **defaults to the author's set**)

| Option | Meaning |
|---|---|
| **Same as the author** (default) | The installer fetches 4 audio files from the video-2 mod's own release |
| Keep the voice pack's own | Have them uncheck it — identical functionality, **different tone only** |

**② How should the 2.34 GB voice pack arrive?** (see "Voice pack" in section 5):

- **Let the installer download it** — resumable, slow but hands-off;
- **User downloads it themselves** — open
  `https://github.com/Ariname-Lilith/Just_Lilith/releases/tag/v_0.3.0`, download **both**
  `tts-main.7z.001` and `tts-main.7z.002`, put them together in
  `%USERPROFILE%\Desktop\Just_Lilith-TTS\` (create the folder if needed), then run with `--staging`
  pointing at that folder.

### Step 4 · Install

**First confirm the game is not running:**

```powershell
if (Get-Process Lilith -ErrorAction SilentlyContinue) { 'game is still running — close it first' }
```

Files are locked while the game runs, so writes will fail. Once it's closed:

```powershell
# Full install (the default-checked set)
& "<EXE>" --install --game "<GAME>" --report "$env:TEMP\jl-install.txt"

# Text chat only — saves the 3 GB
& "<EXE>" --install --game "<GAME>" --only plugin,framework --report "$env:TEMP\jl-install.txt"

# User already downloaded the voice pack to the desktop staging folder
& "<EXE>" --install --game "<GAME>" --staging "$env:USERPROFILE\Desktop\Just_Lilith-TTS" --report "$env:TEMP\jl-install.txt"
```

Then read the report:

```powershell
Get-Content "$env:TEMP\jl-install.txt"
```

It ends with a **落地核对** ("landing check") listing, per component, whether the expected file is in place.

### Step 4.5 · Voice runtime (**no voice without it**)

The 2.34 GB voice pack contains **no Python**. The runtime (Python + PyTorch, ~2.5–3 GB) comes from
the author's own script — the installer can run it for you:

```powershell
# Dry run first: prints the plan, downloads nothing, returns in seconds
& "<EXE>" --setup-runtime --game "<GAME>" --runtime-args -DryRun --report "$env:TEMP\jl-runtime.txt"

# The real thing: 1–2 hours, ~2.5–3 GB
& "<EXE>" --setup-runtime --game "<GAME>" --report "$env:TEMP\jl-runtime.txt"

# Afterwards, re-run the Step 4 --install command **unchanged** — that installs the speed pack
& "<EXE>" --install --game "<GAME>" --report "$env:TEMP\jl-install.txt"
```

This is the same code path as the GUI's one-click runtime prompt; the only difference is that the GUI
shows progress in its own window while the CLI streams it into the report file.

> ⚠️ **Use a long timeout.** The real run takes 1–2 hours. A default 30-second timeout will kill it.
> Either raise it, or run it in the background and poll the report file — the report flushes per line.

> ⚠️ **It detects an existing runtime and skips** — re-running will not re-download 2.5 GB.
> The check is `<GAME>\BepInEx\plugins\Just_Lilith\tts\runtime\python.exe`.

> ⚠️ **If the `tts` component (the 2.4 GB models) is not installed, this fails immediately** —
> the script installs Python into `tts\runtime\`, which must already exist. The installer says
> "语音目录不在" and tells you to run `--install` first. **That is not a network problem.**

### Step 5 · Verify

| Component | Proof it is installed |
|---|---|
| Plugin | `<GAME>\BepInEx\plugins\Just_Lilith\Just_Lilith.Unity.dll` |
| BepInEx framework | `<GAME>\BepInEx\core` |
| **Voice (models + engine)** | `<GAME>\BepInEx\plugins\Just_Lilith\tts\engine` and `tts\config\voices.json` beside it |
| **Voice runtime** (**a different component**) | `…\tts\runtime\python.exe` and `.just_lilith_runtime.json` beside it |

> ⚠️ **Don't mix those two up.** The 2.34 GB `tts` pack ships **models and engine only**;
> `runtime\python.exe` is placed by the **runtime installer** (`tts-runtime*`). A missing
> `runtime\python.exe` does **not** mean the voice pack failed — check whether the `.bat` was run
> (section 5) first.

**If the report shows ❌, it genuinely failed.** Do not tell the user "it should be fine" — paste the
failing line verbatim. The process also exits non-zero, so check that too.

### Step 5.5 · Report back in this shape

Don't just say "installed". Use this structure so the user knows where they stand:

```text
✅ Installed: <which components, how big each>
⏭️ Skipped: <which, why> (or "none")
📁 Game folder: <path>
⚠️ Still up to you:
   1. <one concrete thing + where to do it>
   2. ...
📄 Full report saved at: <report path>
❌ Problems: <verbatim, or "none">
```

**Nothing here requires the user to paste an API key into the chat.** See constraint 6 below — if they
offer to send it, tell them not to; the game has a field for it.

> ⚠️ **If the report contains a「还差一步」block, relay it verbatim.**
> When voice is installed it **will** appear (see section 5) — and the exit code is still **0**,
> because pass 1 did everything it could. But the **speed pack is not installed yet**; that's pass 2.
> **Relying on the exit code alone will miss it.** The block looks like:
>
> ```
> =========================================================
> ⚠️ 还差一步 —— 语音加速包这次没装上
>  ① 去游戏根目录：<path>
>  ② 进 tts-runtime-installer\ ，双击「安装语音运行时.bat」，等它跑完（要下 2.5–3 GB）
>  ③ 跑完之后，再点一次「开始安装」—— 第二次会把加速包补上
> =========================================================
> ```

### Step 6 · Tell the user what is still left

The installer only places files. **A few things the user must do themselves**:

1. **Enter an API Key** — without it she won't speak or reply.
   In game: `设置 → API 设置` → enter the endpoint and key → click 「保存并检测」 → pick a model.
   DeepSeek keys: `https://platform.deepseek.com/api_keys`; endpoint `https://api.deepseek.com`.
2. **If they want the Agent** (only if `agent-codex` was installed):
   ① set that API config's "接口格式" to **Responses**, not Chat Completions;
   ② in game → 「莉莉丝」 tab → pick a model → turn the Agent on.
3. **The voice runtime's last step**: ticking `tts-runtime*` only fetches the 31 MB installer —
   the user still has to **double-click** `tts-runtime-installer\安装语音运行时.bat`.
   See section 5.

---

## 3. Component list

The `--only` values are these ids; separate several with commas.

> 📌 **The numbers on this page were written against one version and may be stale.
> `installer.json` is the source of truth.** When they disagree, trust the file:
>
> ```powershell
> & "<EXE>" --help --report "$env:TEMP\jl-help.txt"
> Get-Content "$env:TEMP\jl-help.txt"
> ```
>
> `--help` is **generated on the spot from `installer.json`**, so components, sizes and dependencies are
> always current. This document explains *why*; `--help` tells you *what is true right now*.

| id | Name | Size | Default | Notes |
|---|---|---|---|---|
| `plugin` | Plugin | ~1 MB | ✅ | The core. Required. |
| `framework` | BepInEx framework | ~31 MB | ✅ | Prerequisite. Skip if already present. |
| `tts` | zh/ja voice **models + inference engine** (**no Python**) | **~2.34 GB** | ✅ | Without it there is no voice; text chat still works |
| `tts-zh-v2pro` | Chinese voice model v2Pro | ~398 MB | ✅ | Switches the Chinese default voice; **needs `tts`** |
| `tts-voices-mod2` | Reference voice pack (video 2's set) | ~41 MB | ✅ | **The user decides** (see section 5) |
| `tts-patch` | Voice speed patch | ~220 MB | ✅ | Makes speech near-realtime; **needs `tts-runtime*`**; **also what makes voice work at all without an NVIDIA card** |
| `tts-runtime` | Voice runtime installer (**general**: integrated / AMD / non-50-series NVIDIA) | ~31 MB | ✅ | **Required for voice** — see section 5 |
| `tts-runtime-rtx50` | Voice runtime installer (NVIDIA RTX 50-series only) | ~31 MB | ✅ | See section 5 — **pick exactly one of these two** (CLI picks for you) |
| `agent-codex` | Lilith Agent | ~78 MB | no | Advanced. **Very broad permissions** (can modify any file on this PC) and burns API credits |

**Dependencies (the order matters; the installer handles them, but keep it in mind when splitting with `--only`):**

```
framework ──> plugin
tts ──> tts-zh-v2pro      (no tts means no voices.json — skipped outright)
tts ──> tts-patch         (the patch edits service.py from the tts archive; reversed order gets overwritten)
tts-runtime* ──> tts-patch (pip runs tts\runtime\python.exe, which only the runtime installer provides)
```

**The full "I want voice" chain** (missing any link means silence):

```
tts (models+engine) → tts-runtime* (Python) → tts-patch (voice without a NVIDIA card + speed) → user's API Key
```

If you `--only` the dependent one without the prerequisite, the report says `跳过（前置不在）`
("skipped, prerequisite missing") — **that is expected, not breakage.** The exit code is non-zero
because the thing you asked for did not get installed.

---

## 4. Hard constraints (agent must read)

1. **Write only inside the game folder.** No files elsewhere, no registry writes, no services, no
   system environment changes. (Only exceptions: download cache in `%TEMP%\JustLilithSetup\`, and the
   voice-pack staging folder on the user's desktop.)
2. **Confirm the `Lilith` process is not running before touching anything.**
3. **These files must never be deleted:**

   ```text
   Lilith.exe            GameAssembly.dll    baselib.dll
   UnityPlayer.dll       UnityCrashHandler64.exe
   Lilith_Data\          AGENTS.md
   ```

   In particular **`baselib.dll` and `GameAssembly.dll` carry no vendor information at all** — they look
   like stray files but are the game itself.
4. **Do not "tidy up" anything else** you happen to see in the game folder (other mods, the user's files).
5. **Report failures.** If the report shows ❌ or the process returns non-zero, tell the user as-is.
   Do not smooth it over into "should be fine".
6. **⚠️ Never ask the user for their API key.** They enter it themselves in-game under
   `设置 → API 设置`. **Having them paste it into the chat leaves a plaintext secret in the history** —
   don't do it. Likewise, `BepInEx\config\local.just_lilith.llm.json` **contains the key**: never read it
   out, never quote it, never put it in a report or screenshot.
7. **Ask separately before installing `agent-codex`.** It grants the ability to modify *any file on this
   PC*. Don't tick it unless the user explicitly asks — it is the **only component whose consequences
   reach outside the game folder**. Even then, suggest testing against a scratch folder first.

---

## 5. Things worth knowing

### Why the voice pack (`tts`, 2.34 GB) gets its own explanation

It is a **two-volume archive**: `tts-main.7z.001` and `tts-main.7z.002`. **Both are required, and they
must sit in the same folder.**

Two routes:

- **Local import (recommended):** the user downloads both into
  `%USERPROFILE%\Desktop\Just_Lilith-TTS\`, then run with `--staging "<that folder>"`. The installer
  verifies SHA256 → extracts → places.
- **Automatic download:** omit `--staging`; the installer downloads from a mirror. **Resumable** —
  if it breaks, re-running continues where it stopped.

⚠️ **Don't use a third-party downloader that renames files.** Multi-volume 7z identifies volumes by
filename; renaming or dropping `.002` makes the archive unopenable.

### The voice runtime: **the `tts` pack contains no Python — skip this and there is no voice**

⚠️ **The single most misunderstood part.** The 2.34 GB `tts` pack is **models + inference engine**.
It contains **no Python runtime**. Python and its dependencies (PyTorch et al., 2.5–3 GB) come **only**
from `tts-runtime` / `tts-runtime-rtx50` — so **having voice requires installing one of them**,
regardless of whether there's a discrete GPU.

| Machine | Install |
|---|---|
| No NVIDIA card (integrated / AMD), or unsure | `tts-runtime` |
| NVIDIA, not 50-series | `tts-runtime` |
| NVIDIA RTX 50-series (5060/5070/5080/5090) | `tts-runtime-rtx50` |

> In CLI mode the installer **reads the GPU and picks for you** (it's strictly one of the two).

**Why install the CUDA build without an NVIDIA card:** PyTorch's CUDA build **falls back to CPU
automatically** when no CUDA device is present, and the author's own script explicitly supports
machines without CUDA. What actually blocks integrated graphics is the plugin's own
"refuses to start without a CUDA device" check — `tts-patch` fixes that.

**Dependency order**:

```
tts (models+engine) → tts-runtime* (Python) → tts-patch (patch + speed pack)
```

`tts-patch` runs `tts\runtime\python.exe`, so it declares that prerequisite. **If the runtime is
missing it will be marked `跳过（前置不在）` and the exit code will be 1** — that means a missing
piece, not breakage.

### Reference voice: **let the user choose** (default follows the author → video 2's set)

`tts-voices-mod2` changes *how she sounds* — 4 styles (neutral / excited / sleepy / sobbing).

- **Checked by default**: matches what this fork's author hears. The source is the video-2 mod
  (`Lilith-AI-Mod`); the installer pulls **only those 4 wav files** out of its release
  (the archive also contains that mod's own DLL — **not a single byte of it is placed**).
- **If the user prefers the pack's own voices** → have them uncheck it. Identical functionality,
  **different tone only**.

⚠️ Either way this affects **only those 4 styles**; the rest always come from the voice pack.
**This is taste, not a bug fix** — so ask, don't decide for them.

### The last step: running the runtime script (**agents can do this now**)

Ticking `tts-runtime*` only downloads the **31 MB installer**. It creates
`tts-runtime-installer\` in the game folder, containing `安装语音运行时.bat` (and `wheelhouse\`).
That script is what pulls the other 2.5–3 GB of Python and PyTorch.

**Three routes, pick one:**

| Who | How |
|---|---|
| **Agent** (recommended) | `--setup-runtime`, see Step 4.5. Output goes to the report, exit code is real |
| **User, via the GUI** | After install it asks "do it now?" → Yes. It then installs the speed pack **automatically** |
| **User, by hand** | Open `tts-runtime-installer\`, double-click `安装语音运行时.bat`, then click Install once more |

> ⚠️ **Do not have the agent run that `.bat`.** It ends with `pause`, and an agent will not press a
> key — the command **hangs forever** instead of failing. That is not an error, it is a hang, which is
> the worst failure mode to debug. Use `--setup-runtime` instead: it drives the same script's `.ps1`
> body directly, with no `pause`.

**When a user says "installed but there's no voice", ask first: was that step run?**

### Uninstalling

```powershell
# Default: removes only the plugin; keeps the BepInEx framework and the user's voice models
& "<EXE>" --uninstall --game "<GAME>" --report "$env:TEMP\jl-uninstall.txt"

# Also remove the framework (~6.7 GB more) — ⚠️ other BepInEx mods will break too
& "<EXE>" --uninstall --game "<GAME>" --remove-framework --report "..."

# Also remove the user's own trained voice models (~946 MB, irreplaceable) — only if they explicitly ask
& "<EXE>" --uninstall --game "<GAME>" --remove-framework --remove-models --report "..."
```

- User config is **backed up to a zip on the desktop** before removal (API keys, persona, chat history,
  voice config).
- Deletion **goes to the Recycle Bin**, not permanent — a mistake can be undone.
- `--remove-models` deletes voice models the user trained. **Irreplaceable. Don't add it unless asked.**

---

## 6. Reports and exit codes

| Code | Meaning |
|---|---|
| `0` | Success. For install/uninstall that means everything landed. For `--dry-run` / `--help` / `--selftest` it only means the action itself completed |
| `1` | Failure — a component ❌, a `落地核对 ❌ 不在` line, or a component skipped as `前置不在` (i.e. not installed) |
| `2` | **Bad arguments** — unrecognised flag (typo), or arguments that matched no mode. A usage report is still written |

`--setup-runtime` has its own set (its codes come from the author's script, plus two early exits of our own):

| Code | Meaning |
|---|---|
| `0` | The script reported success. We **also** verify `runtime\python.exe` separately — trusting `0` alone would miss "script said OK but nothing installed" |
| `1` | Failure (network / disk / antivirus). **Read the last lines the script itself printed** — that is the real cause |
| `0` (with `-DryRun`) | Dry run succeeded. **`python.exe` being absent is expected here** — nothing was installed |
| `1` (early exit, script never ran) | Can't run: voice folder missing / runtime-installer files incomplete / no `--game`. The report **states plainly that it is not a network problem** |
| `0` (early exit, already installed) | Runtime was already there; skipped, no 2.5 GB re-download |

**Always pass `--report` in command-line mode.** Without it the output goes to stdout, and `WinExe`
programs can have stdout swallowed depending on how they were launched — you'd get a "looks like it
worked but nothing happened" result. Write the report, read the file, don't guess.

```powershell
Get-Content "<report>"                     # PowerShell: fine as-is
```
```python
open(path, encoding='utf-8-sig').read()    # Python: use utf-8-sig
```

**`❌` in the report means real failure.** Every component ends up `✅` succeeded, `•` skipped
(prerequisite missing, or already installed), or `❌` failed.

---

## 7. If the agent cannot run commands

If the user only has a web chat box (no shell, no access to their PC), **turn it into manual steps**:

1. Double-click `Just_Lilith-Setup.exe` (**that one file is enough** — no need to copy the others).
2. The "游戏目录" row is usually filled in automatically; if not, click 浏览 and pick the folder
   containing `Lilith.exe`.
3. Tick components. The recommended ones are already ticked — **just click 「开始安装」**.
4. For the 2.34 GB voice pack the UI asks whether they already downloaded it or want the installer to
   fetch it.
5. **When it finishes it asks "install the voice runtime now?" → tell them to click Yes.**
   That opens a window and runs 1–2 hours (~2.5–3 GB); afterwards it installs the speed pack
   **by itself**. Neither step needs them to do anything.
6. A "what's left to do" panel appears — follow the buttons.

---

## 8. Troubleshooting

| Symptom | What to do |
|---|---|
| `❌ 目录校验不过（里面没有 Lilith.exe）` | Wrong `--game`. It must be the folder containing `Lilith.exe`, not the Steam library root |
| `❌ SHA256 不匹配` | Corrupt download. Re-run — it re-downloads. The report has expected vs actual; paste it |
| `跳过（前置不在）` | Normal. A component you asked for needs another one that isn't installed |
| Installed but no voice | ① **does `tts\runtime\python.exe` exist?** (missing = the runtime step never ran; most common — see Step 4.5) ② is the API Key set? ③ does the report show `tts-patch` as `跳过（前置不在）`? ④ if all done: paste the **last 100 lines** of `<GAME>\BepInEx\LogOutput.log` |
| `--setup-runtime` says `语音目录不在` | The 2.4 GB `tts` component isn't installed yet. Run `--install` first, then retry this step. **Not a network problem** |
| Disk fills up mid-install | The full voice tier needs **~8 GB** free including extraction |
| Plugin doesn't load in game | Check that `<GAME>\winhttp.dll` and `<GAME>\BepInEx\core` both exist |

---

## 9. One-paragraph summary for the agent

```text
Read --help first → locate the folder containing Lilith.exe → --dry-run to probe →
tell the user the result and download size, let them choose → confirm the game isn't running →
--install → read the 落地核对 section of the report →
for voice, run --setup-runtime (1–2 hours; raise your timeout) → run --install once more for the
speed pack → state what the user still has to do (API key, etc.).
Write only inside the game folder, never touch the whitelist files, and report failures as they are.
```

**Three things that trip agents up:**

1. `--setup-runtime` **takes 1–2 hours** — a default timeout (30s or so) will cut it off.
2. **Don't run that `.bat`** — its trailing `pause` means your command never returns.
3. If the report shows `❌` or a「还差一步」block, **pass it to the user verbatim**. Don't decide
   "it should be fine" on their behalf.
