<#
.SYNOPSIS
    Installs skills from this repository into your personal Claude skills folder, or packages them as upload-ready zips.
.DESCRIPTION
    Copies each skills/<name> folder to ~/.claude/skills/<name> (overwriting older copies of the same skill).
    With -Zip, builds dist/<name>.zip files. Use -Format Root (default) for Gemini and Microsoft Copilot
    (SKILL.md at archive root), or -Format Folder for claude.ai (<name>/SKILL.md inside the archive).
.PARAMETER Skills
    Optional list of skill names to install. Defaults to all skills.
.PARAMETER Destination
    Target skills folder. Defaults to $HOME/.claude/skills.
.PARAMETER Zip
    Create dist/<name>.zip packages instead of installing.
.PARAMETER Format
    Archive layout when -Zip is used: 'Root' (SKILL.md at zip root, for Gemini & Copilot — default)
    or 'Folder' (<name>/SKILL.md, for claude.ai).
.EXAMPLE
    ./install.ps1
    Installs every skill.
.EXAMPLE
    ./install.ps1 -Skills vmware-vsphere, windows-server -WhatIf
    Shows what would be installed for two skills.
.EXAMPLE
    ./install.ps1 -Zip
    Builds Gemini/Copilot upload-ready zips (SKILL.md at root) in ./dist.
.EXAMPLE
    ./install.ps1 -Zip -Format Folder
    Builds claude.ai upload-ready zips (<name>/SKILL.md) in ./dist.
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter()]
    [string[]]$Skills,

    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string]$Destination = (Join-Path -Path $HOME -ChildPath '.claude/skills'),

    [Parameter()]
    [switch]$Zip,

    [Parameter()]
    [ValidateSet('Root', 'Folder')]
    [string]$Format = 'Root'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$sourceRoot = Join-Path -Path $PSScriptRoot -ChildPath 'skills'
$available = Get-ChildItem -Path $sourceRoot -Directory | Where-Object { Test-Path -Path (Join-Path $_.FullName 'SKILL.md') }

if ($Skills) {
    $unknown = $Skills | Where-Object { $_ -notin $available.Name }
    foreach ($name in $unknown) { Write-Warning "Unknown skill: $name" }
    $selected = $available | Where-Object { $_.Name -in $Skills }
}
else {
    $selected = $available
}

if ($Zip) {
    $distRoot = Join-Path -Path $PSScriptRoot -ChildPath 'dist'
    New-Item -ItemType Directory -Path $distRoot -Force | Out-Null
    foreach ($skill in $selected) {
        $zipPath = Join-Path -Path $distRoot -ChildPath "$($skill.Name).zip"
        if ($PSCmdlet.ShouldProcess($zipPath, "Create skill package ($Format layout)")) {
            if ($Format -eq 'Folder') {
                # Zip the folder itself so the archive contains <name>/SKILL.md (claude.ai)
                Compress-Archive -Path $skill.FullName -DestinationPath $zipPath -Force
            }
            else {
                # Zip the contents directly so SKILL.md sits at archive root (Gemini & Copilot)
                $items = Get-ChildItem -Path $skill.FullName -Force | Where-Object { $_.Name -notin @('__pycache__', '.DS_Store', 'Thumbs.db') }
                Compress-Archive -Path $items.FullName -DestinationPath $zipPath -Force
            }
            Write-Output "[OK] $($skill.Name) -> $zipPath ($Format)"
        }
    }
    return
}

New-Item -ItemType Directory -Path $Destination -Force | Out-Null
foreach ($skill in $selected) {
    $target = Join-Path -Path $Destination -ChildPath $skill.Name
    if ($PSCmdlet.ShouldProcess($target, 'Install skill')) {
        if (Test-Path -Path $target) {
            Remove-Item -Path $target -Recurse -Force
        }
        Copy-Item -Path $skill.FullName -Destination $target -Recurse
        Write-Output "[OK] $($skill.Name) -> $target"
    }
}
