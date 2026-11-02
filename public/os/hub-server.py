"""Orbit hub with chats inside (Phase 2).

Runs on your own computer only (http://127.0.0.1:4777). It shows your hub and lets
each helper chat with you right there, through Claude Code signed in to your own
Claude plan. No API key, no extra cost: it uses your plan's normal usage.
Nothing here is sent anywhere except your chats, to Claude, like any Claude chat.

Started by "Start Orbit Hub" once "Bring your hub to life" (once called "Turn on hub chats") has run. Needs only Python 3
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
NAMES = {"desk": "Personal Assistant", "mentor": "Mentor", "board": "Advisory Board", "ops": "Operations", "fo": "Funnel",
         "bd": "Business Development", "cs": "Client Success", "cp": "Content", "cd": "Creative Director", "coach": "Coach"}
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
Set and forget: anything you set up runs on autopilot until it hits a hard wall. If you need them, do 99% of the prep, pause, tell them exactly what one action to take, and wait for their "go" to finish.
Ongoing suggestions: whenever this chat shows a better way to work (a correction, a preference, friction, a repeated step a routine, skill or memory could handle), offer it then. Add one last line exactly: RECO: <the suggestion, one short line> | <Routine, Skill, Memory, Hub, Tool or Process>. At most one per reply, only when genuinely useful.
The team mailbox (Orbit v0.4.6; your hub carries it, nothing to set up): your helpers keep each other posted so {who} isn't the messenger.
- Start: their message may begin with a [Team mailbox] block. Read it first. Use the updates, answer any ask you can with a line ANSWER: <id> | <the answer, one line>, and use answers to your own asks. Say what changed in one line only if it matters; never repeat the block back.
- Mid-chat: don't know something another helper would know? Ask them, not {who}: ASK: <helper or All> | <the question>. Tell {who} "asked the team" and carry on. Only a real blocker goes to {who}: ASK: You | <the question>.
- End: anything from this chat another helper needs? UPDATE: <helper or All> | <what changed, one line>. Something for the hub itself (a new button, something now live, a recurring job)? HUB: <what> | <where it might go>.
- Catch: when {who} drops an idea in passing ("never use...", "I'd love it if..."), route it: apply it if it's yours, UPDATE the helper who owns it, or RECO it if it's a better way to work. Then show it in one line: 🪝 caught: "<their words>" → <where it went>.
- A reco from their hub that you were asked to apply has landed? DONE: <reco id> | <what changed, a few words>.
These lines go on their own lines at the very end, plain text, only when real. The hub turns them into small cards; never explain them."""

OPS_EXTRA = """
You keep their hub. A "hub post" (an idea for the hub from another helper) gets fitted by you: say in one line where it fits best, then end with
BUILD: <button, live or job> | <helper> | <label> | <the button's prompt, the thing's type, or how often the job runs> | <where it lands, in plain words> | <hub post id>
button = a new button in that helper's room; live = something now live, listed on home; job = a recurring job on the tracker. The hub asks them "Add to your hub?", backs up first and offers Undo.
If it doesn't fit any of those, say so plainly and suggest the closest thing. Recos check-outs: apply each with their OK, and close each one with its DONE line when it lands.
Weekly look-back: only fresh, open Recos. Anything untouched for 30 days is already marked outdated in their hub, with Keep or Let go: don't bring it up."""

LESSON = """You are {who}'s Mentor, teaching one layer of one topic inside their hub's lesson page. Layers: 1 foundations, 2 working depth, 3 mastery.
Every reply is short and plain (no walls of text, never more than about 120 words of prose), like explaining to a smart 9-year-old, warm but not cheesy.
First reply: open with one short line saying you are an AI mentor (Claude). Then explain the layer simply through ONE analogy from outside their field, then ask ONE effective question that tests understanding (not recall of your words: make them explain, apply it to a new case, or spot it done badly).
Every first reply, and any reply that brings a new analogy, also includes a picture of the analogy as one SVG in a fenced ```svg block: viewBox 0 0 400 300, line art only, stroke currentColor, fill none, stroke-width 1.5, no text longer than 3 words, no scripts or external links.
After each answer: say what they got right and what's missing in a line or two, then ask the next single question. They answer first; you reveal after.
When they have clearly proven the layer (explained it in their own words AND applied it to a new case), say so in one line and end your reply with the exact line: LAYER PROVEN
Tie examples to their business when it helps (CLAUDE.md, their Notion). Never invent facts, studies or quotes. Never use person names in examples; use roles.
Ongoing suggestions: when something shows a better way to work, add one last line exactly: RECO: <the suggestion, one short line> | <Routine, Skill, Memory, Hub, Tool or Process>. At most one per reply."""

