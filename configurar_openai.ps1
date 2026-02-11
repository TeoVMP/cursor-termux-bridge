# Script para configurar OpenAI en .env
# Ejecuta: .\configurar_openai.ps1

# Configura tu API key aquí o edita .env manualmente
$apiKey = Read-Host "Ingresa tu OpenAI API Key (o deja vacío para usar .env)"
if ([string]::IsNullOrWhiteSpace($apiKey)) {
    Write-Host "Usando API key de .env si existe" -ForegroundColor Yellow
    exit 0
}

Write-Host "Configurando OpenAI en .env..." -ForegroundColor Cyan

# Verificar si .env existe
if (-not (Test-Path .env)) {
    Write-Host "Creando .env desde env.example..." -ForegroundColor Yellow
    Copy-Item config\env.example .env
}

# Leer contenido actual
$content = Get-Content .env -Raw

# Configurar AI_PROVIDER
if ($content -match "AI_PROVIDER=") {
    $content = $content -replace "AI_PROVIDER=.*", "AI_PROVIDER=openai"
} else {
    $content += "`nAI_PROVIDER=openai`n"
}

# Configurar OPENAI_API_KEY
if ($content -match "OPENAI_API_KEY=") {
    $content = $content -replace "OPENAI_API_KEY=.*", "OPENAI_API_KEY=$apiKey"
} else {
    $content += "OPENAI_API_KEY=$apiKey`n"
}

# Configurar OPENAI_MODEL si no está
if (-not ($content -match "OPENAI_MODEL=")) {
    $content += "OPENAI_MODEL=gpt-4-turbo`n"
} else {
    $content = $content -replace "OPENAI_MODEL=.*", "OPENAI_MODEL=gpt-4-turbo"
}

# Guardar
$content | Set-Content .env -NoNewline

Write-Host "`n✓ Configuración completada!" -ForegroundColor Green
Write-Host "`nVariables configuradas:" -ForegroundColor Cyan
Write-Host "  AI_PROVIDER=openai" -ForegroundColor White
Write-Host "  OPENAI_API_KEY=sk-proj-..." -ForegroundColor White
Write-Host "  OPENAI_MODEL=gpt-4" -ForegroundColor White
Write-Host "`nReinicia el servidor para aplicar los cambios." -ForegroundColor Yellow
