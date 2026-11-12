$ErrorActionPreference = 'Stop'
$chromePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$viewerPath = Join-Path $PSScriptRoot 'EV3-Lift-Viewer.html'
$viewerUri = ([uri]$viewerPath).AbsoluteUri
$profilePath = Join-Path $PSScriptRoot 'checks-browser-profile'
$checks = @()
foreach ($case in @(@{name='lowered';query='';pose='0'}, @{name='raised';query='?pose=raised';pose='70'}, @{name='gears';query='?mode=gears';pose='0'})) {
    $screenPath = Join-Path $PSScriptRoot ('renders\viewer-' + $case.name + '.png')
    $domPath = Join-Path $PSScriptRoot ('viewer-dom-' + $case.name + '.txt')
    $errPath = Join-Path $PSScriptRoot ('viewer-stderr-' + $case.name + '.txt')
    $arguments = @('--headless=new', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--disable-background-networking', '--no-first-run', '--no-default-browser-check', '--window-size=1500,1000', '--virtual-time-budget=4000', ('--user-data-dir="' + $profilePath + '"'), ('--screenshot="' + $screenPath + '"'), '--dump-dom', ('"' + $viewerUri + $case.query + '"'))
    $browserProcess = Start-Process -FilePath $chromePath -ArgumentList $arguments -WindowStyle Hidden -PassThru -RedirectStandardOutput $domPath -RedirectStandardError $errPath
    if (-not $browserProcess.WaitForExit(20000)) { throw ('Browser did not finish: ' + $case.name) }
    $dom = Get-Content -Raw -LiteralPath $domPath
    $body = [regex]::Match($dom, '<body[^>]*>').Value
    $ok = ($browserProcess.ExitCode -eq 0) -and $body.Contains('data-render="ok"') -and $body.Contains('data-gl-error="0"') -and $body.Contains(('data-pose="' + $case.pose + '"'))
    if (-not $ok) { throw ('Viewer failed: ' + $case.name + ' ' + $body) }
    $checks += [pscustomobject]@{name=$case.name;status='PASS';exitCode=$browserProcess.ExitCode;body=$body}
    Write-Output ($case.name + ': PASS ' + $body)
}
[pscustomobject]@{viewerSha256=(Get-FileHash -LiteralPath $viewerPath -Algorithm SHA256).Hash;checks=$checks} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'browser-checks.json') -Encoding utf8