COACH_EXTRA = """
You are their Coach, the third seat of their Council (Orbit v0.4.7): encouraging and energetic. You keep their life outside work strong, so the work stays strong.
Your plan for them and how you work live on the Coach page in their Notion (search "Coach"). Read it before you answer, and keep its log and look-backs up to date when they tell you what they did.
No Coach page yet, or they ask to set it up? Read https://ashahmeetsworld.github.io/ashah-world/os/Coach-setup.md in full (WebFetch) and follow it exactly.
You are not a doctor: anything that sounds like pain, injury or a crisis, say to stop and see a professional. Never use person names; name teachers and creators by role or style.
Only offer links you actually found. Never guilt them: one skip is fine, never two in a row, three in a row earns the skip back."""


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
        return "Claude isn't signed in on this computer any more. Double-click Bring your hub to life (Turn on hub chats in older folders) in your Orbit Hub folder to sign in again (one click)."
    return "Something went wrong on Claude's side: " + err[:240]


def out_files():
    try:
        return {f: os.path.getmtime(os.path.join(OUT_DIR, f)) for f in os.listdir(OUT_DIR) if f.lower().endswith((".html", ".png", ".jpg", ".svg", ".pdf"))}
    except OSError:
        return {}


def run_chat(hid, msg, sid=None):
    exe = claude_bin()
    if not exe:
        raise FileNotFoundError("Claude Code isn't on this computer yet. Double-click Bring your hub to life (Turn on hub chats in older folders) in your Orbit Hub folder.")
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
      if hid == "ops":
          brief += OPS_EXTRA
      if hid == "coach":
          brief = brief.replace("Your full instructions are in their Claude Project for you; here, work from CLAUDE.md, the sources folder and their Notion.", "Your instructions are below and on the Coach page in their Notion.") + COACH_EXTRA
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


# ---------- Voices (Orbit v0.4.8) ----------
# The Personal Assistant, the Council (Mentor, Advisory Board, Coach) and the six helpers answer out loud, each in its own voice,
# made on this computer for free (Kokoro, open source, Apache 2.0). Set up once, the first time they hold the mic:
# the voice engine goes into ~/.orbit/voice-lib and the voices (about 350MB) into ~/.orbit/voice. Until it's ready,
# the hub uses the browser's own voice. Nothing is sent anywhere.
VOICE_HOME = os.path.join(HERE, "voice")
VOICE_LIB = os.path.join(HERE, "voice-lib")
VOICE_LOG = os.path.join(HERE, "voice-status.txt")
VOICE_BASE = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
VOICE_FILES = {"kokoro-v1.0.onnx": 325532387, "voices-v1.0.bin": 28214398}
VOICES = {
    "desk": {"mix": {"af_heart": 1}, "lang": "en-us", "speed": 1.0},
    "coach": {"mix": {"am_onyx": 1}, "lang": "en-us", "speed": 1.0, "pitch": 0.907, "chest": 0.467},
    "mentor": {"mix": {"bm_george": 1}, "lang": "en-gb", "speed": 0.92},
    "board": {"mix": {"bm_lewis": 1}, "lang": "en-gb", "speed": 0.95},
    # the team, each voiced to their personality
    "ops": {"mix": {"am_echo": 1}, "lang": "en-us", "speed": 1.0},          # witty: dry, quick
    "cd": {"mix": {"af_bella": 1}, "lang": "en-us", "speed": 1.0},          # expressive: warm, vivid
    "cp": {"mix": {"af_sky": 1}, "lang": "en-us", "speed": 1.05},           # playful: light, bubbly
    "bd": {"mix": {"am_michael": 1}, "lang": "en-us", "speed": 0.97},       # magnetic: smooth, assured
    "fo": {"mix": {"af_kore": 1}, "lang": "en-us", "speed": 1.02},          # direct: clear, no-nonsense
    "cs": {"mix": {"af_jessica": 1}, "lang": "en-us", "speed": 0.95},       # nurturing: gentle, caring
}
VOICE = {"state": "off", "note": "", "pct": 0}
VOICE_LOCK = threading.Lock()
SAY_LOCK = threading.Lock()
_kokoro = None


