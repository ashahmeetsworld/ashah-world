"""Instagram posting robot v2.0 (GitHub Actions, no Claude needed). 28 Nov 2026.
GitHub's own timer started this robot only every 6 to 10 hours (reel4 was missed on 27 Nov), so
the robot now keeps its own clock: each run posts anything due (catching up slots up to 7 days
late), then stays awake and posts the next slot on the minute if it is within the next ~5.5 hours,
then starts the next run itself. The GitHub timer stays on only to restart the chain if it breaks.
Never double-posts: a slot is skipped if posted.json has it, Instagram already has its caption, or
any post went up between this slot's time and the next slot's time. Checked again right before
publishing. Env: IG_ACCESS_TOKEN (repo secret). DRY_RUN=1 builds containers but never publishes."""
import os, sys, json, time, datetime as dt, urllib.parse, urllib.request
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.environ["IG_ACCESS_TOKEN"]
DRY = bool(os.environ.get("DRY_RUN"))
ONLY = os.environ.get("ONLY", "").strip()  # manual run: post this one folder now
B = "https://graph.instagram.com/v26.0" if T.startswith("IG") else "https://graph.facebook.com/v26.0"
BRANCH = "nov-orbit-swap"
RAW = f"https://raw.githubusercontent.com/ashahmeetsworld/ashah-world/{BRANCH}/"
GH = "https://api.github.com/repos/ashahmeetsworld/ashah-world/contents/"
U = "17841443383606084"  # @ashah.world


def api(m, p, **kw):
    kw["access_token"] = T
    d = urllib.parse.urlencode(kw)
    req = urllib.request.Request(f"{B}/{p}" + ("?" + d if m == "GET" else ""),
                                 data=None if m == "GET" else d.encode(), method=m)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print("ERR", e.read().decode()[:500].replace(T, "***"))
        raise


def get(url, auth=False):
    req = urllib.request.Request(url)
    if auth and os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", "Bearer " + os.environ["GITHUB_TOKEN"])
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode()


def key(s):
    return " ".join(s.split())[:80]


def caption(f):
    if f.startswith("reel"):
        return get(RAW + f"reels/reel{f[4:]}-caption.txt").strip()
    return get(RAW + f + "/caption.txt").strip()


def wait(i):
    for _ in range(120):
        s = api("GET", i, fields="status_code").get("status_code")
        if s in ("FINISHED", None):
            return
        if s == "ERROR":
            raise SystemExit("container error " + i)
        time.sleep(5)
    raise SystemExit("timeout " + i)


def publish(f, cap, when):
    if f.startswith("reel"):
        n = f[4:]
        c = api("POST", f"{U}/media", media_type="REELS", video_url=RAW + f"reels/reel{n}.mp4",
                cover_url=RAW + f"reels/reel{n}-cover.jpg", caption=cap, share_to_feed="true")["id"]
        wait(c)
    else:
        names = sorted(x["name"] for x in json.loads(get(GH + f + "?ref=" + BRANCH, auth=True)))
        media = [x for x in names if x[:2].isdigit() and x.endswith((".mp4", ".jpg"))]
        try:
            tags = json.loads(get(RAW + f + "/tags.json")) if "tags.json" in names else {}
        except Exception:
            tags = {}
        kids = []
        for x in media:
            if x.endswith(".mp4"):
                r = api("POST", f"{U}/media", media_type="VIDEO", video_url=RAW + f + "/" + x, is_carousel_item="true")
            elif x in tags:
                ut = json.dumps([{"username": u, "x": 0.5, "y": 0.55} for u in tags[x]])
                try:
                    r = api("POST", f"{U}/media", image_url=RAW + f + "/" + x, is_carousel_item="true", user_tags=ut)
                except Exception:
                    print("tag failed, posting", x, "without tag")
                    r = api("POST", f"{U}/media", image_url=RAW + f + "/" + x, is_carousel_item="true")
            else:
                r = api("POST", f"{U}/media", image_url=RAW + f + "/" + x, is_carousel_item="true")
            kids.append(r["id"])
            print(" ", x, r["id"])
        for k in kids:
            wait(k)
        c = api("POST", f"{U}/media", media_type="CAROUSEL", children=",".join(kids), caption=cap)["id"]
        wait(c)
    if DRY:
        return "dry run OK (container built, not published)"
    link = slot_done(f, when, recent_posts(), cap)  # last check right before going live
    if link and not ONLY:
        return f"skipped, a post went live while this was being built {link}"
    p = api("POST", f"{U}/media_publish", creation_id=c)["id"]
    return "published " + api("GET", p, fields="permalink")["permalink"]


