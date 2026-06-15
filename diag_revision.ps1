$fqdn = az containerapp show --name ca-web-ncbg27q3kcuoi --resource-group rg-manutech-ai --query 'properties.configuration.ingress.fqdn' -o tsv
Write-Host 'FQDN:' $fqdn
if ($fqdn) {
  try {
    $r = Invoke-WebRequest -UseBasicParsing -Uri "https://$fqdn/api/health" -Method GET -TimeoutSec 10 -ErrorAction Stop
    Write-Host 'Health status:' $r.StatusCode
    Write-Host 'Body:' $r.Content
  } catch {
    Write-Host 'Health check failed:' $_.Exception.Message
  }
} else {
  Write-Host 'No FQDN found (ingress may be disabled)'
}
Write-Host '=== Logs ==='
az containerapp logs show --name ca-web-ncbg27q3kcuoi --resource-group rg-manutech-ai --revision ca-web-ncbg27q3kcuoi--0000005 --tail 200 -o json
