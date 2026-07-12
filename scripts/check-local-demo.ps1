<#
check-local-demo.ps1 - Check whether the local demo services are reachable.

Usage:
  powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1
  powershell -ExecutionPolicy Bypass -File scripts/check-local-demo.ps1 -BackendPort 8000 -H5Port 5173 -ConsolePort 5174

Notes:
  This script only sends local HTTP requests. It does not start services,
  install dependencies, or modify files. Frontend checks also validate app
  identity markers so another local app on the same port is not mistaken for
  this demo.
#>
[CmdletBinding()]
param(
  [int]$BackendPort = 8000,
  [int]$H5Port = 5173,
  [int]$ConsolePort = 5174,
  [int]$TimeoutSeconds = 3,
  [string]$BackendHealthMarker = '"status":"ok"',
  [string]$H5IdentityMarker = 'name="zycs-demo-app" content="customer-h5"',
  [string]$ConsoleIdentityMarker = 'name="zycs-demo-app" content="console"'
)

$ErrorActionPreference = "Stop"

function Test-HttpEndpoint {
  param(
    [string]$Name,
    [string]$Uri,
    [string]$ExpectedContent = ""
  )

  try {
    $response = Invoke-WebRequest -UseBasicParsing -Uri $Uri -TimeoutSec $TimeoutSeconds
    if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 400) {
      if ($ExpectedContent -and -not ([string]$response.Content).Contains($ExpectedContent)) {
        Write-Warning "[FAIL] $Name -> $Uri returned HTTP $($response.StatusCode), but identity marker was not found: $ExpectedContent"
        Write-Warning "       Another local app may be using this port. Stop it or pass explicit ports."
        return $false
      }

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
  [pscustomobject]@{ Name = "Backend health"; Uri = "http://127.0.0.1:$BackendPort/health"; ExpectedContent = $BackendHealthMarker },
  [pscustomobject]@{ Name = "Backend docs"; Uri = "http://127.0.0.1:$BackendPort/docs"; ExpectedContent = "" },
  [pscustomobject]@{ Name = "H5 customer page"; Uri = "http://127.0.0.1:$H5Port"; ExpectedContent = $H5IdentityMarker },
  [pscustomobject]@{ Name = "Web console"; Uri = "http://127.0.0.1:$ConsolePort"; ExpectedContent = $ConsoleIdentityMarker }
)

Write-Host "==> Checking local demo services"
$passed = 0

foreach ($check in $checks) {
  if (Test-HttpEndpoint -Name $check.Name -Uri $check.Uri -ExpectedContent $check.ExpectedContent) {
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
