#!/bin/bash
# Script para crear y subir el repositorio a GitHub

REPO_NAME="cursor-termux-bridge"
DESCRIPTION="Bridge system to code and query Cursor/IA from Termux on Android"

# Verificar si hay cambios sin commitear
if [ -n "$(git status --porcelain)" ]; then
    echo "Hay cambios sin commitear. Haciendo commit..."
    git add .
    git commit -m "Update: preparando para GitHub"
fi

# Intentar crear repositorio con GitHub CLI
if command -v gh &> /dev/null; then
    echo "Creando repositorio con GitHub CLI..."
    gh repo create $REPO_NAME --public --description "$DESCRIPTION" --source=. --remote=origin --push
    exit 0
fi

# Intentar crear con API de GitHub (requiere GITHUB_TOKEN)
if [ -n "$GITHUB_TOKEN" ]; then
    echo "Creando repositorio con API de GitHub..."
    USERNAME=$(git config user.name)
    
    # Crear repositorio
    curl -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        https://api.github.com/user/repos \
        -d "{\"name\":\"$REPO_NAME\",\"description\":\"$DESCRIPTION\",\"public\":true}"
    
    # Añadir remote y push
    git remote add origin https://github.com/$USERNAME/$REPO_NAME.git
    git branch -M main
    git push -u origin main
    exit 0
fi

# Si no hay GitHub CLI ni token, mostrar instrucciones
echo "No se encontró GitHub CLI ni GITHUB_TOKEN."
echo ""
echo "Por favor, crea el repositorio manualmente:"
echo "1. Ve a https://github.com/new"
echo "2. Nombre: $REPO_NAME"
echo "3. Descripción: $DESCRIPTION"
echo "4. NO inicialices con README"
echo "5. Luego ejecuta:"
echo ""
echo "   git remote add origin https://github.com/TU_USUARIO/$REPO_NAME.git"
echo "   git branch -M main"
echo "   git push -u origin main"
