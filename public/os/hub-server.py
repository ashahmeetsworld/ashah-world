"""Orbit hub with chats inside (Phase 2).

Runs on your own computer only (http://127.0.0.1:4777). It shows your hub and lets
each helper chat with you right there, through Claude Code signed in to your own
Claude plan. No API key, no extra cost: it uses your plan's normal usage.
Nothing here is sent anywhere except your chats, to Claude, like any Claude chat.

Started by "Start Orbit Hub" once "Turn on hub chats" has run. Needs only Python 3
(the start file brings its own through uv) and Claude Code.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSION = "1"
HERE = os.path.dirname(os.path.abspath(__file__))  # ~/.orbit: the engine, kept outside the hub folder so updates never switch chats off
HUB = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else HERE  # their Orbit Hub folder
PORT = 4777
CHAT_DIR = os.path.join(HERE, "chats")
TEAM_DIR = os.path.join(HUB, "team")
OUT_DIR = os.path.join(CHAT_DIR, "out")
HOSTS = {f"127.0.0.1:{PORT}", f"localhost:{PORT}"}
ID_RE = re.compile(r"[a-z][a-z0-9-]{0,30}")
SID_RE = re.compile(r"[0-9a-f-]{36}")
NAMES = {"desk": "Front Desk", "mentor": "Mentor", "board": "Advisory Board", "ops": "Operations", "fo": "Funnel",
         "bd": "Business Development", "cs": "Client Success", "cp": "Content", "cd": "Creative Director"}
BUSY = {}
FILES = {"js": "text/javascript; charset=utf-8", "css": "text/css; charset=utf-8", "json": "application/json", "png": "image/png",
         "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp", "svg": "image/svg+xml", "woff2": "font/woff2"}
LOCK = threading.Lock()

BRIEF = """You are {name}, one of {who}'s Orbit helpers, chatting with them inside their Orbit hub on their own computer.
{skill_line}
Read CLAUDE.md in this folder for who they are and the shared rules. Their team's memory is their Notion (the notion tools): look there before you ask.
Replies are short and plain: the point first, like explaining to a smart 9-year-old, warm but not cheesy. One short question when you're unsure.
Put drafts in the reply itself. For anything visual (a board, a storyboard, a one-pager, a calendar), write ONE self-contained .html file into the out folder (out/<short-name>.html, dark background, light text) and say its name in one line: the hub shows it as a button.
Never send, post, publish or change anything outside this chat without their clear OK here. Never ask them to open a terminal or run a command.
Ongoing suggestions: whenever this chat shows a better way to work (a correction, a preference, friction, a repeated step a routine, skill or memory could handle), offer it then. Add one last line exactly: RECO: <the suggestion, one short line> | <Routine, Skill, Memory, Hub, Tool or Process>. At most one per reply, only when genuinely useful."""

LESSON = """You are {who}'s Mentor, teaching one layer of one topic inside their hub's lesson page. Layers: 1 foundations, 2 working depth, 3 mastery.
Every reply is short and plain (no walls of text, never more than about 120 words of prose), like explaining to a smart 9-year-old, warm but not cheesy.
First reply: open with one short line saying you are an AI mentor (Claude). Then explain the layer simply through ONE analogy from outside their field, then ask ONE effective question that tests understanding (not recall of your words: make them explain, apply it to a new case, or spot it done badly).
Every first reply, and any reply that brings a new analogy, also includes a picture of the analogy as one SVG in a fenced ```svg block: viewBox 0 0 400 300, line art only, stroke currentColor, fill none, stroke-width 1.5, no text longer than 3 words, no scripts or external links.
After each answer: say what they got right and what's missing in a line or two, then ask the next single question. They answer first; you reveal after.
When they have clearly proven the layer (explained it in their own words AND applied it to a new case), say so in one line and end your reply with the exact line: LAYER PROVEN
Tie examples to their business when it helps (CLAUDE.md, their Notion). Never invent facts, studies or quotes. Never use person names in examples; use roles.
Ongoing suggestions: when something shows a better way to work, add one last line exactly: RECO: <the suggestion, one short line> | <Routine, Skill, Memory, Hub, Tool or Process>. At most one per reply."""


def world():
    """Their world file (orbit-world.js), for names and helpers."""
    try:
        raw = open(os.path.join(HUB, "orbit-world.js"), encoding="utf-8").read().strip()
        raw = re.sub(r"^window\.ORBIT_WORLD\s*=\s*", "", raw).rstrip(";").strip()
        return json.loads(raw)
    except Exception:
        return {}


def helper_name(hid, w):
    h = (w.get("helpers") or {}).get(hid) or {}
    return h.get("name") or NAMES.get(hid) or hid.replace("-", " ").title()


def sync_team():
    """Copies the team folder (each helper's instructions and the sources of truth) to where Claude Code finds it.
    team/<id>.md becomes the skill orbit-<id>; team/sources/* goes to chats/sources; team/about.md becomes CLAUDE.md."""
    os.makedirs(OUT_DIR, exist_ok=True)
    if not os.path.isdir(TEAM_DIR):
        return
    w = world()
    for f in os.listdir(TEAM_DIR):
        src = os.path.join(TEAM_DIR, f)
        if f == "sources" and os.path.isdir(src):
            dst = os.path.join(CHAT_DIR, "sources")
            os.makedirs(dst, exist_ok=True)
            for s in os.listdir(src):
                if os.path.isfile(os.path.join(src, s)):
                    shutil.copyfile(os.path.join(src, s), os.path.join(dst, s))
        elif f == "about.md":
            shutil.copyfile(src, os.path.join(CHAT_DIR, "CLAUDE.md"))
        elif f.endswith(".md") and ID_RE.fullmatch(f[:-3]):
            hid = f[:-3]
            body = open(src, encoding="utf-8").read()
            if not body.startswith("---"):
                name = helper_name(hid, w)
                body = f"---\nname: orbit-{hid}\ndescription: How {name} works. Always use it when chatting as {name}.\n---\n\n" + body
            d = os.path.join(CHAT_DIR, ".claude", "skills", "orbit-" + hid)
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as o:
                o.write(body)
    if not os.path.exists(os.path.join(CHAT_DIR, "CLAUDE.md")):
        you = w.get("you") or {}
        with open(os.path.join(CHAT_DIR, "CLAUDE.md"), "w", encoding="utf-8") as o:
            o.write(f"# {you.get('brand') or you.get('name') or 'Their'} Orbit\n\nWho they are, their brand, customer, offer and rules live in their Notion and in the sources folder here. Read before you ask.\n")


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
        return "Claude isn't signed in on this computer any more. Double-click Turn on hub chats in your Orbit Hub folder to sign in again (one click)."
    return "Something went wrong on Claude's side: " + err[:240]


def out_files():
    try:
        return {f: os.path.getmtime(os.path.join(OUT_DIR, f)) for f in os.listdir(OUT_DIR) if f.lower().endswith((".html", ".png", ".jpg", ".svg", ".pdf"))}
    except OSError:
        return {}


def run_chat(hid, msg, sid=None):
    exe = claude_bin()
    if not exe:
        raise FileNotFoundError("Claude Code isn't on this computer yet. Double-click Turn on hub chats in your Orbit Hub folder.")
    sync_team()
    w = world()
    name = helper_name(hid, w)
    who = ((w.get("you") or {}).get("first_name")) or "the founder"
    skill = os.path.isdir(os.path.join(CHAT_DIR, ".claude", "skills", "orbit-" + hid))
    if hid == "mentor-lesson":
        brief = LESSON.format(who=who)
    else:
      brief = BRIEF.format(name=name, who=who, skill_line=(f"Follow the orbit-{hid} skill: it's how you work." if skill else
                         "Your full instructions are in their Claude Project for you; here, work from CLAUDE.md, the sources folder and their Notion."))
    cmd = [exe, "-p", msg, "--output-format", "json", "--append-system-prompt", brief,
           "--allowedTools", "Read", "Glob", "Grep", "WebSearch", "WebFetch", "Skill", "mcp__notion", "Edit(./out/**)", "Write(./out/**)",
           "--disallowedTools", "Bash", "PowerShell", "NotebookEdit"]
    if sid:
        cmd += ["--resume", sid]
    # No API key passes through, so Claude Code always uses their Claude plan, never paid API usage.
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL")}
    before = out_files()
    r = subprocess.run(cmd, cwd=CHAT_DIR, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900,
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
    return {"chats": bool(exe) and signed, "claude": bool(exe), "signed_in": signed, "team": os.path.isdir(TEAM_DIR), "server": VERSION}


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
        if self.headers.get("Host") not in HOSTS:  # only this computer's own browser
            return self.send(403, "forbidden", "text/plain")
        p = self.path.split("?")[0].split("#")[0]
        if p in ("/", "/index.html", "/Your%20hub.html"):
            page = os.path.join(HUB, "Your hub.html")
            if not os.path.exists(page):
                page = os.path.join(os.path.dirname(HUB), "04 Hub demo.html")
            return self.file(page, "text/html; charset=utf-8")
        if p == "/orbit-world.js":
            return self.file(os.path.join(HUB, "orbit-world.js"), "text/javascript; charset=utf-8")
        name = p.lstrip("/").replace("%20", " ")
        if "/" not in name and "\\" not in name and not name.startswith(".") and name.rsplit(".", 1)[-1].lower() in FILES:
            return self.file(os.path.join(HUB, name), FILES[name.rsplit(".", 1)[-1].lower()])  # e.g. orbit-skin.js
        if p == "/ping.gif":
            return self.send(200, b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;", "image/gif")
        if p == "/api/folder":
            return self.send(200, HUB, "text/plain; charset=utf-8")
        if p == "/api/quit":  # the start file uses this to switch to a new Orbit Hub folder
            self.send(200, "bye", "text/plain")
            return threading.Thread(target=self.server.shutdown, daemon=True).start()
        if p == "/api/status":
            return self.send(200, json.dumps(status()), "application/json")
        if p.startswith("/out/"):
            name = os.path.basename(p[5:].replace("%20", " "))
            kind = {"html": "text/html; charset=utf-8", "png": "image/png", "jpg": "image/jpeg", "svg": "image/svg+xml", "pdf": "application/pdf"}
            ext = name.rsplit(".", 1)[-1].lower()
            if ext in kind:
                return self.file(os.path.join(OUT_DIR, name), kind[ext])
        self.send(404, "not found", "text/plain")

    def do_POST(self):
        # Only the hub page sends this header, so other websites can't use the chats.
        if self.headers.get("Host") not in HOSTS or "1" not in (self.headers.get("X-Orbit-Hub"), self.headers.get("X-AMW-Hub")):
            return self.send(403, "forbidden", "text/plain")
        if self.path != "/api/chat":
            return self.send(404, "not found", "text/plain")
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            hid, msg, sid = data.get("helper") or data["seat"], data["msg"].strip(), data.get("sid")
            assert ID_RE.fullmatch(hid) and 0 < len(msg) < 12000
            assert sid is None or SID_RE.fullmatch(sid)
        except Exception:
            return self.send(400, "bad chat", "text/plain")
        with LOCK:
            if BUSY.get(hid):
                return self.send(409, "Still working on your last message. One moment.", "text/plain")
            BUSY[hid] = True
        try:
            out = run_chat(hid, msg, sid)
        except FileNotFoundError as e:
            return self.send(424, str(e), "text/plain")
        except subprocess.TimeoutExpired:
            return self.send(504, "That took too long. Try again, or ask for something smaller.", "text/plain")
        except Exception as e:
            return self.send(502, str(e), "text/plain")
        finally:
            BUSY[hid] = False
        self.send(200, json.dumps(out), "application/json")


def main():
    try:
        sync_team()
    except Exception:
        pass
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError:
        print("Your hub is already running.")
        return
    with open(os.path.join(HERE, "hub-folder.txt"), "w", encoding="utf-8") as f:
        f.write(HUB)
    print(f"Your Orbit hub is running at http://127.0.0.1:{PORT}  (keep this running; it uses no API key)")
    srv.serve_forever()


if __name__ == "__main__":
    main()
