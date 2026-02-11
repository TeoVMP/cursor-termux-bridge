# Instrucciones para subir a GitHub

## Opción 1: Usando GitHub Web (Más fácil)

1. Ve a https://github.com/new
2. Nombre del repositorio: `cursor-termux-bridge`
3. Descripción: "Bridge system to code and query Cursor/IA from Termux on Android"
4. Elige público o privado
5. **NO** inicialices con README, .gitignore o licencia (ya los tenemos)
6. Click en "Create repository"

7. Luego ejecuta estos comandos (GitHub te los mostrará):

```bash
git remote add origin https://github.com/TU_USUARIO/cursor-termux-bridge.git
git branch -M main
git push -u origin main
```

## Opción 2: Usando GitHub CLI (si lo tienes instalado)

```bash
gh repo create cursor-termux-bridge --public --source=. --remote=origin --push
```

## Opción 3: Usando API de GitHub (con token)

Si tienes un token de GitHub en la variable de entorno `GITHUB_TOKEN`:

```bash
# El script deploy.sh intentará crear el repositorio automáticamente
bash deploy.sh
```
