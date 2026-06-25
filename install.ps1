$ErrorActionPreference = "Stop"

function Test-PythonCandidate {
    param(
        [Parameter(Mandatory = $true)][string]$Exe,
        [Parameter(Mandatory = $true)][string[]]$Args
    )

    $command = Get-Command -Name $Exe -ErrorAction SilentlyContinue
    if ($null -eq $command) {
        return $null
    }

    $probe = & $Exe @($Args + @("-c", "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)")) 2>$null
    if ($LASTEXITCODE -eq 0) {
        return @{ Exe = $Exe; Args = $Args }
    }
    return $null
}

function Resolve-Python {
    $candidates = @(
        @{ Exe = "py"; Args = @("-3") },
        @{ Exe = "python3"; Args = @() },
        @{ Exe = "python"; Args = @() }
    )

    foreach ($candidate in $candidates) {
        $resolved = Test-PythonCandidate -Exe $candidate.Exe -Args $candidate.Args
        if ($null -ne $resolved) {
            return $resolved
        }
    }
    return $null
}

$python = Resolve-Python
if ($null -eq $python) {
    Write-Error "Python 3.10+ is required but was not found."
    exit 1
}

if ($null -eq (Get-Command -Name git -ErrorAction SilentlyContinue)) {
    Write-Error "Git is required but was not found."
    exit 1
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$installer = Join-Path $scriptDir "scripts\install.py"
& $python.Exe @($python.Args + @($installer) + $args)
exit $LASTEXITCODE
