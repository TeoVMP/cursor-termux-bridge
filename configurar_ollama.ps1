# Script para configurar Ollama (modelo local gratuito)
# Ejecuta: .\configurar_ollama.ps1

Write-Host "Configurando Ollama (modelo local gratuito)..." -ForegroundColor Cyan

# Verificar si Ollama está instalado
try {
    $ollamaVersion = ollama --version 2>&1
    Write-Host "✓ Ollama encontrado: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠ Ollama no está instalado" -ForegroundColor Yellow
    Write-Host "`nInstala Ollama desde: https://ollama.ai/download" -ForegroundColor Yellow
    Write-Host "O ejecuta: winget install Ollama.Ollama" -ForegroundColor Yellow
    Write-Host "`nDespués de instalar, ejecuta este script de nuevo." -ForegroundColor Yellow
    exit 1
}

# Verificar si .env existe
if (-not (Test-Path .env)) {
    Write-Host "Creando .env desde env.example..." -ForegroundColor Yellow
    Copy-Item config\env.example .env
}

# Leer contenido actual
$content = Get-Content .env -Raw

# Configurar AI_PROVIDER
if ($content -match "AI_PROVIDER=") {
    $content = $content -replace "AI_PROVIDER=.*", "AI_PROVIDER=ollama"
} else {
    $content += "`nAI_PROVIDER=ollama`n"
}

# Configurar OLLAMA_BASE_URL
if ($content -match "OLLAMA_BASE_URL=") {
    $content = $content -replace "OLLAMA_BASE_URL=.*", "OLLAMA_BASE_URL=http://localhost:11434"
} else {
    $content += "OLLAMA_BASE_URL=http://localhost:11434`n"
}

# Configurar OLLAMA_MODEL
Write-Host "`nModelos disponibles:" -ForegroundColor Cyan
Write-Host "  1. codellama (recomendado para código)" -ForegroundColor White
Write-Host "  2. deepseek-coder (muy bueno para código)" -ForegroundColor White
Write-Host "  3. llama3.2 (modelo general)" -ForegroundColor White
Write-Host "  4. mistral (rápido y eficiente)" -ForegroundColor White

$modelo = Read-Host "`nElige modelo (1-4) o escribe nombre personalizado [1]"
switch ($modelo) {
    "1" { $modeloElegido = "codellama" }
    "2" { $modeloElegido = "deepseek-coder" }
    "3" { $modeloElegido = "llama3.2" }
    "4" { $modeloElegido = "mistral" }
    "" { $modeloElegido = "codellama" }
    default { $modeloElegido = $modelo }
}

if ($content -match "OLLAMA_MODEL=") {
    $content = $content -replace "OLLAMA_MODEL=.*", "OLLAMA_MODEL=$modeloElegido"
} else {
    $content += "OLLAMA_MODEL=$modeloElegido`n"
}

# Guardar
$content | Set-Content .env -NoNewline

Write-Host "`n✓ Configuración completada!" -ForegroundColor Green
Write-Host "`nVariables configuradas:" -ForegroundColor Cyan
Write-Host "  AI_PROVIDER=ollama" -ForegroundColor White
Write-Host "  OLLAMA_BASE_URL=http://localhost:11434" -ForegroundColor White
Write-Host "  OLLAMA_MODEL=$modeloElegido" -ForegroundColor White

Write-Host "`n⚠ IMPORTANTE:" -ForegroundColor Yellow
Write-Host "  1. Asegúrate de que Ollama esté corriendo" -ForegroundColor White
Write-Host "  2. Descarga el modelo: ollama pull $modeloElegido" -ForegroundColor White
Write-Host "  3. Reinicia el servidor después de configurar" -ForegroundColor White

# Verificar si el modelo está descargado
Write-Host "`nVerificando si el modelo está descargado..." -ForegroundColor Cyan
try {
    $models = ollama list 2>&1
    if ($models -match $modeloElegido) {
        Write-Host "✓ Modelo $modeloElegido encontrado" -ForegroundColor Green
    } else {
        Write-Host "⚠ Modelo $modeloElegido no encontrado" -ForegroundColor Yellow
        Write-Host "  Ejecuta: ollama pull $modeloElegido" -ForegroundColor White
    }
} catch {
    Write-Host "⚠ No se pudo verificar modelos" -ForegroundColor Yellow
}