S = json.load(open(os.path.join(HERE, "slots.json")))
tz = ZoneInfo(S["tz"])
GRACE = dt.timedelta(minutes=2)          # post this long after the slot time (lets a Claude run go first)
CATCH_UP = dt.timedelta(days=7)          # a missed slot still goes out up to 7 days late
AWAKE = dt.timedelta(hours=5, minutes=30)  # how long one run stays awake waiting for the next slot
EARLY = dt.timedelta(minutes=15)
posted = json.load(open(os.path.join(HERE, "posted.json")))
SLOTS = sorted((dt.datetime.strptime(t, "%Y-%m-%d %H:%M").replace(tzinfo=tz), f) for f, t in S["slots"])


def slot_done(f, when, recent, cap=None):
    """Link of the post that already covers this slot, or None."""
    if f in posted:
        return posted[f]
    if cap is not None:
        for m in recent:
            if key(m.get("caption") or "") == key(cap):
                return m.get("permalink")
    later = [w for w, _ in SLOTS if w > when]
    end = (later[0] - EARLY) if later else None
    others = {key(c) for g, c in all_captions().items() if g != f and c}
    for m in recent:
        if key(m.get("caption") or "") in others:
            continue  # that post is another slot's (for example a late catch-up), not this one
        ts = dt.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        if ts >= when - EARLY and (end is None or ts < end):
            return m.get("permalink")
    return None


_caps = {}


def all_captions():
    for _, g in SLOTS:
        if g not in _caps:
            try:
                _caps[g] = caption(g)
            except Exception:
                _caps[g] = ""
    return _caps


def recent_posts():
    return api("GET", f"{U}/media", fields="caption,permalink,timestamp", limit=40).get("data", [])


def handle(f, when):
    """Post one slot unless it is already covered. Returns True if it failed."""
    t = f"{when:%Y-%m-%d %H:%M}"
    link = slot_done(f, when, recent_posts())
    if link and not ONLY:
        print(f"{f} ({t}): already live {link}")
        return False
    cap = caption(f)
    if "orbit" in cap.lower():
        # Orbit is off every touchpoint (6 Nov 2026): never post a caption that still mentions it
        print(f"{f} ({t}): HELD, caption on {BRANCH} still mentions Orbit")
        return True
    link = slot_done(f, when, recent_posts(), cap)
    if link:
        print(f"{f} ({t}): already live {link}")
        return False
    try:
        print(f"{f} ({t}): {publish(f, cap, when)}", flush=True)
        return False
    except BaseException as e:
        print(f"{f} ({t}): FAILED {e}")
        return True


def relay():
    """Start the next robot run (workflow_dispatch is allowed with the job's own GITHUB_TOKEN)."""
    req = urllib.request.Request(
        "https://api.github.com/repos/ashahmeetsworld/ashah-world/actions/workflows/ig-post.yml/dispatches",
        data=json.dumps({"ref": "main"}).encode(), method="POST",
        headers={"Authorization": "Bearer " + os.environ.get("GITHUB_TOKEN", ""),
                 "Accept": "application/vnd.github+json"})
    try:
        urllib.request.urlopen(req, timeout=60).read()
        print("next run started")
    except Exception as e:
        print("could not start the next run (the GitHub timer will):", e)


def due_now(now):
    if ONLY:
        return [(w, f) for w, f in SLOTS if f == ONLY]
    return [(w, f) for w, f in SLOTS if w + GRACE <= now <= w + CATCH_UP and f not in posted]


failed = False
started = dt.datetime.now(tz)
print(f"{started:%a %d %b %H:%M} Melbourne: robot v2.0 awake")
for w, f in due_now(started):
    failed |= handle(f, w)
if not ONLY:
    # Stay awake for any slot coming up before this run ends, and post it on the minute.
    for w, f in SLOTS:
        now = dt.datetime.now(tz)
        if now < w + GRACE <= started + AWAKE and f not in posted:
            print(f"{now:%a %d %b %H:%M} Melbourne: waiting for {f} ({w:%a %d %b %H:%M})", flush=True)
            time.sleep(max(0, (w + GRACE - now).total_seconds()))
            failed |= handle(f, w)
    nxt = [(w, f) for w, f in SLOTS if w > dt.datetime.now(tz) and f not in posted]
    print(f"{dt.datetime.now(tz):%a %d %b %H:%M} Melbourne: next slot "
          + (f"{nxt[0][1]} ({nxt[0][0]:%a %d %b %H:%M})" if nxt else "none scheduled"), flush=True)
    if nxt and not DRY:
        # Keep the chain going: rest out the rest of this run, then start the next run ourselves.
        rest = (started + AWAKE - dt.datetime.now(tz)).total_seconds()
        if rest > 0:
            time.sleep(rest)
        relay()
sys.exit(1 if failed else 0)
