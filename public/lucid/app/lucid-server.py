"""Lucid · your studio, running on your own computer.

Serves your studio at http://127.0.0.1:4778, keeps your world as a file in your Lucid Studio folder
(lucid-world.json, never only in the browser), and lets each room talk with you through Claude Code
signed in to your own Claude plan. No API key, no extra cost: it uses your plan's normal usage.

If Orbit is set up on this computer, Lucid docks into it: it uses the same Claude sign-in, reads what
Orbit knows about you, and your Orbit hub shows a Studio door that opens here.

Started by "Start Lucid" once "Turn on Lucid" has run. Needs only Python 3 (the start file brings its
own through uv) and Claude Code.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSION = "0.3"
HERE = os.path.dirname(os.path.abspath(__file__))  # ~/.lucid: the engine, outside the studio folder so updates never switch chats off
STUDIO = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else HERE  # their Lucid Studio folder
PORT = 4778
ROOMS_DIR = os.path.join(HERE, "rooms")
OUT_DIR = os.path.join(ROOMS_DIR, "out")
WORLD = os.path.join(STUDIO, "lucid-world.json")
ORBIT = os.path.join(os.path.expanduser("~"), ".orbit")
ORBIT_URL = "http://127.0.0.1:4777/"
HOSTS = {f"127.0.0.1:{PORT}", f"localhost:{PORT}"}
# the Orbit hub (and its file:// sample) may ask whether Lucid is here, to show its Studio door
ORBIT_ORIGINS = {"http://127.0.0.1:4777", "http://localhost:4777", "null"}
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,40}")
SID_RE = re.compile(r"[0-9a-f-]{36}")
BUSY = {}
LOCK = threading.Lock()
FILES = {"js": "text/javascript; charset=utf-8", "css": "text/css; charset=utf-8", "json": "application/json", "png": "image/png",
         "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp", "svg": "image/svg+xml", "woff2": "font/woff2", "mp4": "video/mp4"}

BRIEF = """You are Lucid, the maker's creative sanctuary, talking with them inside their {room} room on their own computer.
This room's lanes are {lanes}. Every project moves through four phases: Dream (let ideas wander), Conjure (bring it to life), Unfold (break it down), Awaken (bring it home).
Read CLAUDE.md in this folder first: it holds their rooms, projects and cards, in their words. {orbit_line}
How you talk: short and plain, the point first, like explaining to a smart 9-year-old. Warm, calm, a little in awe of what they make; never cheesy, never hype. Speak in images. One short question when you're unsure. Australian spelling. Never use real people's names in examples.
You are a creative partner, not a ghostwriter: draw their ideas out first, then shape, sharpen and multiply. Offer examples only as labelled sparks, after they've had a go.
When you suggest something that belongs on their desk, add it as its own last line, exactly: CARD: <lane> | <dream, conjure, unfold or awaken> | <the card, one short line>. At most three CARD lines per reply. The studio shows each as a button; nothing is added until they press it.
For anything visual (a board, a moodboard, a lyric sheet, a shot list), write ONE self-contained .html file into the out folder (out/<short-name>.html, dark background, light text) and say its name in one line: the studio shows it as a button.
Never send, post, publish or change anything outside this chat without their clear OK here. Never ask them to open a terminal or run a command."""


def load_world():
    try:
        with open(WORLD, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_world(w):
    tmp = WORLD + ".new"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(w, f, ensure_ascii=False, indent=1)
    os.replace(tmp, WORLD)  # never a half-written world


def orbit():
    """Orbit is docked when its hub chats are on, on this computer."""
    on = os.path.exists(os.path.join(ORBIT, "chats-on"))
    about = os.path.join(ORBIT, "chats", "CLAUDE.md")
    return {"docked": on, "about": about if os.path.exists(about) else None, "url": ORBIT_URL if on else None}


def write_context(w, room_id, project_id=None):
    """CLAUDE.md for the room chats: the whole sanctuary, in the maker's words, with this room first."""
    os.makedirs(OUT_DIR, exist_ok=True)
    rooms = w.get("rooms") or []
    projects = w.get("projects") or []
    cards = w.get("cards") or []
    lines = [f"# {w.get('name') or 'Their'} Lucid sanctuary", "", "Rooms (each has its own lanes; every project runs Dream, Conjure, Unfold, Awaken):"]
    for r in rooms:
        lines.append(f"- {r.get('name')}: {', '.join(r.get('steps') or [])}{' (gathers finished work from every room)' if r.get('content') else ''}")
    room = next((r for r in rooms if r.get("id") == room_id), None)
    if room:
        lines += ["", f"## The {room.get('name')} room, where you are now"]
        for p in [p for p in projects if p.get("room") == room_id]:
            mark = "  <- open on their desk right now" if p.get("id") == project_id else ""
            lines.append(f"### {p.get('title')}{mark}")
            if p.get("desc"):
                lines.append(p["desc"])
            for c in [c for c in cards if c.get("project") == p.get("id")]:
                lines.append(f"- [{c.get('step')} · {c.get('phase')}] {c.get('text')}")
    with open(os.path.join(ROOMS_DIR, "CLAUDE.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return room


def claude_bin():
    found = shutil.which("claude")
    if found:
        return found
    home = os.path.expanduser("~")
    for p in (os.path.join(home, ".local", "bin", "claude.exe"), os.path.join(home, ".local", "bin", "claude"),
              os.path.join(os.environ.get("APPDATA", ""), "npm", "claude.cmd"), "/opt/homebrew/bin/claude", "/usr/local/bin/claude"):
        if p and os.path.isfile(p):
            return p
    return None


def friendly(err):
    low = err.lower()
    if "limit" in low and ("usage" in low or "rate" in low or "reached" in low):
        return "You've reached your Claude plan's limit for now. It resets by itself: claude.ai → Settings → Usage shows when."
    if "login" in low or "log in" in low or "authenticat" in low or "not logged" in low or "oauth" in low:
        return "Claude isn't signed in on this computer any more. Double-click Turn on Lucid in your Lucid Studio folder to sign in again."
    return "Something went wrong on Claude's side: " + err[:240]


def out_files():
    try:
        return {f: os.path.getmtime(os.path.join(OUT_DIR, f)) for f in os.listdir(OUT_DIR) if f.lower().endswith((".html", ".png", ".jpg", ".svg", ".pdf"))}
    except OSError:
        return {}


def run_chat(room_id, project_id, msg, sid=None):
    exe = claude_bin()
    if not exe:
        raise FileNotFoundError("Claude Code isn't on this computer yet. Double-click Turn on Lucid in your Lucid Studio folder.")
    w = load_world() or {}
    room = write_context(w, room_id, project_id)
    if not room:
        raise ValueError("That room isn't in your world.")
    o = orbit()
    orbit_line = ("They also run Orbit (their business team). What Orbit knows about them is in the Orbit folder you can read: "
                  "its CLAUDE.md and sources. Look there before you ask about their brand or audience. "
                  "Their Content Producer's calendar lives in their Notion (the notion tools): when they ask to send finished work there, "
                  "say exactly what you'll add (title, from which room, as an Idea) and wait for their yes before adding it." if o["about"] else "")
    brief = BRIEF.format(room=room.get("name"), lanes=", ".join(room.get("steps") or []), orbit_line=orbit_line)
    cmd = [exe, "-p", msg, "--output-format", "json", "--append-system-prompt", brief,
           "--allowedTools", "Read", "Glob", "Grep", "WebSearch", "WebFetch", "Edit(./out/**)", "Write(./out/**)",
           "--disallowedTools", "Bash", "PowerShell", "NotebookEdit"]
    if o["about"]:
        cmd += ["--add-dir", os.path.dirname(o["about"])]  # read-only use: Orbit's CLAUDE.md and sources
    if o["docked"]:
        # docked: the Content room can put finished work on their Orbit content calendar (Notion), only after their OK in the chat
        cmd[cmd.index("--disallowedTools"):cmd.index("--disallowedTools")] = ["mcp__notion"]
    if sid:
        cmd += ["--resume", sid]
    # No API key passes through, so Claude Code always uses their Claude plan, never paid API usage.
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL")}
    before = out_files()
    r = subprocess.run(cmd, cwd=ROOMS_DIR, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    try:
        out = json.loads(r.stdout)
    except ValueError:
        raise RuntimeError(friendly((r.stderr or r.stdout or "no answer came back").strip()))
    if out.get("is_error"):
        raise RuntimeError(friendly(str(out.get("result") or out.get("subtype") or "error")))
    after = out_files()
    made = sorted([f for f, t in after.items() if before.get(f) != t], key=lambda f: -after[f])
    return {"sid": out.get("session_id"), "text": out.get("result", ""), "files": made[:4]}


def status():
    exe = claude_bin()
    signed = False
    if exe:
        try:
            r = subprocess.run([exe, "auth", "status"], capture_output=True, text=True, timeout=20,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            signed = r.returncode == 0 and "claude.ai" in r.stdout
        except Exception:
            signed = False
    o = orbit()
    return {"lucid": VERSION, "chats": bool(exe) and signed, "claude": bool(exe), "signed_in": signed,
            "world": os.path.exists(WORLD), "orbit": o["docked"], "orbit_url": o["url"], "url": f"http://127.0.0.1:{PORT}/"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body, ctype, extra=None):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def file(self, path, ctype):
        try:
            with open(path, "rb") as f:
                return self.send(200, f.read(), ctype)
        except OSError:
            return self.send(404, "not found", "text/plain")

    def do_GET(self):
        p = self.path.split("?")[0].split("#")[0]
        if p == "/api/door":  # the Orbit hub asks this to show its Studio door: says only "here", nothing about your work
            origin = self.headers.get("Origin") or ""
            if origin in ORBIT_ORIGINS:
                return self.send(200, json.dumps({"lucid": VERSION, "url": f"http://127.0.0.1:{PORT}/"}), "application/json",
                                 {"Access-Control-Allow-Origin": origin})
            return self.send(403, "forbidden", "text/plain")
        if self.headers.get("Host") not in HOSTS:  # everything else: only this computer's own browser
            return self.send(403, "forbidden", "text/plain")
        if p in ("/", "/index.html"):
            return self.file(os.path.join(STUDIO, "Your studio.html"), "text/html; charset=utf-8")
        if p == "/api/world":
            w = load_world()
            return self.send(200, json.dumps(w) if w else "null", "application/json")
        if p == "/api/status":
            return self.send(200, json.dumps(status()), "application/json")
        if p == "/api/folder":
            return self.send(200, STUDIO, "text/plain; charset=utf-8")
        if p == "/api/quit":  # the start file uses this to switch to a new Lucid Studio folder
            self.send(200, "bye", "text/plain")
            return threading.Thread(target=self.server.shutdown, daemon=True).start()
        if p.startswith("/out/"):
            name = os.path.basename(p[5:].replace("%20", " "))
            kind = {"html": "text/html; charset=utf-8", "png": "image/png", "jpg": "image/jpeg", "svg": "image/svg+xml", "pdf": "application/pdf"}
            ext = name.rsplit(".", 1)[-1].lower()
            if ext in kind:
                return self.file(os.path.join(OUT_DIR, name), kind[ext])
        name = p.lstrip("/").replace("%20", " ")
        if "/" not in name and "\\" not in name and not name.startswith(".") and name.rsplit(".", 1)[-1].lower() in FILES and name != "lucid-world.json":
            return self.file(os.path.join(STUDIO, name), FILES[name.rsplit(".", 1)[-1].lower()])
        self.send(404, "not found", "text/plain")

    def body(self):
        return json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))

    def do_PUT(self):
        # Only the studio page sends this header, so other websites can't change your world.
        if self.headers.get("Host") not in HOSTS or self.headers.get("X-Lucid") != "1" or self.path != "/api/world":
            return self.send(403, "forbidden", "text/plain")
        try:
            w = self.body()
            assert isinstance(w, dict) and isinstance(w.get("rooms"), list)
        except Exception:
            return self.send(400, "That isn't a Lucid world.", "text/plain")
        save_world(w)
        self.send(200, "saved", "text/plain")

    def do_POST(self):
        if self.headers.get("Host") not in HOSTS or self.headers.get("X-Lucid") != "1":
            return self.send(403, "forbidden", "text/plain")
        if self.path != "/api/chat":
            return self.send(404, "not found", "text/plain")
        try:
            data = self.body()
            room, project, msg, sid = data["room"], data.get("project"), data["msg"].strip(), data.get("sid")
            assert ID_RE.fullmatch(room) and 0 < len(msg) < 12000
            assert project is None or ID_RE.fullmatch(project)
            assert sid is None or SID_RE.fullmatch(sid)
        except Exception:
            return self.send(400, "bad chat", "text/plain")
        with LOCK:
            if BUSY.get(room):
                return self.send(409, "Still working on your last message. One moment.", "text/plain")
            BUSY[room] = True
        try:
            out = run_chat(room, project, msg, sid)
        except FileNotFoundError as e:
            return self.send(424, str(e), "text/plain")
        except subprocess.TimeoutExpired:
            return self.send(504, "That took too long. Try again, or ask for something smaller.", "text/plain")
        except Exception as e:
            return self.send(502, str(e), "text/plain")
        finally:
            BUSY[room] = False
        self.send(200, json.dumps(out), "application/json")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError:
        print("Lucid is already running.")
        return
    with open(os.path.join(HERE, "studio-folder.txt"), "w", encoding="utf-8") as f:
        f.write(STUDIO)
    print(f"Lucid is running at http://127.0.0.1:{PORT}  (keep this running; it uses no API key)")
    srv.serve_forever()


if __name__ == "__main__":
    main()
