# Bitácora de instalación desde clon limpio

- **Fecha:** 2026-10-29 (instalación limpia y pruebas); 2026-11-04 (flujo funcional de tres usuarios y correcciones del README)
- **Commit clonado:** c31ee14
- **Commit final probado (con correcciones):** b8f7906
- **Commit con las correcciones del README (retro 7):** <hash del push de hoy>
- **Entorno:** Windows, Docker Desktop, Python 3.12.10, PowerShell
- **Método:** clon nuevo en carpeta vacía, sin copiar `.env` ni `.venv` del proyecto original.
- **Flujo funcional (2026-11-04):** ejecutado en el repositorio de trabajo, con la BD de Docker local.

## Resultado por paso del README

| Paso | Resultado | Observación |
|---|---|---|
| 1. Clonar | OK | |
| 2. Crear `.env` | OK (tras corrección) | `.env.example` traía `DATABASE_URL_DOCUMENTAL` y `DATABASE_URL_DOCKER` vacías y contraseñas `cambia_esto`, que incumplen la política de SQL Server |
| 3. Levantar servicios | OK (tras corrección) | Falló por variable requerida vacía y por conflicto de `container_name` con otra copia del proyecto |
| 4. Crear la base | OK (tras corrección) | El comando con comillas no funciona en PowerShell |
| 5. Crear tablas | OK | |
| 5 bis. Vistas | OK |
| 6. Abrir la app | OK | Flujo completo de los tres usuarios en la sección siguiente |
| Clonación final (2026-11-08) | Pasos 1 a 6 del README en PowerShell | OK, sin cambios |

## Flujo funcional con los tres usuarios

| # | Usuario | Acción | Resultado |
|---|---|---|---|
| 1 | `usuariodoc1` | Iniciar sesión y subir un documento | OK (3 documentos: contratos_corporativo, litigioso, regulatorio_compliance) |
| 2 | `usuariodoc1` | Verificar que el documento aparece en estado inicial | OK |
| 3 | `revisordoc1` | Iniciar sesión y revisar el documento | OK |
| 4 | `admindoc1` | Aprobar el documento | OK (los 3 quedaron en `aprobado`) |
| 5 | `revisordoc1` / `admindoc1` | Abrir «Historial» del documento (`GET /documents/{id}/events`) | OK |
| 6 | `admindoc1` | `GET /reports/stats` en Swagger | OK (3 documentos, 12 eventos, todos `aprobado`) |

**Respuesta de `GET /reports/stats`:**

~~~json
{
  "total_documentos": 3,
  "total_eventos": 12,
  "por_estado": {
    "aprobado": 3
  },
  "por_categoria_estado": [
    {
      "Categoria": "contratos_corporativo",
      "Estado": "aprobado",
      "TotalDocumentos": 1
    },
    {
      "Categoria": "litigioso",
      "Estado": "aprobado",
      "TotalDocumentos": 1
    },
    {
      "Categoria": "regulatorio_compliance",
      "Estado": "aprobado",
      "TotalDocumentos": 1
    }
  ]
}
~~~

## Pruebas automáticas (venv nuevo, sin `.env`)

`pip install -r requirements-dev.txt` y `python -m pytest`: **6 passed**.

## Problemas encontrados y correcciones

1. `.env.example` con URLs de BD vacías: se completaron los valores de ejemplo.
2. Contraseña de ejemplo inválida para SQL Server: se cambió por un valor que cumple la política y se documentó en el README.
3. Conflicto de `container_name`: no se pueden levantar dos copias a la vez; se añadió nota en el README.
4. SQL Server tarda en el primer arranque con volumen nuevo: se indicó esperar a "ready for client connections".
5. Comando `sqlcmd` del paso 4 (y 5 bis) incompatible con PowerShell: se añadió variante por stdin.
6. Requisito de memoria: se documentó la RAM necesaria para Docker.

## Prueba rápida de punta a punta

1. Inicia sesión y cambia la contraseña temporal en `/account`.
2. Con `usuariodoc1`, sube un documento.
3. Con `revisordoc1`, revisa el documento.
4. Con `admindoc1`, apruébalo.
5. Consulta el historial del documento.
6. Abre «Reportes» y verifica que carguen los datos.