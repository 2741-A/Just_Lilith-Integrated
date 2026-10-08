# 第三方组件与来源清单（NOTICE）

> 这份是给**发布者自己**看的账本，也是给下游的透明说明。
> 加新的第三方东西时**顺手加一行**，别等发布前再回头翻。
> 最后更新：2026-10-07（补入安装器内嵌的 7-Zip）

---

## 一、原始作品（本插件是它的下游修改版）

| 项 | 内容 |
| --- | --- |
| 名称 | Just_Lilith |
| 作者 | **Ariname-Lilith**（B站「烤门万」） |
| 仓库 | https://github.com/Ariname-Lilith/Just_Lilith |
| 许可 | **PolyForm Noncommercial License 1.0.0** |
| ⚠️ 注意 | 仓库里的许可文件**文件名拼成了 `LICNESE`**（少一个 E），所以 GitHub 的许可证识别显示为「无」。**实际是有许可的**，内容就是 PolyForm Noncommercial 1.0.0。引用来源时别被 GitHub 的显示误导。 |
| 联系方式 | amoxicillin.a.v.n@gmail.com · https://space.bilibili.com/28692404 |

**PolyForm 对本项目的三条硬约束**（再分发时必须做到）：
1. **署名**：保留原作者与来源
2. **附条款**：拿到副本的人必须同时拿到许可条款或 URL
3. **非商业**：不得销售、付费下载、捆绑收费、广告变现、商业引流

---

## 二、运行时 / 引擎

| 组件 | 用途 | 来源 | 许可 | 是否随包分发 |
| --- | --- | --- | --- | --- |
| **GPT-SoVITS** | 本地语音合成引擎 | https://github.com/RVC-Boss/GPT-SoVITS | **MIT** | ❌ 使用者自备（`tts-main.7z`） |
| **BepInEx**（IL2CPP 版） | Unity 插件框架 | https://github.com/BepInEx/BepInEx | **LGPL-2.1**（实测版本 `6.0.0-be.788`） | ❌ 使用者自备 |
| **Python 3.9 embed** | TTS 运行时 | python.org | PSF License | ❌ 使用者自备 |
| **PyTorch (CPU)** | 推理后端 | https://pytorch.org | BSD-3-Clause | ❌ 使用者自备 |
| **.NET 6** | 插件运行时 | Microsoft | MIT | ❌ 随游戏环境 |
| **Codex CLI** | Agent 通道（可选） | https://github.com/openai/codex | **Apache-2.0**（实测版本 `0.161.0`） | ❌ 使用者自备 |
| **Harmony (Lib.Harmony)** | 运行时补丁 | https://github.com/pardeike/Harmony | MIT | ✅ 随插件 DLL |
| **7-Zip 24.09** | **安装器**解压 RAR / 多卷 7z | https://www.7-zip.org | **LGPL-2.1** + unRAR 限制 + BSD | ✅ 内嵌在安装器里（2.37 MB，见 2.1） |

### 2.1 ⚠️ 安装器内嵌了 7-Zip —— 附许可文本是**硬性要求**，不是可选项

| 项 | 内容 |
| --- | --- |
| 组件 | 7-Zip **24.09**（x64）：`7z.exe` 0.54 MB + `7z.dll` 1.82 MB + `License.txt` |
| 来源 | https://www.7-zip.org/download.html |
| 用途 | 安装器解压 `.rar`（RAR5）与多卷 `.7z.001/.002`。.NET 自带的 `System.IO.Compression` **只认 zip**，而原版这两个包恰好是 rar 和多卷 7z |
| 许可 | `7z.dll`：主体 **GNU LGPL**；部分代码为 **LGPL + unRAR license restriction**；另有 **BSD 3-clause / BSD 2-clause** 部分。其余文件：**GNU LGPL** |
| 再分发要求（原文） | *"Redistributions in binary form must reproduce related license information from this file."* |

**这条是怎么满足的（三处，缺一不可）**：

1. `License.txt` **原样内嵌**进安装器（`thirdparty\7z\License.txt`）。安装器要用 7-Zip 时会把它释放到临时目录，用户能看到；
2. `build.ps1` 打包时再复制一份到 exe **旁边**，叫 `7-Zip-License.txt`；
3. 就是本节这张表（来源 + 许可 + 再分发要求）。

> 🔎 **unRAR 限制只约束一件事**：不得用这段代码做 RAR **压缩器**。
> 我们只拿它**解压**，不受这条限制。
>
> ⚠️ 不要为了「少带一个 exe」改用纯托管的解压库：多卷 7z 的支持普遍不完整，
> 而 2.4 GB 的语音包正好是多卷 —— 解不开比多带 2.37 MB 严重得多。

