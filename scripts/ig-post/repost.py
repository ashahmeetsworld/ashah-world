"""Re-post a live carousel as a fresh copy (e.g. with the hook's sound stripped, so Ashah can add
his own music in the Instagram app), then he deletes the old post himself.

Steps for any carousel FOLDER (ig12, ig19...):
  1. Copy the folder from branch nov-orbit-swap to ig-repost/FOLDER/ and strip sound from videos:
       ffmpeg -i 01.mp4 -an -c:v copy -movflags +faststart out.mp4
  2. Commit and push ig-repost/FOLDER to BRANCH below (raw GitHub URLs feed the API).
  3. python3 scripts/ig-post/repost.py FOLDER        -> dry run: builds containers, never publishes
     python3 scripts/ig-post/repost.py FOLDER --go   -> publishes (only after Ashah's "go")
Unlike post.py it does not skip a caption that is already live: a repost reuses the same caption.
Env: IG_ACCESS_TOKEN."""
import os, sys, json, time, urllib.parse, urllib.request

T = os.environ["IG_ACCESS_TOKEN"]
B = "https://graph.instagram.com/v26.0" if T.startswith("IG") else "https://graph.facebook.com/v26.0"
BRANCH = os.environ.get("REPOST_BRANCH", "claude/project-thread-3y2jzb")
U = "17841443383606084"  # @ashah.world
F = sys.argv[1]
GO = "--go" in sys.argv
RAW = f"https://raw.githubusercontent.com/ashahmeetsworld/ashah-world/{BRANCH}/ig-repost/{F}/"
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "ig-repost", F)


def api(m, p, **kw):
    kw["access_token"] = T
    d = urllib.parse.urlencode(kw)
    req = urllib.request.Request(f"{B}/{p}" + ("?" + d if m == "GET" else ""),
                                 data=None if m == "GET" else d.encode(), method=m)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit("ERR " + e.read().decode()[:500].replace(T, "***"))


def wait(i):
    for _ in range(120):
        s = api("GET", i, fields="status_code").get("status_code")
        if s in ("FINISHED", None):
            return
        if s == "ERROR":
            sys.exit("container error " + i)
        time.sleep(5)
    sys.exit("timeout " + i)


cap = open(os.path.join(HERE, "caption.txt")).read().strip()
if "orbit" in cap.lower():
    sys.exit("caption mentions Orbit: refusing")
media = sorted(x for x in os.listdir(HERE) if x[:2].isdigit() and x.endswith((".mp4", ".jpg")))
kids = []
for x in media:
    kw = dict(media_type="VIDEO", video_url=RAW + x) if x.endswith(".mp4") else dict(image_url=RAW + x)
    kids.append(api("POST", f"{U}/media", is_carousel_item="true", **kw)["id"])
    print(" ", x, kids[-1])
for k in kids:
    wait(k)
c = api("POST", f"{U}/media", media_type="CAROUSEL", children=",".join(kids), caption=cap)["id"]
wait(c)
if not GO:
    sys.exit(print(f"dry run OK: {len(kids)} slides built, nothing published"))
p = api("POST", f"{U}/media_publish", creation_id=c)["id"]
print("published", api("GET", p, fields="permalink")["permalink"])
