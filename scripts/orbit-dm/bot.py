"""Orbit comment bot for @ashah.world.

A post says 'Comment "ORBIT"' (in its caption or in my own comment). Someone
comments ORBIT (any case, quotes, or a small typo). The bot sends them that
keyword's message by private DM, then hides their comment so the comment section
stays about the post. Keywords and their messages live in keywords.json; a new
campaign is one new entry there, nothing else.

Runs every few minutes on GitHub Actions (see .github/workflows/orbit-dm.yml).
No state file: a hidden comment counts as done, and Meta allows only one private
reply per comment, so a retry can never DM someone twice.

Env: IG_ACCESS_TOKEN (required), IG_USER_ID, DRY_RUN=1 to only report.
Python standard library only.
"""
import json, os, re, sys, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

def clean_token(raw):
    """Forgive paste slips: a copied 'IG_ACCESS_TOKEN=' prefix, quotes, spaces, line breaks."""
    t = re.sub(r"\s+", "", raw or "")
    if "=" in t and t.split("=", 1)[0].upper().endswith("TOKEN"):
        t = t.split("=", 1)[1]
    return t.strip("\"'`")


TOKEN = clean_token(os.environ.get("IG_ACCESS_TOKEN", ""))
# Instagram-login tokens (start "IG") use graph.instagram.com; Facebook-login tokens use graph.facebook.com
GRAPH = "https://graph.instagram.com/v21.0" if TOKEN.startswith("IG") else "https://graph.facebook.com/v21.0"
IG_ID = os.environ.get("IG_USER_ID", "").strip() or "17841443383606084"
DRY = os.environ.get("DRY_RUN", "") not in ("", "0", "false")
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "keywords.json"), encoding="utf-8") as f:
    KEYWORDS = [k for k in json.load(f)["keywords"] if k.get("keyword") and k.get("message")]
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


def matches(text, keyword):
    """True for ORBIT, "orbit"!, Orbit pls, orbt, orbitt, O R B I T, 'orbit 🙏'.
    Multi-word keywords ("booty cheeks") match as a phrase, spaces optional."""
    if not text:
        return False
    key = re.sub(r"[^a-z0-9]", "", keyword.lower())
    letters = re.sub(r"[^a-z0-9]", "", text.lower())
    if not key or not letters:
        return False
    slack = 1 if len(key) >= 4 else 0
    if len(key) >= 10:
        slack = 2
    if edit_distance(letters, key) <= slack:
        return True  # the whole comment is (nearly) the keyword
    if key in letters and " " in keyword.strip():
        return True  # phrase inside a longer comment
    words = re.findall(r"[a-z0-9]+", text.lower())
    n = len(keyword.split())
    for i in range(len(words) - n + 1):
        chunk = "".join(words[i:i + n])
        if abs(len(chunk) - len(key)) <= slack and edit_distance(chunk, key) <= slack:
            return True
    return False


def keyword_for(text, active=None):
    for k in (KEYWORDS if active is None else active):
        if matches(text, k["keyword"]):
            return k
    return None


def norm(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())


def active_keywords(caption, own_texts):
    """A keyword only works on posts that ask for it: in the caption or in my own comment."""
    pool = norm(caption) + " " + " ".join(norm(t) for t in own_texts)
    return [k for k in KEYWORDS if norm(k["keyword"]) in pool]


def wants_orbit(text):  # kept for older checks
    return keyword_for(text) is not None


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
    global IG_ID
    if TOKEN.startswith("IG"):
        me, err = api("GET", "me", fields="user_id,username")
        if err:
            sys.exit(f"Could not read the account: {err.get('message')}")
        IG_ID = str(me.get("user_id") or me.get("id"))
        print(f"account: @{me.get('username')}")
    media, err = api("GET", f"{IG_ID}/media", fields="id,timestamp,permalink,caption", limit=25)
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
        own = [c.get("text", "") for c in flat if (c.get("from") or {}).get("id") == IG_ID]
        active = active_keywords(m.get("caption"), own)
        if not active:
            continue  # this post doesn't ask people to comment a keyword
        for c in flat:
            who = (c.get("from") or {})
            if who.get("id") == IG_ID or c.get("hidden"):
                continue
            hit = keyword_for(c.get("text", ""), active)
            if not hit:
                continue
            if parse_time(c["timestamp"]) < cutoff:
                continue  # too old for a private reply
            tag = f"@{who.get('username', '?')} on {m.get('permalink')} ({c['id']})"
            if DRY:
                print(f"DRY RUN would DM ({hit['keyword']}) + hide: {tag}: {c.get('text')!r}")
                skipped += 1
                continue
            body = json.dumps({"comment_id": c["id"]})
            msg = json.dumps({"text": hit["message"]})
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