def vlog(line):
    try:
        with open(VOICE_LOG, "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + str(line)[:2000] + "\n")
    except OSError:
        pass


def voice_import():
    import importlib
    if os.path.isdir(VOICE_LIB) and VOICE_LIB not in sys.path:
        sys.path.insert(0, VOICE_LIB)
    importlib.invalidate_caches()
    return importlib.import_module("kokoro_onnx")


def voice_install():
    """The engine goes into its own folder (uv first, then pip), so it never touches anything else on their computer."""
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    home = os.path.expanduser("~")
    uv = shutil.which("uv") or next((p for p in (os.path.join(home, ".local", "bin", "uv.exe"), os.path.join(home, ".local", "bin", "uv")) if os.path.exists(p)), None)
    tries = []
    if uv:
        tries.append([uv, "pip", "install", "--quiet", "--python", sys.executable, "--target", VOICE_LIB, "kokoro-onnx"])
    tries.append([sys.executable, "-m", "pip", "install", "--quiet", "--disable-pip-version-check", "--target", VOICE_LIB, "kokoro-onnx"])
    err = ""
    for cmd in tries:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900, creationflags=flags)
        except Exception as e:
            err = str(e)
            continue
        if r.returncode == 0:
            return
        err = (r.stderr or r.stdout).strip()[-1500:]
        vlog("install try failed: " + err)
    raise RuntimeError("Couldn't install the voice engine: " + err[-300:])


def voice_download():
    import urllib.request
    os.makedirs(VOICE_HOME, exist_ok=True)
    total = sum(VOICE_FILES.values())
    done = sum(os.path.getsize(os.path.join(VOICE_HOME, f)) for f in VOICE_FILES if os.path.exists(os.path.join(VOICE_HOME, f)))
    for name, size in VOICE_FILES.items():
        dest = os.path.join(VOICE_HOME, name)
        if os.path.exists(dest) and os.path.getsize(dest) == size:
            continue
        part = dest + ".part"
        with urllib.request.urlopen(VOICE_BASE + name, timeout=60) as r, open(part, "wb") as f:
            while True:
                b = r.read(1 << 20)
                if not b:
                    break
                f.write(b)
                done += len(b)
                VOICE["pct"] = min(99, int(done * 100 / total))
        os.replace(part, dest)


def voice_setup():
    global _kokoro
    try:
        VOICE.update(state="installing", note="Setting up the voices", pct=0)
        vlog(f"start: python {sys.version.split()[0]}")
        try:
            kk = voice_import()
        except ImportError:
            vlog("installing the voice engine")
            voice_install()
            kk = voice_import()
        VOICE.update(note="Downloading the voices (about 350MB, once)")
        voice_download()
        _kokoro = kk.Kokoro(os.path.join(VOICE_HOME, "kokoro-v1.0.onnx"), os.path.join(VOICE_HOME, "voices-v1.0.bin"))
        VOICE.update(state="ready", note="", pct=100)
        vlog("ready")
    except Exception as e:
        import traceback
        VOICE.update(state="failed", note=str(e)[:300])
        vlog("FAILED: " + traceback.format_exc())


def voice_start():
    with VOICE_LOCK:
        if VOICE["state"] in ("installing", "ready"):
            return
        VOICE["state"] = "installing"
        VOICE["tried"] = time.time()
    threading.Thread(target=voice_setup, daemon=True).start()


