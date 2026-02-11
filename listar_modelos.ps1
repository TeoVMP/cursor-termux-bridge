# Script para listar modelos disponibles de OpenAI
# Ejecuta: .\listar_modelos.ps1

Write-Host "Obteniendo modelos disponibles de OpenAI..." -ForegroundColor Cyan

# Cargar API key desde .env
$envContent = Get-Content .env -Raw
if ($envContent -match "OPENAI_API_KEY=(.+)") {
    $apiKey = $matches[1].Trim()
} else {
    Write-Host "Error: OPENAI_API_KEY no encontrada en .env" -ForegroundColor Red
    exit 1
}

try {
    $headers = @{
        "Authorization" = "Bearer $apiKey"
    }
    
    $response = Invoke-RestMethod -Uri "https://api.openai.com/v1/models" -Headers $headers -Method Get
    
    Write-Host "`nModelos GPT disponibles:" -ForegroundColor Green
    Write-Host "=" * 50 -ForegroundColor Cyan
    
    $gptModels = $response.data | Where-Object { $_.id -like "*gpt*" } | Sort-Object id
    
    foreach ($model in $gptModels) {
        Write-Host "  - $($model.id)" -ForegroundColor Yellow
    }
    
    Write-Host "`nModelos recomendados para código:" -ForegroundColor Green
    $recommended = $gptModels | Where-Object { 
        $_.id -like "*gpt-4*" -or $_.id -like "*gpt-3.5-turbo*" 
    }
    
    foreach ($model in $recommended) {
        Write-Host "  ✓ $($model.id)" -ForegroundColor Cyan
    }
    
} catch {
    Write-Host "Error al obtener modelos: $_" -ForegroundColor Red
    Write-Host "`nVerifica que tu API key sea válida" -ForegroundColor Yellow
}
