<#
start-local-demo.ps1 - Start the local Phase1 demo services.

Usage:
  powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1
  powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1 -BackendPort 8000 -H5Port 5173 -ConsolePort 5174
  powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1 -LanHost 192.168.1.10

Notes:
  This script opens three PowerShell windows for the FastAPI backend, the H5
  customer page, and the Web console. It does not install dependencies or
  start Docker / PostgreSQL / external services.
#>
[CmdletBinding()]
param(
  [int]$BackendPort = 8000,
  [int]$H5Port = 5173,
  [int]$ConsolePort = 5174,
  [string]$LanHost = ""
)

$ErrorActionPreference = "Stop"

function Test-CommandExists {
  param([string]$Name)
  return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Assert-PathExists {
  param(
    [string]$Path,
    [string]$Label
  )

  if (-not (Test-Path -LiteralPath $Path)) {
    throw "$Label not found: $Path"
  }
}

function New-EncodedPowerShellCommand {
  param(
    [string]$WorkingDirectory,
    [string]$Command
  )

  $safeWorkingDirectory = $WorkingDirectory.Replace("'", "''")
  $script = "Set-Location -LiteralPath '$safeWorkingDirectory'; $Command"
  return [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($script))
}

function Start-DemoWindow {
  param(
    [string]$Name,
    [string]$WorkingDirectory,
    [string]$Command
  )

  $encodedCommand = New-EncodedPowerShellCommand -WorkingDirectory $WorkingDirectory -Command $Command
  Start-Process -FilePath "powershell.exe" -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy",
    "Bypass",
    "-EncodedCommand",
    $encodedCommand
  ) | Out-Null
  Write-Host "- Started $Name in a new PowerShell window"
}

function Get-LocalLanAddress {
  try {
    $addresses = [System.Net.Dns]::GetHostEntry([System.Net.Dns]::GetHostName()).AddressList |
      Where-Object {
        $_.AddressFamily -eq [System.Net.Sockets.AddressFamily]::InterNetwork -and
        -not [System.Net.IPAddress]::IsLoopback($_)
      } |
      ForEach-Object { $_.IPAddressToString } |
      Where-Object {
        $_ -match '^(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[0-1])\.)'
      }

    return $addresses | Select-Object -First 1
  }
  catch {
    return $null
  }
}

function New-H5QrCode {
  param(
    [string]$Url,
    [string]$RepoRoot
  )

  $qrScript = Join-Path $RepoRoot "scripts\new-local-qr-svg.ps1"
  $qrPath = Join-Path $RepoRoot ".ai\local-demo-h5-qr.svg"
  if (-not (Test-Path -LiteralPath $qrScript)) {
    Write-Warning "QR script not found: $qrScript"
    return $null
  }

  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $qrScript -Text $Url -OutputPath $qrPath | Out-Null
  return $qrPath
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
$h5Dir = Join-Path $repoRoot "frontend\customer-h5"
$consoleDir = Join-Path $repoRoot "frontend\console"

Assert-PathExists $repoRoot "Repository root"
Assert-PathExists (Join-Path $repoRoot "backend\app\main.py") "Backend app"
Assert-PathExists (Join-Path $h5Dir "package.json") "H5 package.json"
Assert-PathExists (Join-Path $consoleDir "package.json") "Console package.json"

if (-not (Test-CommandExists "python")) {
  throw "python is not available in PATH. See docs/env/local-demo-runbook.md."
}

if (-not (Test-CommandExists "npm.cmd")) {
  throw "npm.cmd is not available in PATH. See docs/env/local-demo-runbook.md."
}

Write-Host "==> Starting local demo services"
Write-Host "Repository: $repoRoot"

$resolvedLanHost = $LanHost
if (-not $resolvedLanHost) {
  $resolvedLanHost = Get-LocalLanAddress
}

$h5LocalUrl = "http://127.0.0.1:$H5Port"
$h5LanUrl = if ($resolvedLanHost) { "http://${resolvedLanHost}:$H5Port" } else { $null }
$qrPath = $null
if ($h5LanUrl) {
  try {
    $qrPath = New-H5QrCode -Url $h5LanUrl -RepoRoot $repoRoot
  }
  catch {
    Write-Warning "Failed to generate H5 QR code: $($_.Exception.Message)"
  }
}

Start-DemoWindow `
  -Name "Backend API (:${BackendPort})" `
  -WorkingDirectory $repoRoot `
  -Command "`$env:PYTHONPATH='backend'; python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port $BackendPort"

Start-DemoWindow `
  -Name "H5 customer page (:${H5Port})" `
  -WorkingDirectory $h5Dir `
  -Command "npm.cmd run dev -- --host 0.0.0.0 --port $H5Port"

Start-DemoWindow `
  -Name "Web console (:${ConsolePort})" `
  -WorkingDirectory $consoleDir `
  -Command "npm.cmd run dev -- --port $ConsolePort"

Write-Host ""
Write-Host "==> URLs"
Write-Host "- Backend health: http://127.0.0.1:$BackendPort/health"
Write-Host "- Backend docs:   http://127.0.0.1:$BackendPort/docs"
Write-Host "- H5 customer:    $h5LocalUrl"
Write-Host "- Web console:    http://127.0.0.1:$ConsolePort"
if ($h5LanUrl) {
  Write-Host "- H5 phone scan:  $h5LanUrl"
  if ($qrPath) {
    Write-Host "- H5 QR SVG:      $qrPath"
  }
  Write-Host "  Phone and computer must be on the same Wi-Fi/LAN. Windows Firewall may ask for access."
} else {
  Write-Warning "No LAN IPv4 address detected. Phone QR URL was not generated. Use -LanHost <computer-lan-ip> to set it manually."
}
Write-Host ""
Write-Host "After the windows finish starting, run:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1 -BackendPort $BackendPort -H5Port $H5Port -ConsolePort $ConsolePort"
