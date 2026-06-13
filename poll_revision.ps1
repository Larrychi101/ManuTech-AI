$uri = 'ca-web-ncbg27q3kcuoi--0000005'
$max=30
for ($i=0;$i -lt $max;$i++) {
    $s = az containerapp revision show --name ca-web-ncbg27q3kcuoi --resource-group rg-manutech-ai --revision $uri -o json 2>$null
    if ($LASTEXITCODE -ne 0) { Write-Host 'az failed' ; exit 1 }
    $obj = $s | ConvertFrom-Json
    $hs = $obj.healthState
    $rs = $obj.runningState
    Write-Host ("poll {0}: health={1} running={2} ready={3} replicas={4}" -f $i,$hs,$rs,$obj.ready,$obj.replicas)
    if ($hs -eq 'Healthy') { Write-Host 'Revision is Healthy'; exit 0 }
    Start-Sleep -Seconds 10
}
Write-Host 'Timed out waiting for Healthy'
exit 2
