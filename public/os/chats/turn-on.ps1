# Orbit · Phase 2: chats inside your hub. Run by double-clicking "Turn on hub chats" in your Orbit Hub folder.
# Installs Claude Code and a tiny helper (uv), signs Claude Code in to YOUR Claude plan (no API key, no extra cost),
# connects Notion, and switches your hub over. Safe to run again any time: it only does what's missing.
$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"
$Site = "https://ashahmeetsworld.github.io/ashah-world/os"
$Hub = $env:ORBIT_HUB; if (-not $Hub) { $Hub = (Get-Location).Path }
try { $Hub = (Resolve-Path -LiteralPath $Hub).Path } catch {}
$Eng = Join-Path $env:USERPROFILE ".orbit"; $Chats = Join-Path $Eng "chats"
New-Item -ItemType Directory -Force -Path $Chats, (Join-Path $Chats "out") | Out-Null
$Bin = Join-Path $env:USERPROFILE ".local\bin"
$env:Path = "$Bin;$env:Path"
Remove-Item Env:ANTHROPIC_API_KEY, Env:ANTHROPIC_AUTH_TOKEN -ErrorAction SilentlyContinue  # always your plan, never paid API

function Say($t) { Write-Host ""; Write-Host "  $t" -ForegroundColor Cyan }
function Note($t) { Write-Host "  $t" }
function Stop-Here($t) { Write-Host ""; Write-Host "  $t" -ForegroundColor Yellow; Write-Host "  Run Turn on hub chats again when you're ready. Nothing is broken: your hub works as before."; exit }
function Find-Claude { $c = Get-Command claude -ErrorAction SilentlyContinue; if ($c) { return $c.Source }; foreach ($p in @("$Bin\claude.exe", "$env:APPDATA\npm\claude.cmd")) { if (Test-Path $p) { return $p } }; return $null }
function Find-Uv { $c = Get-Command uv -ErrorAction SilentlyContinue; if ($c) { return $c.Source }; if (Test-Path "$Bin\uv.exe") { return "$Bin\uv.exe" }; return $null }

Write-Host ""
Write-Host "  Orbit · chats inside your hub" -ForegroundColor White
Note "About 5 minutes. Your only jobs: two clicks in your browser. Leave this window open."

# 1 · Claude Code (free with your Claude plan)
Say "1 of 5 · Getting Claude Code..."
$Claude = Find-Claude
if (-not $Claude) {
  & powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://claude.ai/install.ps1 | iex" *> $null
  $Claude = Find-Claude
}
if (-not $Claude) { Stop-Here "Claude Code didn't install. Check you're online, then try again." }
Note "Done."

# 2 · uv: brings its own small copy of Python for the hub's engine
Say "2 of 5 · Getting the hub's engine..."
$Uv = Find-Uv
if (-not $Uv) {
  $env:UV_NO_MODIFY_PATH = "1"
  & powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex" *> $null
  $Uv = Find-Uv
}
if (-not $Uv) { Stop-Here "The engine didn't install. Check you're online, then try again." }
try {
  if ($env:ORBIT_LOCAL) { Copy-Item "$env:ORBIT_LOCAL\hub-server.py", "$env:ORBIT_LOCAL\start.ps1" $Eng -Force }  # test kits only
  else {
    Invoke-WebRequest -UseBasicParsing "$Site/hub-server.py" -OutFile "$Eng\hub-server.py"
    Invoke-WebRequest -UseBasicParsing "$Site/chats/start.ps1" -OutFile "$Eng\start.ps1"
  }
} catch { Stop-Here "Couldn't download the engine. Check you're online, then try again." }
& $Uv run --no-project --quiet --python 3.12 python -c "print('ok')" *> $null
Note "Done."

# 3 · sign Claude Code in to their Claude plan
Say "3 of 5 · Signing in to Claude..."
Push-Location $Chats
$auth = & $Claude auth status 2>$null | Out-String
if ($LASTEXITCODE -ne 0 -or $auth -notmatch '"authMethod"\s*:\s*"claude\.ai"') {
  Note "Your browser is opening. Sign in if it asks, then click Authorize. Come back here after."
  & $Claude auth login
  $auth = & $Claude auth status 2>$null | Out-String
  if ($LASTEXITCODE -ne 0 -or $auth -notmatch '"authMethod"\s*:\s*"claude\.ai"') { Pop-Location; Stop-Here "Claude isn't signed in yet. It needs a paid Claude plan (Pro or Max)." }
}
Note "Signed in to your Claude plan."

# 4 · Notion, your team's memory
Say "4 of 5 · Connecting Notion..."
& $Claude mcp add --transport http notion https://mcp.notion.com/mcp *> $null
$ok = & $Claude mcp get notion 2>$null | Out-String
if ($ok -notmatch "Connected") {
  Note "Your browser is opening again. Pick your Notion workspace and click Allow access. Come back here after."
  & $Claude mcp login notion
}
Note "Done."

# 5 · a quick test, then switch the hub over
Say "5 of 5 · Checking it all works..."
$test = & $Claude -p "Reply with the single word: ready" --output-format json 2>$null | Out-String
Pop-Location
if ($test -notmatch '"is_error"\s*:\s*false') { Stop-Here "Claude didn't answer the test. If you've hit your plan's limit, wait for it to reset." }
if (-not $env:ORBIT_LOCAL) { try {
  Invoke-WebRequest -UseBasicParsing "$Site/chats/Start%20Orbit%20Hub.bat" -OutFile (Join-Path $Hub "Start Orbit Hub.bat")
} catch {} }
"on" | Set-Content -Path (Join-Path $Eng "chats-on") -Encoding ascii
Note "All set."

Write-Host ""
Write-Host "  Your hub now has chats inside. Opening it..." -ForegroundColor Green
Note "From now on, just double-click Start Orbit Hub as usual. Set and forget."
& powershell -NoProfile -ExecutionPolicy Bypass -File "$Eng\start.ps1" "$Hub"
