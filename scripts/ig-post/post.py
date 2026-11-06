"""Instagram posting robot (GitHub Actions, no Claude needed).
Every run: for each slot in slots.json that is due (and not more than 24 h late), publish it from
branch nov-orbit-swap via the Instagram Graph API, unless Instagram already has a post with the
same caption (so it never double-posts with the Claude routine or a manual post).
Env: IG_ACCESS_TOKEN (repo secret). DRY_RUN=1 builds containers but never publishes."""
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


def publish(f, cap):
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
    p = api("POST", f"{U}/media_publish", creation_id=c)["id"]
    return "published " + api("GET", p, fields="permalink")["permalink"]


S = json.load(open(os.path.join(HERE, "slots.json")))
tz = ZoneInfo(S["tz"])
now = dt.datetime.now(tz)
# Wait a few minutes past the slot so a Claude routine posting the same slot goes first;
# the caption check below then sees it and skips.
GRACE = dt.timedelta(minutes=8)
due = []
for f, t in S["slots"]:
    when = dt.datetime.strptime(t, "%Y-%m-%d %H:%M").replace(tzinfo=tz)
    if (ONLY and f == ONLY) or (not ONLY and when + GRACE <= now <= when + dt.timedelta(hours=24)):
        due.append((f, t))
if not due:
    sys.exit(print(f"{now:%a %d %b %H:%M} Melbourne: nothing due"))

live = {key(m.get("caption") or ""): m.get("permalink")
        for m in api("GET", f"{U}/media", fields="caption,permalink", limit=40).get("data", [])}
failed = False
for f, t in due:
    cap = caption(f)
    if "orbit" in cap.lower():
        # Orbit is off every touchpoint (6 Nov 2026): never post a caption that still mentions it
        failed = True
        print(f"{f} ({t}): HELD, caption on {BRANCH} still mentions Orbit")
        continue
    if key(cap) in live:
        print(f"{f} ({t}): already on Instagram {live[key(cap)]}")
        continue
    try:
        print(f"{f} ({t}): {publish(f, cap)}")
    except BaseException as e:
        failed = True
        print(f"{f} ({t}): FAILED {e}")
sys.exit(1 if failed else 0)
