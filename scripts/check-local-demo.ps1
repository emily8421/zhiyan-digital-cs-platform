<#
check-local-demo.ps1 - Check whether the local demo services are reachable.

Usage:
  powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1
  powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1 -BackendPort 8000 -H5Port 5173 -ConsolePort 5174

Notes:
  This script only sends local HTTP requests. It does not start services,
  install dependencies, or modify files.
#>
[CmdletBinding()]
param(
  [int]$BackendPort = 8000,
  [int]$H5Port = 5173,
  [int]$ConsolePort = 5174,
  [int]$TimeoutSeconds = 3
)

$ErrorActionPreference = "Stop"

function Test-HttpEndpoint {
  param(
    [string]$Name,
    [string]$Uri
  )

  try {
    $response = Invoke-WebRequest -UseBasicParsing -Uri $Uri -TimeoutSec $TimeoutSeconds
    if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 400) {
      Write-Host "[OK]   $Name -> $Uri ($($response.StatusCode))"
      return $true
    }

    Write-Warning "[FAIL] $Name -> $Uri returned HTTP $($response.StatusCode)"
    return $false
  }
  catch {
    Write-Warning "[FAIL] $Name -> $Uri ($($_.Exception.Message))"
    return $false
  }
}

$checks = @(
  [pscustomobject]@{ Name = "Backend health"; Uri = "http://127.0.0.1:$BackendPort/health" },
  [pscustomobject]@{ Name = "Backend docs"; Uri = "http://127.0.0.1:$BackendPort/docs" },
  [pscustomobject]@{ Name = "H5 customer page"; Uri = "http://127.0.0.1:$H5Port" },
  [pscustomobject]@{ Name = "Web console"; Uri = "http://127.0.0.1:$ConsolePort" }
)

Write-Host "==> Checking local demo services"
$passed = 0

foreach ($check in $checks) {
  if (Test-HttpEndpoint -Name $check.Name -Uri $check.Uri) {
    $passed += 1
  }
}

Write-Host ""
Write-Host "==> Result: $passed / $($checks.Count) reachable"

if ($passed -eq $checks.Count) {
  Write-Host "Local demo is ready:"
  Write-Host "- H5 customer: http://127.0.0.1:$H5Port"
  Write-Host "- Web console: http://127.0.0.1:$ConsolePort"
  Write-Host "- Backend docs: http://127.0.0.1:$BackendPort/docs"
  exit 0
}

Write-Warning "Some services are not reachable. Check the startup windows, wait a few seconds, then run this script again."
exit 1
