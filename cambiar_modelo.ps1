# Script para cambiar el modelo de OpenAI
# Ejecuta: .\cambiar_modelo.ps1 gpt-4-turbo

param(
    [string]$modelo = "gpt-4-turbo"
)

Write-Host "Cambiando modelo a: $modelo" -ForegroundColor Cyan

if (-not (Test-Path .env)) {
    Write-Host "Error: .env no existe" -ForegroundColor Red
    exit 1
}

$content = Get-Content .env -Raw

if ($content -match "OPENAI_MODEL=") {
    $content = $content -replace "OPENAI_MODEL=.*", "OPENAI_MODEL=$modelo"
} else {
    $content += "`nOPENAI_MODEL=$modelo`n"
}

$content | Set-Content .env -NoNewline

Write-Host "✓ Modelo cambiado a: $modelo" -ForegroundColor Green
Write-Host "`nModelos disponibles:" -ForegroundColor Cyan
Write-Host "  - gpt-4-turbo (recomendado)" -ForegroundColor White
Write-Host "  - gpt-4" -ForegroundColor White
Write-Host "  - gpt-3.5-turbo (más barato)" -ForegroundColor White
Write-Host "`nReinicia el servidor para aplicar los cambios." -ForegroundColor Yellow
