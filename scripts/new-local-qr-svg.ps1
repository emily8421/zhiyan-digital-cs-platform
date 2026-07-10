<#
new-local-qr-svg.ps1 - Generate a local QR Code SVG without external dependencies.

Usage:
  powershell -ExecutionPolicy Bypass -File scripts/new-local-qr-svg.ps1 -Text "http://192.168.1.10:5173" -OutputPath .ai/local-demo-h5-qr.svg

Notes:
  This script generates a fixed QR Code Version 4-L in byte mode. It is intended
  for short local demo URLs and supports UTF-8 payloads up to 78 bytes.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$Text,

  [Parameter(Mandatory = $true)]
  [string]$OutputPath,

  [int]$Scale = 8,
  [int]$QuietZone = 4
)

$ErrorActionPreference = "Stop"

$Version = 4
$Size = 17 + 4 * $Version
$DataCodewordCount = 80
$ErrorCorrectionCodewordCount = 20
$MaskPattern = 0
$ErrorCorrectionLevelFormatBits = 1

function Initialize-GaloisField {
  $script:QrGfExp = New-Object int[] 512
  $script:QrGfLog = New-Object int[] 256
  $value = 1
  for ($index = 0; $index -lt 255; $index += 1) {
    $script:QrGfExp[$index] = $value
    $script:QrGfLog[$value] = $index
    $value = $value -shl 1
    if (($value -band 0x100) -ne 0) {
      $value = $value -bxor 0x11D
    }
  }
  for ($index = 255; $index -lt 512; $index += 1) {
    $script:QrGfExp[$index] = $script:QrGfExp[$index - 255]
  }
}

function Invoke-GfMultiply {
  param(
    [int]$Left,
    [int]$Right
  )

  if ($Left -eq 0 -or $Right -eq 0) {
    return 0
  }
  return $script:QrGfExp[$script:QrGfLog[$Left] + $script:QrGfLog[$Right]]
}

function New-RsGeneratorPolynomial {
  param([int]$Degree)

  [int[]]$generator = @(1)
  for ($degreeIndex = 0; $degreeIndex -lt $Degree; $degreeIndex += 1) {
    $coefficient = $script:QrGfExp[$degreeIndex]
    $next = New-Object int[] ($generator.Length + 1)
    for ($index = 0; $index -lt $generator.Length; $index += 1) {
      $next[$index] = $next[$index] -bxor (Invoke-GfMultiply $generator[$index] 1)
      $next[$index + 1] = $next[$index + 1] -bxor (Invoke-GfMultiply $generator[$index] $coefficient)
    }
    $generator = $next
  }
  return $generator
}

function New-RsRemainder {
  param(
    [int[]]$DataCodewords,
    [int]$Degree
  )

  $generator = New-RsGeneratorPolynomial -Degree $Degree
  $remainder = New-Object int[] $Degree

  foreach ($dataCodeword in $DataCodewords) {
    $factor = $dataCodeword -bxor $remainder[0]
    for ($index = 0; $index -lt ($Degree - 1); $index += 1) {
      $remainder[$index] = $remainder[$index + 1]
    }
    $remainder[$Degree - 1] = 0
    for ($index = 0; $index -lt $Degree; $index += 1) {
      $remainder[$index] = $remainder[$index] -bxor (Invoke-GfMultiply $generator[$index + 1] $factor)
    }
  }

  return $remainder
}

function Add-Bits {
  param(
    [System.Collections.Generic.List[int]]$Bits,
    [int]$Value,
    [int]$Length
  )

  for ($index = $Length - 1; $index -ge 0; $index -= 1) {
    $Bits.Add(($Value -shr $index) -band 1) | Out-Null
  }
}

function New-DataCodewords {
  param([byte[]]$Bytes)

  if ($Bytes.Count -gt 78) {
    throw "QR payload is too long for the local demo QR generator. Maximum: 78 UTF-8 bytes. Actual: $($Bytes.Count)."
  }

  $bits = New-Object 'System.Collections.Generic.List[int]'
  Add-Bits -Bits $bits -Value 0x4 -Length 4
  Add-Bits -Bits $bits -Value $Bytes.Count -Length 8
  foreach ($byteValue in $Bytes) {
    Add-Bits -Bits $bits -Value $byteValue -Length 8
  }

  $capacityBits = $DataCodewordCount * 8
  $terminatorLength = [Math]::Min(4, $capacityBits - $bits.Count)
  for ($index = 0; $index -lt $terminatorLength; $index += 1) {
    $bits.Add(0) | Out-Null
  }
  while (($bits.Count % 8) -ne 0) {
    $bits.Add(0) | Out-Null
  }

  $codewords = New-Object 'System.Collections.Generic.List[int]'
  for ($index = 0; $index -lt $bits.Count; $index += 8) {
    $codeword = 0
    for ($bitIndex = 0; $bitIndex -lt 8; $bitIndex += 1) {
      $codeword = ($codeword -shl 1) -bor $bits[$index + $bitIndex]
    }
    $codewords.Add($codeword) | Out-Null
  }

  $padCodewords = @(0xEC, 0x11)
  $padIndex = 0
  while ($codewords.Count -lt $DataCodewordCount) {
    $codewords.Add($padCodewords[$padIndex % 2]) | Out-Null
    $padIndex += 1
  }

  return [int[]]$codewords.ToArray()
}

