# 外部 TTS 接口 · 用自己的语音模型

> 版本：ext.59 起支持  
> 适用：你（或朋友）已经有自己的 TTS 模型 / 推理服务，不想用插件内置的 GPT-SoVITS。

插件只做两件事：把文字发给你，把你的 WAV 播出来。  
**它不会启动、也不会结束你的服务**，更不会改你的模型或 Python 环境。

---

## 一、两个 HTTP 接口

服务必须监听 `127.0.0.1`（或 `localhost`）的某个端口（1024–65535），只走 HTTP，不带路径前缀。

### 1. `GET /health`

用来告诉插件“我准备好了”。

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"status":"ready"}
```

- `status` 只能是 `ready` / `loading` / `starting` / `error`。
- `model_loaded`、`service` 都是可选的；外部服务不需要模仿内置服务的身份字段。
- `loading` / `starting` 时插件会继续等（默认最多 180 秒）。
- 返回 404、非 JSON、或 `status` 不认识 → 插件会明确报“健康检查格式不正确”。

### 2. `POST /synthesize`

插件把要说的文字发给你。

```http
POST /synthesize HTTP/1.1
Content-Type: application/json

{
  "request_id": "2f0c...（UUID，可忽略）",
  "text": "今天也要一起听歌吗？",
  "language": "zh",              // "zh" 或 "ja"
  "reference_style": "neutral",   // 可忽略：neutral/excited/sobbing/hesitant/sleepy/tsundere/ominous
  "reaction_id": null             // 可忽略：反应音标识
}
```

返回：

```http
HTTP/1.1 200 OK
Content-Type: audio/wav

<WAV 二进制>
```

**WAV 要求**（插件直接解析，不做转码）：

- 16-bit PCM；
- 单声道或双声道；
- 采样率：8000 / 11025 / 16000 / 22050 / 24000 / 32000 / 44100 / 48000 / 88200 / 96000；
- 单次 ≤ 180 秒、≤ 32 MiB；
- 文件头里的 RIFF 长度必须和实际字节数一致（用 Python `wave` 模块或 ffmpeg 生成即可）。

插件不关心你内部用什么模型、CPU 还是 GPU、串行还是并行。  
建议服务内部串行处理请求（聊天、音乐评论、固定台词可能同时到达）。

---

## 二、插件配置

配置文件：

```
<游戏目录>\BepInEx\config\local.just_lilith.tts.json
```

把整个文件写成下面这样（端口改成你服务的端口）：

```json
{
  "schema_version": 4,
  "service_enabled": true,
  "enabled": true,
  "language": "Chinese",
  "reference_mode": "Automatic",
  "forced_reference_style": "neutral",
  "reactions_enabled": true,
  "volume": 1.0,
  "service_url": "http://127.0.0.1:17901",
  "external_service": true
}
```

- 日语用户把 `"language"` 改成 `"Japanese"`。
- `service_url` 只能是本机回环地址，不能带路径、查询串或账号密码。
- `service_enabled` 必须为 `true`；游戏里的「语音服务」开关就是它。
- 改完配置**重启游戏**才会重新读取。
- 想切回内置语音：把 `external_service` 改成 `false`，`service_url` 改回 `http://127.0.0.1:17880`，重启游戏。

> 如果使用外部 TTS，安装器中 **不需要勾选 `tts` 语音包（2.34 GB）和语音运行时**。  
> 只装插件本体 + BepInEx 框架即可。

> ⚠️ 安装器里的「🩺 诊断 → 语音打不开」检查的是**内置运行时**。使用外部 TTS 时，
> `tts\runtime` 和内置模型缺失是正常的，**不要为了体检去装那 2.5 GB**；
> 外部服务是否正常，以 `GET /health` 和游戏日志里「外部 TTS 已就绪」为准。

---

## 三、快速验证

### 1. 服务是否活着

PowerShell：

```powershell
Invoke-RestMethod http://127.0.0.1:17901/health
```

应输出 `status : ready`。

### 2. 游戏里

启动游戏后看日志：

```
BepInEx\LogOutput.log
```

成功：

```
module=... external=True
module=... 外部 TTS 已就绪
```

失败会明确写原因，例如：

- `外部 TTS 未启动：请先在 http://127.0.0.1:17901 启动你的 TTS 服务`
- `外部 TTS 健康检查格式不正确：/health 需返回 JSON，status 为 ready/loading/error`
- `外部 TTS 返回错误状态（status=error）`
- `外部 TTS 连接已中断（服务可能已退出）`

### 3. 气泡和语音

外部 TTS 走的是和内置语音**完全相同**的播放通道：

- 语音真正开始播放的那一刻，气泡才出现；
- 合成失败 / 服务断开 → 气泡立即出现，并在状态栏写明原因（不会卡住不说话）；
- 语音比气泡晚到（首次加载模型很慢）→ 气泡会从语音开播那一刻重新陪一遍；
- 插件自己的「少女思考中....」占位文本**永远不会**被送去合成。

---

## 四、示例服务

同目录的 `外部TTS示例服务.py` 是一个只依赖 Python 标准库的最小实现：

```powershell
python 外部TTS示例服务.py --port 17901
```

它现在返回一段提示音（占位）。  
把 `synthesize()` 函数里的注释部分换成你自己的模型推理即可，例如：

```python
def synthesize(text: str, language: str) -> bytes:
    pcm = my_model.tts(text, lang=language)   # 返回 16-bit PCM 字节
    return make_wav(pcm, sample_rate=24000, channels=1)
```

---

## 五、给 AI 智能体的安装步骤

如果用户让 AI 帮忙接自己的 TTS：

1. **先问清楚**：用户的 TTS 服务地址是什么？是否已经能返回 WAV？  
   如果用户只有模型文件（例如 GPT-SoVITS checkpoint），不要硬套这个接口，改走“换模型”路线（见 `README.md` / `voices.json`）。
2. **验证服务**：`Invoke-RestMethod http://127.0.0.1:<port>/health` 必须返回 `status=ready`。
3. **写配置**：把上面的完整 JSON 写到  
   `<游戏目录>\BepInEx\config\local.just_lilith.tts.json`  
   （UTF-8，无 BOM；端口换成用户的）。
4. **不要装语音包**：外部 TTS 用户跳过安装器里的 `tts` 组件和语音运行时。
5. **不要改 DLL / 不要改 Python 运行时**。这个接口就是全部契约。
6. **重启游戏**，检查 `LogOutput.log` 里有没有「外部 TTS 已就绪」。
7. 如果用户的服务还没写，复制 `外部TTS示例服务.py`，让用户把 `synthesize()` 换成自己的推理，再启动。

---

## 六、边界

- **只允许本机回环地址**：`127.0.0.1` / `localhost`；插件不会把聊天文字发到局域网或外网。
- **插件不负责启动/重启你的服务**：服务没开就是“外部 TTS 未启动”，不会偷偷拉起内置运行时。
- **不自动安装 Python 依赖、不自动下载模型**：这些由你（或你的 AI）自己决定。
- **语音内容会经过你的服务**：请确认服务只绑定 `127.0.0.1`，不要把端口暴露到公网。
- **切回内置语音不会串声**：外部模式不读、不写内置的 v2Pro 固定台词缓存；主动搭话使用独立的 `ambient\external` 缓存目录。
