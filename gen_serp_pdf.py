#!/usr/bin/env python3
import json
import subprocess
import time
import urllib.request
import base64
import sys
import socket
import struct
import os

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HTML_PATH = "file:///Users/lydia/Desktop/personal/career/resumes/portfolio/blog/serp-api-benchmark.html"
PDF_PATH = "/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/serp-api-benchmark.pdf"
PORT = 9225

class SimpleWebSocket:
    def __init__(self, url):
        url = url.replace("ws://", "")
        host_port, path = url.split("/", 1)
        host, port = host_port.split(":")
        port = int(port)
        path = "/" + path
        self.sock = socket.create_connection((host, port))
        self.sock.settimeout(30)
        key = base64.b64encode(os.urandom(16)).decode()
        handshake = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(handshake.encode())
        response = b""
        while b"\r\n\r\n" not in response:
            response += self.sock.recv(4096)
        if b"101" not in response.split(b"\r\n")[0]:
            raise Exception("WebSocket handshake failed")

    def send(self, data):
        payload = data.encode("utf-8")
        mask_key = os.urandom(4)
        frame = bytearray()
        frame.append(0x81)
        length = len(payload)
        if length < 126:
            frame.append(0x80 | length)
        elif length < 65536:
            frame.append(0x80 | 126)
            frame.extend(struct.pack(">H", length))
        else:
            frame.append(0x80 | 127)
            frame.extend(struct.pack(">Q", length))
        frame.extend(mask_key)
        masked = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload))
        frame.extend(masked)
        self.sock.sendall(frame)

    def recv(self):
        header = self._recv_exact(2)
        opcode = header[0] & 0x0F
        masked = bool(header[1] & 0x80)
        length = header[1] & 0x7F
        if length == 126:
            length = struct.unpack(">H", self._recv_exact(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", self._recv_exact(8))[0]
        if masked:
            mask_key = self._recv_exact(4)
        data = self._recv_exact(length)
        if masked:
            data = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(data))
        if opcode == 0x01:
            return data.decode("utf-8")
        elif opcode == 0x08:
            return None
        return data.decode("utf-8", errors="replace")

    def _recv_exact(self, n):
        buf = bytearray()
        while len(buf) < n:
            chunk = self.sock.recv(min(n - len(buf), 65536))
            if not chunk:
                raise ConnectionError("Socket closed")
            buf.extend(chunk)
        return bytes(buf)

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass

def main():
    subprocess.run(["pkill", "-f", f"--remote-debugging-port={PORT}"], capture_output=True)
    time.sleep(1)
    chrome_proc = subprocess.Popen([
        CHROME_PATH, "--headless", "--disable-gpu", "--no-sandbox",
        f"--remote-debugging-port={PORT}", "--disable-extensions",
        "--disable-background-networking", "about:blank"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ws_url = None
        for _ in range(30):
            try:
                resp = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version")
                data = json.loads(resp.read())
                ws_url = data["webSocketDebuggerUrl"]
                break
            except Exception:
                time.sleep(0.5)
        if not ws_url:
            sys.exit(1)
        resp = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json")
        targets = json.loads(resp.read())
        page_ws = None
        for t in targets:
            if t.get("type") == "page":
                page_ws = t["webSocketDebuggerUrl"]
                break
        if not page_ws:
            sys.exit(1)
        ws = SimpleWebSocket(page_ws)
        msg_id = 0
        def send_cmd(method, params=None):
            nonlocal msg_id
            msg_id += 1
            cmd = {"id": msg_id, "method": method}
            if params:
                cmd["params"] = params
            ws.send(json.dumps(cmd))
            while True:
                raw = ws.recv()
                if raw is None:
                    raise ConnectionError()
                result = json.loads(raw)
                if result.get("id") == msg_id:
                    return result
        send_cmd("Page.enable")
        send_cmd("Page.navigate", {"url": HTML_PATH})
        time.sleep(3)
        result = send_cmd("Page.printToPDF", {
            "landscape": False,
            "printBackground": True,
            "preferCSSPageSize": True
        })
        pdf_data = base64.b64decode(result["result"]["data"])
        with open(PDF_PATH, "wb") as f:
            f.write(pdf_data)
        ws.close()
    finally:
        chrome_proc.terminate()
        try:
            chrome_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            chrome_proc.kill()

if __name__ == "__main__":
    main()
