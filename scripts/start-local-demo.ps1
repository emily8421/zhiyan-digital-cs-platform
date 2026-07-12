<#
start-local-demo.ps1 - Start the local Phase1 demo services.

Usage:
  powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1
  powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1 -BackendPort 8000 -H5Port 5173 -ConsolePort 5174
  powershell -ExecutionPolicy Bypass -File scripts/start-local-demo.ps1 -LanHost 192.168.1.10

Notes:
  This script opens three PowerShell windows for the FastAPI backend, the H5
  customer page, and the Web console. It does not install dependencies or
  start Docker / PostgreSQL / external services. It fails fast when requested
  ports are already occupied, avoiding accidental checks against another local
  app.
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
  $process = Start-Process -FilePath "powershell.exe" -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy",
    "Bypass",
    "-EncodedCommand",
    $encodedCommand
  ) -PassThru
  Write-Host "- Started $Name in a new PowerShell window (pid=$($process.Id))"
  return $process
}

function Get-PortListenerDetails {
  param([int]$Port)

  $connections = @(Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue)
  $processIds = @($connections | Select-Object -ExpandProperty OwningProcess -Unique | Where-Object { $_ })
  foreach ($processId in $processIds) {
    $processName = "unknown"
    $commandLine = ""
    try {
      $processName = (Get-Process -Id $processId -ErrorAction Stop).ProcessName
    }
    catch {
      $processName = "unknown"
    }

    try {
      $commandLine = (Get-CimInstance Win32_Process -Filter "ProcessId = $processId" -ErrorAction Stop).CommandLine
    }
    catch {
      $commandLine = ""
    }

    [pscustomobject]@{
      Port = $Port
      ProcessId = $processId
      ProcessName = $processName
      CommandLine = $commandLine
    }
  }
}

function Test-PortOpen {
  param(
    [string]$HostName,
    [int]$Port,
    [int]$TimeoutMilliseconds = 1000
  )

  $client = [System.Net.Sockets.TcpClient]::new()
  try {
    $asyncResult = $client.BeginConnect($HostName, $Port, $null, $null)
    if (-not $asyncResult.AsyncWaitHandle.WaitOne($TimeoutMilliseconds, $false)) {
      return $false
    }
    $client.EndConnect($asyncResult)
    return $true
  }
  catch {
    return $false
  }
  finally {
    $client.Close()
  }
}

function Assert-PortAvailable {
  param(
    [string]$Name,
    [int]$Port
  )

  $isOpen = Test-PortOpen -HostName "127.0.0.1" -Port $Port
  if (-not $isOpen) {
    return
  }

  $listeners = @(Get-PortListenerDetails -Port $Port)

  Write-Warning "$Name port $Port is already in use. Stop the existing process or pass a different port."
  if ($listeners.Count -gt 0) {
    foreach ($listener in $listeners) {
      Write-Warning ("  - pid={0} process={1} command={2}" -f $listener.ProcessId, $listener.ProcessName, $listener.CommandLine)
    }
  }
  else {
    Write-Warning "  - TCP connection to 127.0.0.1:$Port succeeded, but process details could not be resolved on this machine."
  }
  throw "$Name port $Port is already in use."
}

function Write-RuntimeState {
  param(
    [string]$RepoRoot,
    [int]$BackendPort,
    [int]$H5Port,
    [int]$ConsolePort,
    [string]$H5LanUrl,
    [string]$QrPath,
    [int]$BackendPid,
    [int]$H5Pid,
    [int]$ConsolePid
  )

  $aiDir = Join-Path $RepoRoot ".ai"
  if (-not (Test-Path -LiteralPath $aiDir)) {
    New-Item -ItemType Directory -Path $aiDir | Out-Null
  }

  $runtimePath = Join-Path $aiDir "local-demo-runtime.json"
  $state = [ordered]@{
    started_at = (Get-Date).ToString("yyyy-MM-ddTHH:mm:sszzz")
    backend = [ordered]@{ port = $BackendPort; url = "http://127.0.0.1:$BackendPort"; pid = $BackendPid }
    customer_h5 = [ordered]@{ port = $H5Port; url = "http://127.0.0.1:$H5Port"; lan_url = $H5LanUrl; identity_marker = 'name="zycs-demo-app" content="customer-h5"'; pid = $H5Pid }
    console = [ordered]@{ port = $ConsolePort; url = "http://127.0.0.1:$ConsolePort"; identity_marker = 'name="zycs-demo-app" content="console"'; pid = $ConsolePid }
    qr_svg = $QrPath
  }

  $state | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $runtimePath -Encoding UTF8
  return $runtimePath
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

if (@(@($BackendPort, $H5Port, $ConsolePort) | Select-Object -Unique).Count -ne 3) {
  throw "BackendPort, H5Port, and ConsolePort must be different."
}

Assert-PortAvailable -Name "Backend API" -Port $BackendPort
Assert-PortAvailable -Name "H5 customer page" -Port $H5Port
Assert-PortAvailable -Name "Web console" -Port $ConsolePort

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

$backendProcess = Start-DemoWindow `
  -Name "Backend API (:${BackendPort})" `
  -WorkingDirectory $repoRoot `
  -Command "`$env:PYTHONPATH='backend'; python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port $BackendPort"

$h5Process = Start-DemoWindow `
  -Name "H5 customer page (:${H5Port})" `
  -WorkingDirectory $h5Dir `
  -Command "npm.cmd run dev -- --host 0.0.0.0 --port $H5Port --strictPort"

$consoleProcess = Start-DemoWindow `
  -Name "Web console (:${ConsolePort})" `
  -WorkingDirectory $consoleDir `
  -Command "npm.cmd run dev -- --port $ConsolePort --strictPort"

$runtimePath = Write-RuntimeState `
  -RepoRoot $repoRoot `
  -BackendPort $BackendPort `
  -H5Port $H5Port `
  -ConsolePort $ConsolePort `
  -H5LanUrl $h5LanUrl `
  -QrPath $qrPath `
  -BackendPid $backendProcess.Id `
  -H5Pid $h5Process.Id `
  -ConsolePid $consoleProcess.Id

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
Write-Host "- Runtime state:  $runtimePath"
Write-Host ""
Write-Host "After the windows finish starting, run:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1 -BackendPort $BackendPort -H5Port $H5Port -ConsolePort $ConsolePort"
