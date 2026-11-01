#!/bin/bash
# Orbit · opens your hub with chats inside. Run by "Start Orbit Hub" once hub chats are on.
# Lives in ~/.orbit. Usage: start.sh "<your Orbit Hub folder>"
HUB="${1:-$PWD}"; HUB="${HUB%/}"
ENG="$HOME/.orbit"; SITE="https://ashahmeetsworld.github.io/ashah-world/os"; URL="http://127.0.0.1:4777/"
UV="$HOME/.local/bin/uv"; [ -x "$UV" ] || UV="$(command -v uv)"
up() { curl -sf -m 2 "${URL}api/folder"; }
openfile() { [ -f "$HUB/Your hub.html" ] && open "$HUB/Your hub.html"; }
curl -sfL -m 8 -o "$ENG/hub-server.new" "$SITE/hub-server.py" && mv -f "$ENG/hub-server.new" "$ENG/hub-server.py"
rm -f "$ENG/hub-server.new"
if [ ! -f "$ENG/hub-server.py" ] || [ -z "$UV" ]; then openfile; exit 0; fi
NOW="$(up)"
if [ -n "$NOW" ] && [ "$NOW" != "$HUB" ]; then curl -sf -m 2 "${URL}api/quit" >/dev/null; sleep 2; NOW=""; fi
if [ -z "$NOW" ]; then
  (cd "$ENG" && nohup "$UV" run --no-project --quiet --python 3.12 hub-server.py "$HUB" >"$ENG/hub.log" 2>&1 &)
  for i in $(seq 40); do up >/dev/null && break; sleep 0.5; done
fi
if up >/dev/null; then open "$URL"; else openfile; fi