---

## 三、语音模型与参考音频

⚠️ **本发布包不包含这些，只在代码里支持它们。**
**文件许可 ≠ 声音授权** —— 详见 [免责声明与许可声明.md](免责声明与许可声明.md) 第 3.2 节。

### 3.1 v4 中文 / 日语（原始作品默认）

| 项 | 内容 |
| --- | --- |
| 文件 | `models/zh/Lilith.zh_v4-e15.ckpt` + `…_e2_s798_l32.pth`<br>`models/ja/Lilith.ja-e15.ckpt` + `…_e2_s796_l32.pth` |
| 来源 | 原始作品 Release：`tts-main.7z.001` / `.002` |
| 发布者 | **Ariname-Lilith** |
| 许可状态 | ⚠️ **原作者自己在声明里写明**：「随包的莉莉丝声音模型和参考音频由作者根据原作数据自行制作。**作者尚未确认这些模型和参考音频的公开再分发授权**，当前发布方案仍将其随包附带。」 |
| 对本项目的含义 | **让使用者去原版 Release 下，不要在自己包里再转一手。** 风险留在原作者那儿，你只指路。 |

### 3.2 v2Pro 中文（**本版的默认中文模型**）

> 📌 这一版**默认就用它**，不再是可选项 —— 因为原版 v4 在 CPU 上比实时还慢（RTF 1.93 vs 0.48）。
> 安装器会从下面的来源自动下载，**不打包进发布包**（安装器本体仍然只有 60 MB）。