function Get-FormatBits {
  param(
    [int]$ErrorCorrectionBits,
    [int]$Mask
  )

  $data = ($ErrorCorrectionBits -shl 3) -bor $Mask
  $remainder = $data
  for ($index = 0; $index -lt 10; $index += 1) {
    $remainder = ($remainder -shl 1) -bxor (((($remainder -shr 9) -band 1)) * 0x537)
  }
  return ((($data -shl 10) -bor ($remainder -band 0x3FF)) -bxor 0x5412)
}

function Get-BitBool {
  param(
    [int]$Value,
    [int]$Index
  )
  return (($Value -shr $Index) -band 1) -ne 0
}

$modules = New-Object 'bool[,]' $Size, $Size
$isFunction = New-Object 'bool[,]' $Size, $Size

function Set-QrModule {
  param(
    [int]$Row,
    [int]$Column,
    [bool]$Black,
    [bool]$FunctionModule = $true
  )

  if ($Row -lt 0 -or $Row -ge $Size -or $Column -lt 0 -or $Column -ge $Size) {
    return
  }
  $modules[$Row, $Column] = $Black
  if ($FunctionModule) {
    $isFunction[$Row, $Column] = $true
  }
}

function Add-FinderPattern {
  param(
    [int]$Top,
    [int]$Left
  )

  for ($rowOffset = -1; $rowOffset -le 7; $rowOffset += 1) {
    for ($columnOffset = -1; $columnOffset -le 7; $columnOffset += 1) {
      $row = $Top + $rowOffset
      $column = $Left + $columnOffset
      if ($row -lt 0 -or $row -ge $Size -or $column -lt 0 -or $column -ge $Size) {
        continue
      }
      $inPattern = $rowOffset -ge 0 -and $rowOffset -le 6 -and $columnOffset -ge 0 -and $columnOffset -le 6
      $black = $inPattern -and (
        $rowOffset -eq 0 -or $rowOffset -eq 6 -or
        $columnOffset -eq 0 -or $columnOffset -eq 6 -or
        ($rowOffset -ge 2 -and $rowOffset -le 4 -and $columnOffset -ge 2 -and $columnOffset -le 4)
      )
      Set-QrModule -Row $row -Column $column -Black $black -FunctionModule $true
    }
  }
}

function Add-AlignmentPattern {
  param(
    [int]$CenterRow,
    [int]$CenterColumn
  )

  for ($rowOffset = -2; $rowOffset -le 2; $rowOffset += 1) {
    for ($columnOffset = -2; $columnOffset -le 2; $columnOffset += 1) {
      $distance = [Math]::Max([Math]::Abs($rowOffset), [Math]::Abs($columnOffset))
      Set-QrModule -Row ($CenterRow + $rowOffset) -Column ($CenterColumn + $columnOffset) -Black ($distance -ne 1) -FunctionModule $true
    }
  }
}