def voice_say(hid, text):
    """One sentence in that seat's voice, as WAV bytes. Only clean changes (pitch, a little low warmth), never distortion."""
    import io
    import wave
    import numpy as np
    v = VOICES.get(hid) or VOICES["desk"]
    pitch, chest = float(v.get("pitch", 1)), float(v.get("chest", 0))
    with SAY_LOCK:
        style = sum(_kokoro.get_voice_style(n) * float(w) for n, w in v["mix"].items())
        a, sr = _kokoro.create(text, voice=style, speed=float(v.get("speed", 1)) / pitch, lang=v.get("lang", "en-us"))
    a = np.asarray(a, np.float32)
    if pitch != 1:
        a = np.interp(np.linspace(0, len(a) - 1, int(len(a) / pitch)), np.arange(len(a)), a).astype(np.float32)
    if chest:
        c = float(np.exp(-2 * np.pi * 220 / sr))
        lp = np.empty_like(a)
        y = 0.0
        for i, x in enumerate(a.tolist()):
            y = (1 - c) * x + c * y
            lp[i] = y
        a = a + chest * 1.8 * lp
    peak = float(np.abs(a).max()) if len(a) else 1.0
    a = a * (0.89 / (peak or 1.0))
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((np.clip(a, -1, 1) * 32767).astype("<i2").tobytes())
    return buf.getvalue()


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
        if p == "/api/upgrade/status":
            return self.send(200, json.dumps(up_status()), "application/json")
        if p == "/api/status":
            return self.send(200, json.dumps(status()), "application/json")
        if p == "/api/voice/status":  # ?start=1 sets the voices up (the first time they hold the mic)
            if "start=1" in self.path and (VOICE["state"] == "off" or (VOICE["state"] == "failed" and time.time() - VOICE.get("tried", 0) > 120)):
                voice_start()
            return self.send(200, json.dumps({k: VOICE[k] for k in ("state", "note", "pct")}), "application/json")
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
        if self.path == "/api/voice/say":
            try:
                data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
                hid, text = str(data.get("helper") or "desk"), str(data["text"]).strip()
                assert ID_RE.fullmatch(hid) and 0 < len(text) < 600
            except Exception:
                return self.send(400, "bad voice request", "text/plain")
            if VOICE["state"] != "ready":
                return self.send(503, json.dumps(VOICE), "application/json")
            try:
                return self.send(200, voice_say(hid, text), "audio/wav")
            except Exception as e:
                vlog("say failed: " + repr(e))
                return self.send(500, str(e)[:300], "text/plain")
        if self.path == "/api/upgrade/hub":
            refresh_hub_page()
            return self.send(200, json.dumps({"ok": True}), "application/json")
        if self.path == "/api/upgrade":
            try:
                n = int(self.headers.get("Content-Length", 0))
                start_upgrade(json.loads(self.rfile.read(n)) if 0 < n < 4000 else {})
            except Exception:
                return self.send(400, "bad upgrade", "text/plain")
            return self.send(200, json.dumps(up_status()), "application/json")
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


# ---------- Upgrade inside the hub (Orbit v0.4.7) ----------
# The hub's Update button runs the update here, on their own Claude plan, while the hub shows each step.
# Claude works on a copy of the team folder (chats/upgrade/team); only when it finishes cleanly is the copy put back,
# after a backup of the old one in <Orbit Hub>/backups. Nothing is ever deleted.
SITE = "https://ashahmeetsworld.github.io/ashah-world/os/"
UP_DIR = os.path.join(CHAT_DIR, "upgrade")
UP = {"state": "idle", "error": "", "version": ""}

UPGRADE = """You are their Orbit Operations helper, upgrading their Orbit team from inside their hub, on their own computer. They pressed Update in their hub: that is their OK for everything in the update file.
Read the update file in full ({update}) and follow Part 1, in HUB MODE:
- Their helpers' instructions live in ./upgrade/team/<helper id>.md (and ./upgrade/team/about.md is the shared CLAUDE.md). Refresh those files from Part 2, keeping every line they added or changed themselves. That is where the update lands.
- Notion: make any changes the update asks for with the notion tools. Never delete, rename or overwrite anything they wrote.
- No browser here: skip anything that needs Claude in Chrome (their claude.ai Projects) and skip making a zip or a fresh Orbit Hub folder (the hub updates itself). Don't ask them anything: there is nobody to answer. Fill blanks with a best guess marked [guess].
- Progress: after each real step, append ONE short plain line to ./upgrade/progress.txt starting with "STEP: " (for example "STEP: Content's instructions refreshed"). Six to ten steps in all.
- If something can only be done in Claude with Chrome (like their Projects' instructions), add one line "LATER: <what, in a few words>".
- When everything is done, append "DONE: <one line on what changed>".
Keep any reply to a single short line."""


