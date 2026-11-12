$ErrorActionPreference = 'Stop'
$chromePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$guidePath = Join-Path $PSScriptRoot 'BUILD-GUIDE.html'
$profilePath = Join-Path $PSScriptRoot 'checks-browser-profile'
$guideSource = Get-Content -LiteralPath $guidePath -Raw
$guideHeader = $guideSource.Substring(0, $guideSource.IndexOf('<main>'))
$sectionHtml = [regex]::Match($guideSource, '<section id="step-13">[\s\S]*?</section>').Value
if (-not $sectionHtml) {throw 'Missing touch assembly section'}
$qaPath = Join-Path $PSScriptRoot 'checks-guide-section.html'
Set-Content -LiteralPath $qaPath -Value ($guideHeader + '<main>' + $sectionHtml + '</main></html>') -Encoding utf8
foreach ($case in @(@{name='guide-top';page=$guidePath}, @{name='guide-touch';page=$qaPath})) {
  $screenPath = Join-Path $PSScriptRoot ('renders\' + $case.name + '.png')
  $domPath = Join-Path $PSScriptRoot ($case.name + '-dom.txt')
  $errPath = Join-Path $PSScriptRoot ($case.name + '-err.txt')
  $guideUri = ([uri]$case.page).AbsoluteUri
  $arguments = @('--headless=new','--disable-background-networking','--no-first-run','--no-default-browser-check','--window-size=1500,1000','--virtual-time-budget=1500',('--user-data-dir="'+$profilePath+'"'),('--screenshot="'+$screenPath+'"'),'--dump-dom',('"'+$guideUri+'"'))
  $guideBrowser = Start-Process -FilePath $chromePath -ArgumentList $arguments -WindowStyle Hidden -PassThru -RedirectStandardOutput $domPath -RedirectStandardError $errPath
  if (-not $guideBrowser.WaitForExit(20000)) {throw 'Guide render timed out'}
  if ($guideBrowser.ExitCode -ne 0) {throw 'Guide render failed'}
  if ((Get-Item -LiteralPath $screenPath).Length -lt 20000) {throw 'Unexpectedly empty guide screenshot'}
  Write-Output ($case.name + ': rendered')
}
