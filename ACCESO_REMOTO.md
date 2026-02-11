# 🌐 Configuración de Acceso Remoto

Como no estás en la misma red, necesitas una forma de acceder al servidor remotamente. Aquí tienes las mejores opciones:

## Opción 1: Tailscale (Recomendado - VPN Mesh)

**Ventajas:**
- ✅ Gratis para uso personal
- ✅ Muy fácil de configurar
- ✅ Seguro (WireGuard)
- ✅ Funciona en Android/Termux
- ✅ No requiere configuración de puertos

### Instalación:

**En tu computadora (Windows):**
1. Descarga Tailscale: https://tailscale.com/download
2. Instala y crea cuenta
3. Conecta: `tailscale up`
4. Copia tu IP de Tailscale: `tailscale ip`

**En tu teléfono (Android):**
1. Instala Tailscale desde Google Play Store
2. Inicia sesión con la misma cuenta
3. Conecta

**En Termux:**
```bash
# Instalar Tailscale CLI (opcional, pero recomendado)
pkg install tailscale

# O usar la app de Android directamente
```

**Configuración:**
```bash
# En Termux, usa la IP de Tailscale de tu computadora
export CURSOR_SERVER_URL='http://100.x.x.x:8000'  # IP de Tailscale
```

---

## Opción 2: ngrok (Más fácil para pruebas rápidas)

**Ventajas:**
- ✅ Muy fácil de usar
- ✅ No requiere instalación en el teléfono
- ✅ HTTPS automático

**Desventajas:**
- ⚠️ URL cambia cada vez (gratis) o necesitas plan de pago
- ⚠️ Límite de conexiones en plan gratis

### Instalación:

**En tu computadora:**
1. Descarga ngrok: https://ngrok.com/download
2. Crea cuenta y obtén tu token
3. Configura: `ngrok config add-authtoken TU_TOKEN`
4. Inicia túnel: `ngrok http 8000`
5. Copia la URL HTTPS (ej: `https://abc123.ngrok.io`)

**En Termux:**
```bash
export CURSOR_SERVER_URL='https://abc123.ngrok.io'
```

---

## Opción 3: Cloudflare Tunnel (Gratis y Confiable)

**Ventajas:**
- ✅ Completamente gratis
- ✅ URL permanente
- ✅ HTTPS automático
- ✅ Sin límites

**Desventajas:**
- ⚠️ Requiere dominio (puedes usar uno gratis)

### Instalación:

**En tu computadora:**
1. Instala cloudflared: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
2. Crea túnel: `cloudflared tunnel create cursor-bridge`
3. Configura: `cloudflared tunnel route dns cursor-bridge tu-subdominio.tu-dominio.com`
4. Inicia: `cloudflared tunnel run cursor-bridge --url http://localhost:8000`

---

## Opción 4: SSH Tunnel (Si tienes servidor)

Si tienes un servidor con IP pública:

```bash
# En tu computadora
ssh -R 8000:localhost:8000 usuario@tu-servidor.com

# En Termux
export CURSOR_SERVER_URL='http://tu-servidor.com:8000'
```

---

## Recomendación: Tailscale

Para tu caso, **Tailscale es la mejor opción** porque:
- Funciona perfectamente en Android/Termux
- No necesitas configurar nada complejo
- Es seguro y privado
- La IP no cambia (mientras estés conectado)

### Pasos rápidos con Tailscale:

1. **Instala Tailscale en Windows** (tu computadora)
2. **Instala Tailscale en Android** (tu teléfono)
3. **Conecta ambos con la misma cuenta**
4. **En tu computadora**, ejecuta:
   ```powershell
   tailscale ip
   # Te dará algo como: 100.64.x.x
   ```
5. **En Termux**, configura:
   ```bash
   export CURSOR_SERVER_URL='http://100.64.x.x:8000'
   echo "export CURSOR_SERVER_URL='http://100.64.x.x:8000'" >> ~/.bashrc
   ```

¡Y listo! Ya puedes conectarte desde cualquier lugar.

---

## Solución Rápida: ngrok (Para probar ahora mismo)

Si quieres probar rápido sin instalar nada en el teléfono:

```bash
# En tu computadora:
ngrok http 8000

# Copia la URL HTTPS que te da (ej: https://abc123.ngrok.io)

# En Termux:
export CURSOR_SERVER_URL='https://abc123.ngrok.io'
```
