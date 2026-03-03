# Publicar en GitHub

## Crear repo y push inicial

```bash
git init
git add .
git commit -m "Bootstrap GPT-CodexBridge with agent server and termux client"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/cursor-termux-bridge.git
git push -u origin main
```

## Desde Termux

```bash
git clone https://github.com/TU_USUARIO/cursor-termux-bridge.git
cd cursor-termux-bridge
bash scripts/setup_termux.sh
```
