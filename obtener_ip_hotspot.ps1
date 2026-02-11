# Script PowerShell para obtener la IP cuando estás conectado al hotspot
# Ejecuta: .\obtener_ip_hotspot.ps1

Write-Host "=== Obteniendo IP de conexión WiFi ===" -ForegroundColor Cyan
Write-Host ""

# Obtener todas las interfaces de red IPv4
$interfaces = Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
    $_.IPAddress -notlike "127.*" -and 
    $_.IPAddress -notlike "169.254.*"
} | Select-Object IPAddress, InterfaceAlias

if ($interfaces) {
    Write-Host "IPs encontradas:" -ForegroundColor Green
    Write-Host ""
    foreach ($if in $interfaces) {
        Write-Host "  $($if.IPAddress) - $($if.InterfaceAlias)" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Usa la IP de tu conexión WiFi (no la de Loopback)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "En Termux, configura:" -ForegroundColor Green
    Write-Host "  export CURSOR_SERVER_URL='http://IP_AQUI:8000'" -ForegroundColor White
} else {
    Write-Host "No se encontraron interfaces de red activas" -ForegroundColor Red
    Write-Host "Asegúrate de estar conectado al hotspot WiFi" -ForegroundColor Yellow
}
