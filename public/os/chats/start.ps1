# Orbit · opens your hub with chats inside. Run by "Start Orbit Hub" once hub chats are on.
# Lives in %USERPROFILE%\.orbit. Usage: start.ps1 "<your Orbit Hub folder>"
param([string]$Hub = (Get-Location).Path)
$ErrorActionPreference = "SilentlyContinue"
try { $Hub = (Resolve-Path -LiteralPath $Hub).Path } catch {}
$Eng = Join-Path $env:USERPROFILE ".orbit"
$Site = "https://ashahmeetsworld.github.io/ashah-world/os"
$Url = "http://127.0.0.1:4777/"
$Uv = Join-Path $env:USERPROFILE ".local\bin\uv.exe"
if (-not (Test-Path $Uv)) { $c = Get-Command uv -ErrorAction SilentlyContinue; if ($c) { $Uv = $c.Source } }
function Up { try { (Invoke-WebRequest -UseBasicParsing ($Url + "api/folder") -TimeoutSec 2).Content } catch { $null } }
function OpenFile { $p = Join-Path $Hub "Your hub.html"; if (Test-Path $p) { Start-Process $p } }

# keep the engine fresh (quietly; offline it uses the copy it has)
try { Invoke-WebRequest -UseBasicParsing "$Site/hub-server.py" -OutFile "$Eng\hub-server.new" -TimeoutSec 8; Move-Item -Force "$Eng\hub-server.new" "$Eng\hub-server.py" } catch {}
if (-not (Test-Path "$Eng\hub-server.py") -or -not (Test-Path $Uv)) { OpenFile; exit }

$now = Up
if ($now -and ($now.Trim() -ne $Hub)) { try { Invoke-WebRequest -UseBasicParsing ($Url + "api/quit") -TimeoutSec 2 | Out-Null } catch {}; Start-Sleep 2; $now = $null }
if (-not $now) {
  Start-Process -WindowStyle Hidden -FilePath $Uv -WorkingDirectory $Eng -ArgumentList @("run", "--no-project", "--quiet", "--python", "3.12", "hub-server.py", "`"$Hub`"")
  for ($i = 0; $i -lt 40 -and -not (Up); $i++) { Start-Sleep -Milliseconds 500 }
}
if (Up) { Start-Process $Url } else { OpenFile }
