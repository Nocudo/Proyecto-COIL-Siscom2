# Script de configuracion rapida de dominios locales en C:\Windows\System32\drivers\etc\hosts
# Permite resolver de inmediato los nombres de dominio en cualquier navegador

$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$ip = "172.22.201.2"
$domains = @(
    "www.coil-group2.com",
    "coil-group2.com",
    "unillanos.coil-group2.com",
    "seneca.coil-group2.com"
)

$content = Get-Content $hostsPath -Raw -ErrorAction Stop

$entriesToAdd = @()
foreach ($domain in $domains) {
    if ($content -notmatch [regex]::Escape("$domain")) {
        $entriesToAdd += "$ip`t$domain"
    }
}

if ($entriesToAdd.Count -gt 0) {
    $block = "`r`n# --- COIL GROUP 2 SD-WAN ENTRIES ---`r`n" + ($entriesToAdd -join "`r`n") + "`r`n"
    Add-Content -Path $hostsPath -Value $block -Encoding utf8
    Write-Host "Se agregaron $($entriesToAdd.Count) entradas a $hostsPath"
} else {
    Write-Host "Todas las entradas de dominio ya se encuentran presentes en $hostsPath"
}

# Flush DNS Cache
Clear-DnsClientCache
Write-Host "Cache DNS limpiada exitosamente. Dominios listos para navegacion."
