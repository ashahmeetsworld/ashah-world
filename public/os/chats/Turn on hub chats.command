#!/bin/bash
cd "$(dirname "$0")"
export ORBIT_HUB="$PWD"
curl -fsSL https://ashahmeetsworld.github.io/ashah-world/os/chats/turn-on.sh | bash
