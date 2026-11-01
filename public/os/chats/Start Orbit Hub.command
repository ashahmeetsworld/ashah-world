#!/bin/bash
cd "$(dirname "$(readlink "$0" || echo "$0")")"
curl -sfL -m 8 -o "Your hub.new" "https://ashahmeetsworld.github.io/ashah-world/os/hub.html" && mv -f "Your hub.new" "Your hub.html"
rm -f "Your hub.new"
[ ! -f "Your hub.html" ] && [ -f "../04 Hub demo.html" ] && cp "../04 Hub demo.html" "Your hub.html"
if [ ! -f "Your hub.html" ]; then
  echo "Couldn't get your hub page. Check you're online and try again, or put this folder next to 04 Hub demo.html."
  read -n 1; exit 1
fi
if [ ! -f .shortcut ]; then
  ln -sf "$PWD/Start Orbit Hub.command" "$HOME/Desktop/Orbit Hub.command"; touch .shortcut
fi
if [ -x "$HOME/.orbit/start.sh" ]; then
  "$HOME/.orbit/start.sh" "$PWD"
else
  open "Your hub.html"
fi
echo "Your hub is open. You can close this window."
