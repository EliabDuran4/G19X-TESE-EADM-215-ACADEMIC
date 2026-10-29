# Bitácora de instalación desde clon limpio

- **Fecha:** 2026-10-29
- **Commit clonado:** c31ee14
- **Commit final probado (con correcciones):** b8f7906
- **Entorno:** Windows, Docker Desktop, Python 3.12.10, PowerShell
- **Método:** clon nuevo en carpeta vacía, sin copiar `.env` ni `.venv` del proyecto original.

## Resultado por paso del README

| Paso | Resultado | Observación |
|---|---|---|
| 1. Clonar | OK | |
| 2. Crear `.env` | OK (tras corrección) | `.env.example` traía `DATABASE_URL_DOCUMENTAL` y `DATABASE_URL_DOCKER` vacías y contraseñas `cambia_esto`, que incumplen la política de SQL Server |
| 3. Levantar servicios | OK (tras corrección) | Falló por variable requerida vacía y por conflicto de `container_name` con otra copia del proyecto |
| 4. Crear la base | OK (tras corrección) | El comando con comillas no funciona en PowerShell |
| 5. Crear tablas | OK | |
| 5 bis. Vistas | OK | Misma variante PowerShell |
| 6. Abrir la app | OK | |

## Pruebas automáticas (venv nuevo, sin `.env`)

`pip install -r requirements-dev.txt` y `python -m pytest`: **6 passed**.

## Problemas encontrados y correcciones

1. `.env.example` con URLs de BD vacías: se completaron los valores de ejemplo.
2. Contraseña de ejemplo inválida para SQL Server: se cambió por un valor que cumple la política y se documentó en el README.
3. Conflicto de `container_name`: no se pueden levantar dos copias a la vez; se añadió nota en el README.
4. SQL Server tarda en el primer arranque con volumen nuevo: se indicó esperar a "ready for client connections".
5. Comando `sqlcmd` del paso 4 (y 5 bis) incompatible con PowerShell: se añadió variante por stdin.
6. Requisito de memoria: se documentó la RAM necesaria para Docker.