| 项 | 内容 |
| --- | --- |
| 文件 | `Lilith_v2pro_8.12_l-e15.ckpt`（155,312,957 B）+ `Lilith_v2pro_8.12_l_e12_s1968.pth`（134,946,086 B） |
| 来源 | HuggingFace 数据集 [`lingxi7562/Lilith`](https://huggingface.co/datasets/lingxi7562/Lilith)（国内用 `hf-mirror.com`） |
| 发布者 | `lingxi7562` |
| 许可 | **Apache-2.0**（数据集 README 的 frontmatter 标注，已核实 `license: apache-2.0`、`gated: false`） |
| SHA256 | ckpt `3b9db482…f3f7fe5` · pth `0d7585cb…aa9f2c6`（与 HF 的 LFS oid 一致） |

**它的前置文件（也必须一起下，原版包里没有）：**

| 项 | 内容 |
| --- | --- |
| 文件 | `pretrained_eres2netv2w24s4ep4.ckpt`（107,528,697 B） |
| 用途 | 说话人验证网络。只在模型版本含 `Pro` 时加载（`TTS.py` 的 `init_vits_weights` 里判的），v2/v4 不需要 |
| 放置位置 | `<插件目录>\tts\engine\GPT_SoVITS\pretrained_models\sv\` |
| 来源 | HuggingFace 模型库 [`lj1995/GPT-SoVITS`](https://huggingface.co/lj1995/GPT-SoVITS) 的 `sv/` |
| 许可 | GPT-SoVITS 项目为 **MIT** |
| SHA256 | `4f5a0bf7…8e581a35` |

> ⚠️ 容易踩的坑：这个文件**不在原版 `tts-main.7z` 里**，少了它 v2Pro 会直接起不来，
> 而报错信息**不会告诉你缺的是它**。所以必须随 v2Pro 一起提供。
| gated | False（无需授权即可下载） |
| 数据集里还有什么 | `Lilith_v2pro_8.12_l-e10.ckpt`、`Lilith_v2pro_8.12_l_e8_s1312.pth`、以及 **v2proplus 系列** 5 个权重；另有训练音频 `wavs_32k/`、`wavs_32k_lilith2/`、`wavs_sliced/` 与训练清单 `lilith_all.list` |

> ⚠️ **Apache-2.0 是「数据集作者对他制作的权重文件」的授权，授权的是文件，不是声音本身。** 声音的权利仍归配音演员与游戏权利方。别把 Apache-2.0 讲成「声音也能随便用」。

### 3.3 参考音色（`tts-voices-mod2` 组件）—— 社区 mod 的一套

> 📌 **默认装这一套**（因为本版作者用的就是它）。不想要就在安装器里取消勾选，
> 那样用的是语音包自带的那套（来自原始作品的 `tts-main.7z`），功能完全一样，只是语气不同。

| 项 | 内容 |
| --- | --- |
| 文件 | `calm-reference.wav` / `excited-reference.wav` / `sleepy-reference.wav` / `wronged-reference.wav` |
| 对应到本插件的风格 | `neutral` / `excited` / `sleepy` / `sobbing`（**只换这 4 个**，其余仍用语音包自带的） |
| 来源包 | [`mimimi6666/Lilith-AI-Mod`](https://github.com/mimimi6666/Lilith-AI-Mod) Release `v0.1.1-rc4` 的 **`core.zip`** |
| 包内路径 | `BepInEx\data\LilithTextInjector\voice\*-reference.wav` |
| SHA256（整包） | `155dc0bb1a1ddea003690bcd8a4edfe949526d46726dab6fd3afd4a3bed9fc73` |
| 是否随本发布包分发 | ❌ **不随包**。安装器从该 mod 自己的 Release 下载 —— **指路，不转手** |
| 许可状态 | ⚠️ 该 mod 的**代码**许可与本批音频的授权是两回事；音频派生自游戏原声，授权状态不确定 |

**另外**：`core.zip` 里还有那个 mod 自己的插件（`LilithTextInjector.dll`）。
本安装器**只按名字取出上面 4 个 wav**，其余一个字节都不落地 ——
免得把两个 mod 混在同一个游戏目录里打架。

> ⚠️ 这个包里的逐字稿（`*_transcripts.json`）在 `sleepy` 那条有**错别字**：
> 写成「那**李尼斯**也起床啦」，而音频里说的是「那**莉莉丝**也起床啦」。
> 本安装器写入的是**改对的**版本（音频转写核实过）。

### 3.4 v2 中文（另一个 mod 的版本，本项目未采用）

| 项 | 内容 |
| --- | --- |
| 文件 | `lilith-e15.ckpt` + `lilith_e8_s288.pth` |
| 来源 | 社区 mod **Lilith-AI-Mod** 的 `voice-pack.zip` / `voice-runtime.zip` |
| 发布者 | `mimimi6666` |

**三个版本的关系**：都是「莉莉丝」、**都是 e15（训练 15 轮）**，很可能是同一批训练数据跑在不同代架构上（v2 / v2Pro / v4）。**但文件不是同一份，不能互相替代。**

---

## 四、人设与世界书（若随包提供模板）

| 项 | 内容 |
| --- | --- |
| 来源 | 社区 mod **The-NOexistenceN-of-Lilith-Mod** 的 `character/lilith.json` + `character/lore/index.json`（22 条原作剧情条目） |
| 仓库 | https://github.com/cza2019/The-NOexistenceN-of-Lilith-Mod |
| 该 mod 许可 | MIT（**代码**部分） |
| 原作文本权利 | **归游戏权利方** —— 剧情、角色、台词不属于该 mod 作者，也不属于本插件 |
| 对本项目的含义 | 可以随模板提供，但发布说明里应写明出处。**不要声称是自己原创的剧情整理。** |

---

## 五、在线查询来源（运行时访问，不随包分发）

音乐评论功能会访问以下公开接口，**不发送任何 API Key**：

| 来源 | 用途 |
| --- | --- |
| 星穹铁道 WIKI（`wiki.biligame.com`） | 官方背景（最高优先级） |
| 萌娘百科（`zh.moegirl.org.cn`） | 角色/作品背景网页抓取 |
| B站搜索 API | 视频标题与简介 |
| 必应中国 / 搜狗 / 360 | 通用搜索兜底 |
| 网易云音乐 API | 同名候选（仅参考，权重最低） |

> ⚠️ 这些站点的服务条款与反爬策略可能会变。若某个来源失效，功能会退回下一层，不会崩。

---

## 六、隐私：本项目**不**包含的东西

发布包与更新**均不包含**以下内容，更新也**不会覆盖**使用者已有的这些数据：

- 作者的 API Key（`local.just_lilith.llm.json`）
- 聊天记录与会话（`workspace/sessions/`、`active-session.json`）
- 音乐评论缓存（`local.just_lilith.music_cache.json`）——里头有使用者听过什么歌
- 余额状态（`local.just_lilith.balance.state.json`）
- Agent 的 Codex `ThreadId`（`workspace/agent/session.json`）
- 游戏日志（`BepInEx/LogOutput.log`）
- 开发机的绝对路径、截图、训练数据集

> 📌 **打包前请对照这份清单逐条检查。** 这一类文件「看着像配置、其实是本人」，最容易漏。

---

## 七、待办（发布前补完）

- [ ] 核 `framework.rar` 里 BepInEx 的具体版本与许可
- [ ] 核 Codex CLI 的许可与本项目引用方式
- [ ] 确认人设/世界书模板是否随包提供；若提供，补出处说明
- [x] 所有占位符已填（版本号 / 日期 / 署名 / 联系方式）　2026-10-08
- [ ] 打包前过一遍第六节的隐私清单
