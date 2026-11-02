#!/bin/bash
# Orbit · Phase 2: chats inside your hub. Run by double-clicking "Bring your hub to life" in your Orbit Hub folder.
# Installs Claude Code and a tiny helper (uv), signs Claude Code in to YOUR Claude plan (no API key, no extra cost),
# connects Notion, and switches your hub over. Safe to run again any time: it only does what's missing.
SITE="https://ashahmeetsworld.github.io/ashah-world/os"
HUB="${ORBIT_HUB:-$PWD}"
ENG="$HOME/.orbit"; CHATS="$ENG/chats"; BIN="$HOME/.local/bin"
mkdir -p "$CHATS/out"
export PATH="$BIN:$PATH"
unset ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN   # always your plan, never paid API
say() { printf "\n  \033[36m%s\033[0m\n" "$1"; }
note() { printf "  %s\n" "$1"; }
stop_here() { printf "\n  \033[33m%s\033[0m\n  Run Bring your hub to life again when you're ready. Nothing is broken: your hub works as before.\n" "$1"; read -n 1 -s -r -p "  Press any key to close." </dev/tty; exit 1; }
find_claude() { command -v claude || { [ -x "$BIN/claude" ] && echo "$BIN/claude"; }; }
find_uv() { command -v uv || { [ -x "$BIN/uv" ] && echo "$BIN/uv"; }; }

printf "\n  Orbit · chats inside your hub\n"
note "About 5 minutes. Your only jobs: two clicks in your browser. Leave this window open."

say "1 of 5 · Getting Claude Code..."
CLAUDE="$(find_claude)"
[ -z "$CLAUDE" ] && { curl -fsSL https://claude.ai/install.sh | bash >/dev/null 2>&1; CLAUDE="$(find_claude)"; }
[ -z "$CLAUDE" ] && stop_here "Claude Code didn't install. Check you're online, then try again."
note "Done."

say "2 of 5 · Getting the hub's engine..."
UV="$(find_uv)"
[ -z "$UV" ] && { curl -LsSf https://astral.sh/uv/install.sh | env UV_NO_MODIFY_PATH=1 sh >/dev/null 2>&1; UV="$(find_uv)"; }
[ -z "$UV" ] && stop_here "The engine didn't install. Check you're online, then try again."
curl -fsSL -o "$ENG/hub-server.py" "$SITE/hub-server.py" && curl -fsSL -o "$ENG/start.sh" "$SITE/chats/start.sh" || stop_here "Couldn't download the engine. Check you're online, then try again."
chmod +x "$ENG/start.sh"
"$UV" run --no-project --quiet --python 3.12 python -c "print('ok')" >/dev/null 2>&1
note "Done."

say "3 of 5 · Signing in to Claude..."
cd "$CHATS"
signed() { "$CLAUDE" auth status 2>/dev/null | grep -q '"authMethod"[[:space:]]*:[[:space:]]*"claude.ai"'; }
if ! signed; then
  note "Your browser is opening. Sign in if it asks, then click Authorize. Come back here after."
  "$CLAUDE" auth login </dev/tty
  signed || stop_here "Claude isn't signed in yet. It needs a paid Claude plan (Pro or Max)."
fi
note "Signed in to your Claude plan."

say "4 of 5 · Connecting Notion..."
"$CLAUDE" mcp add --transport http notion https://mcp.notion.com/mcp >/dev/null 2>&1
if ! "$CLAUDE" mcp get notion 2>/dev/null | grep -q "Connected"; then
  note "Your browser is opening again. Pick your Notion workspace and click Allow access. Come back here after."
  "$CLAUDE" mcp login notion </dev/tty
fi
note "Done."

say "5 of 5 · Checking it all works..."
"$CLAUDE" -p "Reply with the single word: ready" --output-format json 2>/dev/null | grep -q '"is_error"[[:space:]]*:[[:space:]]*false' \
  || stop_here "Claude didn't answer the test. If you've hit your plan's limit, wait for it to reset."
curl -fsSL -o "$HUB/Start Orbit Hub.command" "$SITE/chats/Start%20Orbit%20Hub.command" && chmod +x "$HUB/Start Orbit Hub.command"
echo on > "$ENG/chats-on"
note "All set."

printf "\n  \033[32mYour hub now has chats inside. Opening it...\033[0m\n"
note "From now on, just double-click Start Orbit Hub as usual. Set and forget."
"$ENG/start.sh" "$HUB"
read -n 1 -s -r -p "  You can close this window." </dev/tty
