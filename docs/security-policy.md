# Politica de seguridad

## Principios

- Minimo privilegio: solo rutas y comandos permitidos.
- Aprobacion explicita para acciones de riesgo.
- Auditoria completa de operaciones.

## Controles

- `allowed_roots`: rutas base donde se permiten operaciones.
- `blocked_commands`: prefijos de comandos prohibidos.
- `confirm_command_patterns`: patrones que requieren aprobacion.
- `shell_timeout_seconds`: timeout de procesos shell.
- `max_output_chars`: limite de salida capturada.

## Modo plan-first

Cuando `plan_first=true`, las operaciones mutables (`write_file`, `apply_patch`, `run_shell`) quedan bloqueadas hasta que el cliente envie una aprobacion de plan.
