"""Orbit comment bot for @ashah.world.

Someone comments ORBIT (any case, punctuation, or a small typo) on a recent post.
The bot sends them the Orbit link by private DM, then hides their comment so the
comment section stays about the post.

Runs every few minutes on GitHub Actions (see .github/workflows/orbit-dm.yml).
No state file: a hidden comment counts as done, and Meta allows only one private
reply per comment, so a retry can never DM someone twice.

Env: IG_ACCESS_TOKEN (required), IG_USER_ID, DRY_RUN=1 to only report.
Python standard library only.
"""
import json, os, re, sys, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

GRAPH = "https://graph.facebook.com/v21.0"
def clean_token(raw):
    """Forgive paste slips: a copied 'IG_ACCESS_TOKEN=' prefix, quotes, spaces, line breaks."""
    t = re.sub(r"\s+", "", raw or "")
    if "=" in t and t.split("=", 1)[0].upper().endswith("TOKEN"):
        t = t.split("=", 1)[1]
    return t.strip("\"'`")


TOKEN = clean_token(os.environ.get("IG_ACCESS_TOKEN", ""))
IG_ID = os.environ.get("IG_USER_ID", "").strip() or "17841443383606084"
DRY = os.environ.get("DRY_RUN", "") not in ("", "0", "false")
LINK = "https://ashahmeetsworld.github.io/ashah-world/orbit/"
DM_TEXT = os.environ.get("ORBIT_DM_TEXT") or (
    "Here's Orbit, the free system I run my brand on: " + LINK
)
KEYWORD = "orbit"
WINDOW_DAYS = 7  # Meta only allows private replies within 7 days of the comment


def api(method, path, **params):
    params["access_token"] = TOKEN
    data = None
    url = f"{GRAPH}/{path}"
    if method == "GET":
        url += "?" + urllib.parse.urlencode(params)
    else:
        data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r), None
    except urllib.error.HTTPError as e:
        try:
            err = json.load(e).get("error", {})
        except Exception:
            err = {"message": str(e)}
        return None, err


def edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def wants_orbit(text):
    """True for ORBIT, orbit!, Orbit pls, orbt, orbitt, O R B I T, 'orbit 🙏'."""
    if not text:
        return False
    low = text.lower()
    letters = re.sub(r"[^a-z]", "", low)
    if letters and edit_distance(letters, KEYWORD) <= 1:
        return True  # whole comment is (nearly) the keyword, spaced or not
    for word in re.findall(r"[a-z]+", low):
        if 4 <= len(word) <= 7 and edit_distance(word, KEYWORD) <= 1:
            return True
    return False


def parse_time(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z")


def main():
    if not TOKEN:
        print("IG_ACCESS_TOKEN secret not added yet, nothing to do")
        return
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=WINDOW_DAYS)
    # safe hint for debugging a bad paste: never prints the token itself
    print(f"token check: {len(TOKEN)} characters, starts with {TOKEN[:2]!r}")
    media, err = api("GET", f"{IG_ID}/media", fields="id,timestamp,permalink", limit=25)
    if err:
        sys.exit(f"Could not read posts: {err.get('message')}")
    sent = skipped = failed = 0
    for m in media.get("data", []):
        # comments can arrive on older posts too, so check every listed post
        comments, err = api(
            "GET", f"{m['id']}/comments", limit=50,
            fields="id,text,hidden,timestamp,from,replies{id,text,hidden,timestamp,from}",
        )
        if err:
            print(f"! could not read comments on {m.get('permalink')}: {err.get('message')}")
            failed += 1
            continue
        flat = []
        for c in comments.get("data", []):
            flat.append(c)
            flat.extend(c.get("replies", {}).get("data", []))
        for c in flat:
            who = (c.get("from") or {})
            if who.get("id") == IG_ID or c.get("hidden"):
                continue
            if not wants_orbit(c.get("text", "")):
                continue
            if parse_time(c["timestamp"]) < cutoff:
                continue  # too old for a private reply
            tag = f"@{who.get('username', '?')} on {m.get('permalink')} ({c['id']})"
            if DRY:
                print(f"DRY RUN would DM + hide: {tag}: {c.get('text')!r}")
                skipped += 1
                continue
            body = json.dumps({"comment_id": c["id"]})
            msg = json.dumps({"text": DM_TEXT})
            _, err = api("POST", f"{IG_ID}/messages", recipient=body, message=msg)
            already = err and "already" in (err.get("message", "").lower())
            if err and not already:
                print(f"! DM failed for {tag}: {err.get('message')} (code {err.get('code')}/{err.get('error_subcode')})")
                failed += 1
                continue
            _, herr = api("POST", c["id"], hide="true")
            if herr:
                print(f"! DM sent but hide failed for {tag}: {herr.get('message')}")
                failed += 1
            else:
                print(f"sent + hidden: {tag}")
                sent += 1
    print(f"done: {sent} sent, {skipped} dry-run matches, {failed} problems")


if __name__ == "__main__":
    main()
