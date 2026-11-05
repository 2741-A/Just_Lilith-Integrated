#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Just_Lilith 外部 TTS 示例服务（只用 Python 标准库）

用法：
    python 外部TTS示例服务.py --port 17901

默认返回一段提示音（占位），方便先验证接口是否通。
把 synthesize() 里的注释部分换成你自己的模型推理即可。

接口：
    GET  /health      → {"status":"ready","model_loaded":true}
    POST /synthesize  → 收到 JSON（text/language/...），返回 16-bit PCM WAV

注意：
  - 只绑定 127.0.0.1，不要暴露到局域网/公网；
  - 建议在服务内部串行处理合成（插件可能同时发来聊天、音乐评论、固定台词）；
  - 返回的 WAV 采样率必须是 8000/11025/16000/22050/24000/32000/44100/48000/88200/96000 之一。
"""

import argparse
import io
import json
import math
import struct
import threading
import wave
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# 合成锁：同一时间只让一个请求用模型（GPU 显存/线程安全）。
_MODEL_LOCK = threading.Lock()


def make_wav(pcm: bytes, sample_rate: int = 24000, channels: int = 1) -> bytes:
    """把 16-bit PCM 裸字节包成 WAV。"""
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(pcm)
    return buf.getvalue()


def synthesize(text: str, language: str) -> bytes:
    """
    ===== 把你的模型接在这里 =====

    期望返回：16-bit PCM 裸字节（单/双声道），下面用 24 kHz 单声道示例。
    比如：
        pcm = my_model.tts(text, lang=language)
        return make_wav(pcm, sample_rate=24000, channels=1)

    现在这段只是按文字长度生成一段 440 Hz 提示音，用来验证链路。
    """
    with _MODEL_LOCK:
        rate = 24000
        seconds = min(max(0.4, len(text) * 0.12), 3.0)
        frames = int(rate * seconds)
        pcm = bytearray()
        for i in range(frames):
            # 简单包络，避免爆音
            env = min(1.0, i / 400.0, (frames - i) / 400.0)
            sample = int(math.sin(2 * math.pi * 440.0 * i / rate) * 10000 * env)
            pcm += struct.pack("<h", sample)
        return make_wav(bytes(pcm), sample_rate=rate, channels=1)


class Handler(BaseHTTPRequestHandler):
    server_version = "JustLilithExternalTTS/1.0"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        # 默认日志会刷屏；只保留一行简短记录。
        print("[%s] %s" % (self.address_string(), fmt % args))

    def _send(self, code: int, content_type: str, body: bytes):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?", 1)[0] != "/health":
            self._send(404, "application/json", b'{"error":"not found"}')
            return
        body = json.dumps({"status": "ready", "model_loaded": True}).encode("utf-8")
        self._send(200, "application/json", body)

    def do_POST(self):
        if self.path.split("?", 1)[0] != "/synthesize":
            self._send(404, "application/json", b'{"error":"not found"}')
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            payload = json.loads(raw.decode("utf-8") or "{}")
            text = str(payload.get("text", ""))[:500]
            language = str(payload.get("language", "zh"))
            if not text.strip():
                self._send(400, "application/json", b'{"error":"empty text"}')
                return
            wav = synthesize(text, language)
            self._send(200, "audio/wav", wav)
        except Exception as exc:  # 出错要响亮，别静默
            print("[error] synthesize failed:", repr(exc))
            self._send(500, "application/json", json.dumps({"error": str(exc)}).encode("utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=17901, help="监听端口（1024-65535）")
    args = parser.parse_args()
    if not (1024 <= args.port <= 65535):
        raise SystemExit("端口必须在 1024-65535 之间")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print("外部 TTS 示例服务已启动：http://127.0.0.1:%d" % args.port)
    print("  GET  /health")
    print("  POST /synthesize  (JSON -> audio/wav)")
    print("按 Ctrl+C 停止。")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