def up_lines():
    try:
        with open(os.path.join(UP_DIR, "progress.txt"), encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip()]
    except OSError:
        return []


def up_status():
    lines = up_lines()
    later = [l[6:].strip() for l in lines if l.startswith("LATER:")]
    return {"state": UP["state"], "error": UP["error"], "version": UP["version"],
            "steps": [l[5:].strip() for l in lines if l.startswith("STEP:")][-14:], "later": "; ".join(later)[:200]}


def fetch_site(name, dest):
    import urllib.request
    with urllib.request.urlopen(SITE + name, timeout=15) as r:
        data = r.read()
    if len(data) < 1000:
        raise ValueError("too small")
    tmp = dest + ".new"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, dest)


def refresh_hub_page():
    """The newest hub page from the Orbit site, the same one Start Orbit Hub fetches."""
    try:
        fetch_site("hub.html", os.path.join(HUB, "Your hub.html"))
    except Exception:
        pass
    try:
        fetch_site("hub-server.py", os.path.join(HERE, "hub-server.py"))  # used from the next start
    except Exception:
        pass


def run_upgrade(version, update):
    try:
        exe = claude_bin()
        if not exe:
            raise RuntimeError("Claude Code isn't on this computer yet.")
        if os.path.isdir(UP_DIR):
            shutil.rmtree(UP_DIR)
        os.makedirs(UP_DIR)
        if os.path.isdir(TEAM_DIR):
            shutil.copytree(TEAM_DIR, os.path.join(UP_DIR, "team"))
        else:
            os.makedirs(os.path.join(UP_DIR, "team"))
        with open(os.path.join(UP_DIR, "progress.txt"), "w", encoding="utf-8") as f:
            f.write("STEP: Read the update\n")
        sync_team()
        msg = f"Upgrade my Orbit to v{version}. Run it in hub mode, now."
        cmd = [exe, "-p", msg, "--output-format", "json", "--append-system-prompt", UPGRADE.format(update=update),
               "--allowedTools", "Read", "Glob", "Grep", "WebFetch", "Skill", "mcp__notion", "Edit(./upgrade/**)", "Write(./upgrade/**)",
               "--disallowedTools", "Bash", "PowerShell", "NotebookEdit"]
        env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL")}
        r = subprocess.run(cmd, cwd=CHAT_DIR, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=2400,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        try:
            out = json.loads(r.stdout)
        except ValueError:
            raise RuntimeError(friendly((r.stderr or r.stdout or "no answer came back").strip()))
        if out.get("is_error"):
            raise RuntimeError(friendly(str(out.get("result") or out.get("subtype") or "error")))
        new_team = os.path.join(UP_DIR, "team")
        if os.path.isdir(new_team) and os.listdir(new_team):
            if os.path.isdir(TEAM_DIR):
                base = os.path.join(HUB, "backups", f"team-before-v{version}-{time.strftime('%Y-%m-%d-%H%M%S')}")
                dest, n = base, 2
                while os.path.exists(dest):  # never overwrite an earlier backup
                    dest, n = f"{base}-{n}", n + 1
                shutil.copytree(TEAM_DIR, dest)
            shutil.copytree(new_team, TEAM_DIR, dirs_exist_ok=True)
            sync_team()
        refresh_hub_page()
        with open(os.path.join(UP_DIR, "progress.txt"), "a", encoding="utf-8") as f:
            f.write("STEP: Your hub page refreshed\n")
        UP["state"] = "done"
    except subprocess.TimeoutExpired:
        UP["state"], UP["error"] = "error", "it took too long"
    except Exception as e:
        UP["state"], UP["error"] = "error", str(e)[:240]


def start_upgrade(data):
    version = str(data.get("version") or "")
    update = str(data.get("update") or SITE + "Update-your-Orbit.md")
    assert re.fullmatch(r"\d+\.\d+(\.\d+)?", version) and update.startswith(SITE)
    with LOCK:
        if UP["state"] == "running":
            return
        UP.update(state="running", error="", version=version)
    threading.Thread(target=run_upgrade, args=(version, update), daemon=True).start()


def main():
    try:
        sync_team()
    except Exception:
        pass
    if os.path.exists(os.path.join(VOICE_HOME, "voices-v1.0.bin")):  # set up before: wake the voices now
        voice_start()
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
