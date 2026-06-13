$uri = 'https://management.azure.com/subscriptions/cd2b8ef3-5c1e-47f0-8859-41c3bcffef17/resourceGroups/rg-manutech-ai/providers/Microsoft.App/containerApps/ca-web-ncbg27q3kcuoi?api-version=2026-03-02-preview'
Write-Host "GET $uri"
$json = az rest --method GET --uri $uri -o json
if ($LASTEXITCODE -ne 0) { Write-Host 'az rest GET failed' ; exit 1 }
$obj = $json | ConvertFrom-Json
$changed = $false
foreach ($c in $obj.properties.template.containers) {
    if ($null -ne $c.probes) {
        foreach ($p in $c.probes) {
            if ($null -ne $p.httpGet -and $p.httpGet.port -eq 8080) {
                Write-Host "Changing probe port 8080 -> 80 for container $($c.name)"
                $p.httpGet.port = 80
                $changed = $true
            }
        }
    }
}
if (-not $changed) { Write-Host 'No probe ports equal to 8080 found; nothing to change' }
$body = @{ properties = @{ template = $obj.properties.template } } | ConvertTo-Json -Depth 20
$body | Out-File -FilePath .\patch-probes.json -Encoding utf8
Write-Host 'Wrote patch-probes.json'
Write-Host 'PATCHing resource using file body...'
$azArgs = @('--method','PATCH','--uri',$uri,'--headers','Content-Type=application/json','--body','@patch-probes.json','-o','json')
$patchOut = & az rest @azArgs
Write-Host $patchOut
if ($LASTEXITCODE -ne 0) { Write-Host 'az rest PATCH failed'; exit 1 }
Write-Host 'Fetching revision status for ca-web-ncbg27q3kcuoi--0000004'
az containerapp revision show --name ca-web-ncbg27q3kcuoi --resource-group rg-manutech-ai --revision ca-web-ncbg27q3kcuoi--0000004 --query '{name:name, active:properties.active, ready:properties.ready, replicas:properties.replicas, runningState:properties.runningState, healthState:properties.healthState, probes:properties.template.containers[0].probes}' -o json
if ($LASTEXITCODE -ne 0) { Write-Host 'Failed to fetch revision'; exit 1 }
Write-Host 'Done'