function Add-FunctionPatterns {
  Add-FinderPattern -Top 0 -Left 0
  Add-FinderPattern -Top 0 -Left ($Size - 7)
  Add-FinderPattern -Top ($Size - 7) -Left 0

  for ($index = 8; $index -le ($Size - 9); $index += 1) {
    $black = ($index % 2) -eq 0
    Set-QrModule -Row 6 -Column $index -Black $black -FunctionModule $true
    Set-QrModule -Row $index -Column 6 -Black $black -FunctionModule $true
  }

  Add-AlignmentPattern -CenterRow 26 -CenterColumn 26

  $formatBits = Get-FormatBits -ErrorCorrectionBits $ErrorCorrectionLevelFormatBits -Mask $MaskPattern
  for ($index = 0; $index -le 5; $index += 1) {
    Set-QrModule -Row $index -Column 8 -Black (Get-BitBool -Value $formatBits -Index $index) -FunctionModule $true
  }
  Set-QrModule -Row 7 -Column 8 -Black (Get-BitBool -Value $formatBits -Index 6) -FunctionModule $true
  Set-QrModule -Row 8 -Column 8 -Black (Get-BitBool -Value $formatBits -Index 7) -FunctionModule $true
  Set-QrModule -Row 8 -Column 7 -Black (Get-BitBool -Value $formatBits -Index 8) -FunctionModule $true
  for ($index = 9; $index -lt 15; $index += 1) {
    Set-QrModule -Row 8 -Column (14 - $index) -Black (Get-BitBool -Value $formatBits -Index $index) -FunctionModule $true
  }

  for ($index = 0; $index -lt 8; $index += 1) {
    Set-QrModule -Row 8 -Column ($Size - 1 - $index) -Black (Get-BitBool -Value $formatBits -Index $index) -FunctionModule $true
  }
  for ($index = 8; $index -lt 15; $index += 1) {
    Set-QrModule -Row ($Size - 15 + $index) -Column 8 -Black (Get-BitBool -Value $formatBits -Index $index) -FunctionModule $true
  }
  Set-QrModule -Row ($Size - 8) -Column 8 -Black $true -FunctionModule $true
}

function Add-DataModules {
  param([int[]]$Codewords)

  $dataBits = New-Object 'System.Collections.Generic.List[int]'
  foreach ($codeword in $Codewords) {
    Add-Bits -Bits $dataBits -Value $codeword -Length 8
  }

  $bitIndex = 0
  $upward = $true
  for ($rightColumn = $Size - 1; $rightColumn -ge 1; $rightColumn -= 2) {
    if ($rightColumn -eq 6) {
      $rightColumn -= 1
    }

    for ($verticalIndex = 0; $verticalIndex -lt $Size; $verticalIndex += 1) {
      $row = if ($upward) { $Size - 1 - $verticalIndex } else { $verticalIndex }
      for ($columnOffset = 0; $columnOffset -lt 2; $columnOffset += 1) {
        $column = $rightColumn - $columnOffset
        if ($isFunction[$row, $column]) {
          continue
        }

        $bit = 0
        if ($bitIndex -lt $dataBits.Count) {
          $bit = $dataBits[$bitIndex]
          $bitIndex += 1
        }
        if ((($row + $column) % 2) -eq 0) {
          $bit = $bit -bxor 1
        }
        Set-QrModule -Row $row -Column $column -Black ($bit -eq 1) -FunctionModule $false
      }
    }
    $upward = -not $upward
  }
}

function Write-QrSvg {
  param([string]$Path)

  $pixelSize = ($Size + 2 * $QuietZone) * $Scale
  $rectangles = New-Object 'System.Collections.Generic.List[string]'
  for ($row = 0; $row -lt $Size; $row += 1) {
    for ($column = 0; $column -lt $Size; $column += 1) {
      if ($modules[$row, $column]) {
        $x = ($column + $QuietZone) * $Scale
        $y = ($row + $QuietZone) * $Scale
        $rectangles.Add("<rect x=`"$x`" y=`"$y`" width=`"$Scale`" height=`"$Scale`"/>") | Out-Null
      }
    }
  }

  $escapedText = [System.Security.SecurityElement]::Escape($Text)
  $svg = @(
    "<svg xmlns=`"http://www.w3.org/2000/svg`" width=`"$pixelSize`" height=`"$pixelSize`" viewBox=`"0 0 $pixelSize $pixelSize`" role=`"img`" aria-label=`"QR Code for $escapedText`">",
    "<rect width=`"100%`" height=`"100%`" fill=`"#fff`"/>",
    "<g fill=`"#000`">",
    ($rectangles -join "`n"),
    "</g>",
    "</svg>"
  ) -join "`n"

  $parent = Split-Path -Parent $Path
  if ($parent) {
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
  }
  Set-Content -Encoding UTF8 -Path $Path -Value $svg
}

Initialize-GaloisField
$bytes = [Text.Encoding]::UTF8.GetBytes($Text)
$dataCodewords = New-DataCodewords -Bytes $bytes
$errorCorrectionCodewords = New-RsRemainder -DataCodewords $dataCodewords -Degree $ErrorCorrectionCodewordCount
$allCodewords = @($dataCodewords) + @($errorCorrectionCodewords)

Add-FunctionPatterns
Add-DataModules -Codewords $allCodewords
Write-QrSvg -Path $OutputPath

Write-Host "QR SVG generated: $OutputPath"
