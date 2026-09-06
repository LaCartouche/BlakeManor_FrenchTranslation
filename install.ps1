#Requires -Version 5.0
<#
Blake Manor FR - installer for Windows.

  Double-click install.bat, or from PowerShell:
    powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1

  Options:
    -GamePath "C:\...\The Seance of Blake Manor"   when Steam does not know where the game is
    -Uninstall                                       remove the patch and BepInEx (saves are never touched)

The patch comes from next to this script when it sits in the release zip;
otherwise the latest release is fetched from GitHub. No Steam launch option is
needed on Windows: BepInEx loads through winhttp.dll.
#>
param(
    [string]$GamePath = "",
    [switch]$Uninstall
)
$ErrorActionPreference = "Stop"

$AppDir      = "The Seance of Blake Manor"
$Exe         = "The Seance of Blake Manor.exe"
$BepVersion  = "5.4.23.5"
$BepZip      = "BepInEx_win_x64_$BepVersion.zip"
$BepUrl      = "https://github.com/BepInEx/BepInEx/releases/download/v$BepVersion/$BepZip"
$BepSha256   = "82f9878551030f54657792c0740d9d51a09500eeae1fba21106b0c441e6732c4"
$ReleasesApi = "https://api.github.com/repos/LaCartouche/BlakeManor_FrenchTranslation/releases/latest"
$Here        = Split-Path -Parent $MyInvocation.MyCommand.Path

function Find-Game {
    if ($GamePath -ne "") {
        if (Test-Path (Join-Path $GamePath $Exe)) { return (Resolve-Path $GamePath).Path }
        throw "No '$Exe' in: $GamePath"
    }
    # Steam's own location from the registry, then every library it lists.
    $roots = @()
    foreach ($key in "HKCU:\Software\Valve\Steam", "HKLM:\SOFTWARE\WOW6432Node\Valve\Steam", "HKLM:\SOFTWARE\Valve\Steam") {
        try {
            $item = Get-ItemProperty -Path $key -ErrorAction Stop
            foreach ($name in "SteamPath", "InstallPath") {
                $v = $item.$name
                if ($v) { $roots += $v }
            }
        } catch { }
    }
    $roots += "C:\Program Files (x86)\Steam"
    $libs = @()
    foreach ($root in $roots) {
        if (-not (Test-Path $root)) { continue }
        $libs += $root
        $vdf = Join-Path $root "steamapps\libraryfolders.vdf"
        if (Test-Path $vdf) {
            $text = Get-Content -Path $vdf -Raw
            foreach ($m in [regex]::Matches($text, '"path"\s+"([^"]+)"')) {
                $libs += $m.Groups[1].Value.Replace('\\', '\')
            }
        }
    }
    foreach ($lib in ($libs | Select-Object -Unique)) {
        $game = Join-Path $lib "steamapps\common\$AppDir"
        if (Test-Path (Join-Path $game $Exe)) { return $game }
    }
    throw "Could not find '$AppDir' in any Steam library. Run again with -GamePath 'C:\...\$AppDir'."
}

function Get-File([string]$Url, [string]$Path) {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $Url -OutFile $Path -UseBasicParsing
}

$Game = Find-Game
Write-Host "Game folder: $Game"

if ($Uninstall) {
    foreach ($rel in "BepInEx", "winhttp.dll", "doorstop_config.ini", ".doorstop_version", "changelog.txt") {
        $p = Join-Path $Game $rel
        if (Test-Path $p) { Remove-Item -Path $p -Recurse -Force }
    }
    Write-Host "Removed the patch and BepInEx. Saves were not touched."
    exit 0
}

$Temp = Join-Path $env:TEMP ("blakemanor-fr-" + [guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $Temp | Out-Null
try {
    # 1. BepInEx, checked against its published checksum before anything is unpacked
    $zip = Join-Path $Temp $BepZip
    Write-Host "Downloading BepInEx $BepVersion ..."
    Get-File $BepUrl $zip
    $hash = (Get-FileHash -Path $zip -Algorithm SHA256).Hash.ToLower()
    if ($hash -ne $BepSha256) { throw "$BepZip does not match its published checksum; not installing it." }
    Expand-Archive -Path $zip -DestinationPath $Game -Force
    New-Item -ItemType Directory -Path (Join-Path $Game "BepInEx\plugins") -Force | Out-Null
    Write-Host "BepInEx $BepVersion installed."

    # 2. the patch
    $plugins = Join-Path $Game "BepInEx\plugins"
    foreach ($rel in "BlakeManorFR", "BlakeManorFR.dll") {
        $p = Join-Path $plugins $rel
        if (Test-Path $p) { Remove-Item -Path $p -Recurse -Force }
    }
    $payload = Join-Path $Here "BepInEx\plugins"
    if (Test-Path (Join-Path $payload "BlakeManorFR.dll")) {
        $source = "this archive"
    } else {
        Write-Host "Fetching the latest release ..."
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        $release = Invoke-RestMethod -Uri $ReleasesApi -UseBasicParsing
        $asset = $release.assets | Where-Object { $_.name -like "BlakeManorFR-*.zip" } | Select-Object -First 1
        if (-not $asset) { throw "Could not find a release archive on GitHub." }
        $pzip = Join-Path $Temp $asset.name
        Get-File $asset.browser_download_url $pzip
        $pdir = Join-Path $Temp "patch"
        Expand-Archive -Path $pzip -DestinationPath $pdir -Force
        $payload = Join-Path $pdir "BepInEx\plugins"
        $source = $asset.name
    }
    Copy-Item -Path (Join-Path $payload "*") -Destination $plugins -Recurse -Force
    Write-Host "Patch installed from $source."
    Write-Host ""
    Write-Host "Done. Start the game from Steam as usual; it comes up in French."
    Write-Host "Options > Interface > Langue switches French / English at any time."
} finally {
    Remove-Item -Path $Temp -Recurse -Force -ErrorAction SilentlyContinue
}
