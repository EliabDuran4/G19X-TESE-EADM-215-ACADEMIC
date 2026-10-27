# LegalTech — Sistema de Observabilidad para Procesos Documentales

LegalTech es un sistema web de gestión y observabilidad de procesos documentales jurídicos, desarrollado como proyecto académico durante una estancia en PluriOne.

El sistema permite cargar, consultar, revisar, corregir, aprobar, rechazar, archivar y descargar documentos mediante un flujo controlado por roles. Integra persistencia en SQL Server, autenticación y autorización con Keycloak, observabilidad del **proceso documental** (no solo de las peticiones HTTP) con OpenTelemetry, Prometheus y Grafana, historial de cada documento y análisis asistido por Inteligencia Artificial.

> La Inteligencia Artificial funciona únicamente como herramienta de apoyo. No aprueba, rechaza ni modifica el estado de los documentos; la decisión final corresponde a los usuarios autorizados.

---

## Tabla de contenido

- [Arquitectura](#arquitectura)
- [Tecnologías](#tecnologías)
- [Roles del sistema](#roles-del-sistema)
- [Flujo documental](#flujo-documental)
- [Historial de documentos](#historial-de-documentos)
- [Inteligencia Artificial](#inteligencia-artificial)
- [Requisitos previos](#requisitos-previos)
- [Instalación y puesta en marcha](#instalación-y-puesta-en-marcha)
- [Configuración (.env)](#configuración-env)
- [Keycloak: realm y usuarios de prueba](#keycloak-realm-y-usuarios-de-prueba)
- [Observabilidad](#observabilidad)
- [Operación diaria](#operación-diaria)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Seguridad](#seguridad)
- [Documentación](#documentación)
- [Estado del proyecto](#estado-del-proyecto)
- [Autor](#autor)

---

## Arquitectura

```text
              ┌─────────────────────┐
              │  React.js + Vite    │
              │      Frontend       │
              └──────────┬──────────┘
                         │ HTTP / REST
                         ▼
              ┌─────────────────────┐
              │      FastAPI        │
              │      Backend        │
              └───┬─────┬─────┬─────┘
        ┌─────────┘     │     └──────────┐
        ▼               ▼                ▼
 ┌─────────────┐ ┌─────────────┐ ┌──────────────────┐
 │  Keycloak   │ │ SQL Server  │ │ IA: Claude API / │
 │  Auth / JWT │ │ Persistencia│ │ Ollama (local)   │
 └─────────────┘ └─────────────┘ └──────────────────┘

 Backend + OpenTelemetry SDK
        │
        ▼
 OpenTelemetry Collector ──► Prometheus ──► Grafana
                                  │
                                  └──► Reglas de alerta
```

La base de datos es una única instancia de SQL Server Developer Edition con la base `observabilidad_documental`. La arquitectura inicial contemplaba varios shards; la versión actual usa una sola base para reducir el consumo de recursos del entorno de desarrollo.

Todos los servicios se administran con Docker Compose.

---

## Tecnologías

| Capa | Tecnología |
|---|---|
| Frontend | React.js + Vite |
| Backend | Python + FastAPI |
| ORM | SQLAlchemy |
| Autenticación y autorización | Keycloak + JWT + roles |
| Base de datos | SQL Server Developer Edition |
| Observabilidad | OpenTelemetry + OpenTelemetry Collector |
| Métricas y alertas | Prometheus |
| Visualización | Grafana |
| Inteligencia Artificial | Claude API (Anthropic) u Ollama (local) |
| Contenerización | Docker + Docker Compose |
| Control de versiones | Git + GitHub |

---

## Roles del sistema

| Rol | Permisos principales |
|---|---|
| `usuario_documental` | Iniciar sesión, subir documentos y consultar sus propios documentos y estados. |
| `revisor_documental` | Subir, consultar y descargar documentos; iniciar revisión, comentar, marcar como revisado, solicitar correcciones, consultar el archivo, ver el historial y reabrir documentos finalizados. |
| `admin_documental` | Lo anterior más aprobar o rechazar, consultar el archivo y eliminar documentos. |

El acceso se controla con tokens JWT y roles administrados desde Keycloak.

---

## Flujo documental

```text
recibido ──► en_revision ──► revisado ──┬──► aprobado
                                        └──► rechazado
```

Cuando un documento necesita modificaciones:

```text
en_revision ──► correccion ──► en_revision
```

Los documentos finalizados pueden volver a revisión (reapertura intencional):

```text
aprobado ──┐
           ├──► en_revision
rechazado ─┘
```

---

## Historial de documentos

Cada cambio queda registrado en la tabla `document_events`: subida, revisión, decisión y eliminación, con estado anterior, estado nuevo, usuario, comentario y fecha.

- Endpoint: `GET /documents/{id}/events` (roles revisor y administrador).
- En el frontend, el botón **Historial** de cada documento muestra su línea de tiempo.

---

## Inteligencia Artificial

El análisis puede proporcionar resumen, observaciones, posibles inconsistencias, puntos a revisar, recomendaciones y una conclusión orientativa. Está disponible solo para revisor y administrador.

La IA **no** puede aprobar ni rechazar documentos, cambiar estados ni sustituir la decisión humana. El sistema sigue funcionando aunque el servicio de IA no esté disponible.

Proveedores (variables en `.env`):

| Variable | Valores |
|---|---|
| `AI_PROVIDER` | `ollama` (desarrollo local), `claude` (producción) o `none` |
| `AI_FALLBACK_PROVIDER` | `ollama` para respaldo en producción; vacío = sin respaldo |
| `ANTHROPIC_API_KEY` | Solo necesaria si el proveedor es `claude` |

---

## Requisitos previos

- Windows 10/11 o sistema compatible con Docker.
- Docker Desktop (con Docker Compose) y Git.
- Python 3.12 y ODBC Driver 18 para SQL Server, solo si se ejecuta el backend fuera de Docker o se corre `create_tables.py` desde el equipo.
- Navegador web.
- API Key de Anthropic, únicamente si se usará el análisis con Claude.

---

## Instalación y puesta en marcha

**1. Clonar el repositorio**

```powershell
git clone https://github.com/EliabDuran4/G19X-TESE-EADM-215-ACADEMIC.git
cd G19X-TESE-EADM-215-ACADEMIC
```

**2. Crear el `.env`** (ver [Configuración](#configuración-env))

```powershell
Copy-Item .env.example .env
```

Completar las contraseñas y los secretos. Los valores obligatorios sin definir hacen que `docker compose` se detenga con un mensaje claro.

**3. Levantar los servicios**

```powershell
docker compose up -d --build
docker compose ps
```

Keycloak tarda unos 30 a 60 segundos en importar el realm la primera vez.

**4. Crear la base de datos** (una sola vez)

```powershell
docker exec -it sqlserver_documental bash -c '/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -Q "CREATE DATABASE observabilidad_documental"'
```

También se puede ejecutar `CREATE DATABASE observabilidad_documental;` desde cualquier cliente SQL conectado a `localhost,1438` con el usuario `sa`.

**5. Crear las tablas** (incluye `document_events`)

```powershell
docker compose exec backend python create_tables.py
```

El script ya está dentro de la imagen del backend, así que no hace falta Python local.

**5 bis. Crear las vistas y el usuario de solo lectura** (necesario para `reporting-service` y `/reports`)

Los scripts de `database/scripts/` (`01_vista_resumen.sql`, `02_vista_estadisticas.sql`, `03_vista_trazabilidad.sql`, `04_usuario_reporting_ro.sql`) crean las vistas de reportes y el usuario `reporting_ro`. La contraseña se toma de `REPORTING_DB_PASSWORD` en el `.env`, sin editar ningún `.sql`:

```powershell
$p = (Select-String -Path .env -Pattern '^REPORTING_DB_PASSWORD=(.*)$').Matches.Groups[1].Value
docker cp database/scripts sqlserver_documental:/tmp/scripts
docker exec -e RPW=$p sqlserver_documental bash -c 'for f in /tmp/scripts/0*.sql; do /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -C -d observabilidad_documental -v REPORTING_DB_PASSWORD="$RPW" -b -i "$f" || exit 1; done'
```

Si tienes `sqlcmd` instalado en Windows, también sirve ejecutar cada script contra `localhost,1438` con `-v REPORTING_DB_PASSWORD=...`. Los scripts son repetibles: las vistas usan `CREATE OR ALTER` y el usuario `reporting_ro` se crea solo si no existe.

**6. Abrir la aplicación** en http://localhost:5173 con alguno de los [usuarios de prueba](#usuarios-de-prueba).

### Servicios y puertos

| Servicio | Dirección |
|---|---|
| Frontend | http://localhost:5173 |
| Backend / API | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| Keycloak | http://localhost:8080 |
| SQL Server | `localhost,1438` |
| OpenTelemetry Collector | `localhost:4317` (gRPC), `4318` (HTTP) |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| Reporting service | Interno: http://reporting-service:8001 (no se publica al host; se consulta a través del backend en `/reports`) |

### Reportes (`/reports`)

El backend expone estas rutas, que consultan el `reporting-service` por HTTP. Solo están disponibles para el rol `admin_documental` y requieren token de Keycloak:

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/reports/stats` | Estadísticas generales de documentos |
| GET | `/reports/documents/summary` | Resumen de documentos |
| GET | `/reports/documents/{document_id}/trace` | Trazabilidad de un documento |

Requieren haber ejecutado antes el paso 5 bis (vistas SQL y usuario `reporting_ro`). Se pueden probar desde Swagger en http://localhost:8000/docs.

> Si se ejecuta el backend localmente con `uvicorn` (puerto 8000), hay que detener antes el contenedor `backend` para evitar conflicto de puertos.

---

## Configuración (.env)

Existe **un único** archivo de variables, en la raíz del proyecto. Se copia desde `.env.example` y no se sube al repositorio. Lo leen `docker compose` y el backend (`backend/app/config.py`).

| Grupo | Variables |
|---|---|
| Contraseñas de infraestructura | `KEYCLOAK_ADMIN_PASSWORD`, `MSSQL_SA_PASSWORD`, `GRAFANA_ADMIN_PASSWORD`, `REPORTING_DB_PASSWORD` |
| Base de datos | `DATABASE_URL_DOCUMENTAL` (backend local, puerto 1438), `DATABASE_URL_DOCKER` (backend en Docker, host `sqlserver_documental`, puerto 1433) |
| Keycloak | `KEYCLOAK_URL`, `KEYCLOAK_REALM`, `KEYCLOAK_CLIENT_ID`, `KEYCLOAK_CLIENT_SECRET` |
| CORS | `CORS_ORIGINS` (orígenes del frontend separados por coma; por defecto `http://localhost:5173`) |
| OpenTelemetry | `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_SERVICE_NAME` |
| IA | `AI_PROVIDER`, `AI_FALLBACK_PROVIDER`, `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL`, `OLLAMA_URL`, `OLLAMA_MODEL`, `OLLAMA_TIMEOUT` |

`KEYCLOAK_CLIENT_SECRET` se usa en dos lugares: el backend y la importación del realm. Debe ser el mismo valor en ambos, por eso se define una sola vez aquí.

Ejemplo de `DATABASE_URL_DOCUMENTAL`:

```text
mssql+pyodbc://sa:<PASSWORD>@localhost:1438/observabilidad_documental?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes
```

Si la contraseña contiene caracteres especiales (`@`, `#`, `/`), deben ir codificados en la URL.

---

## Keycloak: realm y usuarios de prueba

El realm se importa automáticamente al crear el contenedor: `./keycloak` está montado en `/opt/keycloak/data/import` y Keycloak arranca con `start-dev --import-realm`. El archivo es `keycloak/observabilidad-documental-realm.json`.

- El realm **solo se importa si no existe**. Para reimportarlo desde cero, borrar únicamente el volumen de Keycloak:

  ```powershell
  docker compose stop keycloak
  docker compose rm -f keycloak
  docker volume rm observabilidad-documental_keycloak_data
  docker compose up -d keycloak
  ```

- El secreto del cliente se toma de `KEYCLOAK_CLIENT_SECRET` (el JSON contiene el marcador `${KEYCLOAK_CLIENT_SECRET}`).
- Consola de administración: http://localhost:8080 con `admin` y `KEYCLOAK_ADMIN_PASSWORD`.

### Usuarios de prueba

| Usuario | Rol |
|---|---|
| `usuariodoc1` | `usuario_documental` |
| `revisordoc1` | `revisor_documental` |
| `admindoc1` | `admin_documental` |

Los tres se crean con la contraseña temporal **`Temporal#2026`** y Keycloak obliga a cambiarla en el primer inicio de sesión. El primer cambio se hace en:

```text
http://localhost:8080/realms/observabilidad-documental/account
```

Después de reimportar el realm hay que cerrar sesión en el frontend para renovar el token.

---

## Observabilidad

La observabilidad cubre el **proceso documental**, no solo las peticiones HTTP.

### Métricas del proceso (backend)

Definidas en `backend/app/core/metrics.py` y exportadas con OpenTelemetry:

- Documentos subidos, por categoría.
- Transiciones de estado (`estado_anterior → estado_nuevo`).
- Tiempo hasta la decisión (aprobado o rechazado), en un histograma con cubetas pensadas para horas y días (`backend/app/core/telemetry.py`).
- Documentos por estado actual.

> La duración se mide desde el último estado `revisado` hasta la decisión del administrador, de modo que un documento reabierto no acumula el tiempo anterior.

### Métricas técnicas

Número y tasa de peticiones, latencia y disponibilidad de componentes.

### Dashboard de Grafana

El datasource y el dashboard `proceso_documental.json` se provisionan automáticamente desde `observability/grafana/`. Se accede en http://localhost:3000 con el usuario `admin` y `GRAFANA_ADMIN_PASSWORD`.

### Alertas

Reglas en `observability/alerts.yml`, cargadas por Prometheus:

- Cuello de botella en los estados `recibido`, `en_revision` y `correccion`.
- Percentil 95 del tiempo de decisión mayor a 24 horas.
- Colector de OpenTelemetry caído.

Se consultan en http://localhost:9090/alerts.

### Logs

Se consultan con los logs de los contenedores. El proyecto no utiliza Grafana Loki.

```powershell
docker compose logs backend
docker compose logs -f
```

---

## Operación diaria

| Acción | Comando |
|---|---|
| Pausar los servicios sin eliminar contenedores | `docker compose stop` |
| Volver a levantarlos | `docker compose up -d` |
| Ver el estado | `docker compose ps` |

Los datos de SQL Server viven en el volumen `sqlserver_documental_data`, montado en `/var/opt/mssql`, y sobreviven a `docker compose down`. **No** usar `docker compose down -v` ni `docker volume rm` sobre ese volumen: borran la base de datos.

---

## Estructura del proyecto

```text
G19X-TESE-EADM-215-ACADEMIC/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── database.py
│   │   │   ├── metrics.py
│   │   │   ├── security.py
│   │   │   └── telemetry.py
│   │   ├── models/
│   │   │   ├── document.py
│   │   │   └── document_event.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── documents.py
│   │   │   └── reports.py
│   │   ├── services/
│   │   │   └── ai_service.py
│   │   ├── config.py
│   │   └── main.py
│   ├── create_tables.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/DocumentRow.jsx
│   │   ├── pages/ (Archive.jsx, Documents.jsx, Login.jsx)
│   │   ├── services/ (api.js, authService.js, documentService.js)
│   │   └── App.jsx, main.jsx, index.css
│   └── package.json
│
├── keycloak/
│   └── observabilidad-documental-realm.json
├── reporting-service/   # FastAPI de solo lectura sobre las vistas SQL (puerto interno 8001)
│
├── database/
│   └── scripts/
│       ├── 01_vista_resumen.sql
│       ├── 02_vista_estadisticas.sql
│       ├── 03_vista_trazabilidad.sql
│       └── 04_usuario_reporting_ro.sql
│
├── observability/
│   ├── alerts.yml
│   ├── otel-collector-config.yaml
│   ├── prometheus.yml
│   └── grafana/ (datasource y dashboard proceso_documental.json)
│
├── MarkDown/            # documentación formal
├── .env.example
├── .gitignore
└── docker-compose.yml
```

---

## Seguridad

- Autenticación con Keycloak, autorización por roles y tokens JWT.
- Validación de permisos en el backend.
- Credenciales y secretos solo en `.env`, excluido con `.gitignore`.
- El realm exportado no contiene hashes de contraseñas; los usuarios de prueba usan una contraseña temporal que debe cambiarse.
- CORS limitado a los orígenes definidos en `CORS_ORIGINS`.
- La API Key de la IA no se almacena en el código fuente.

> Nunca deben publicarse contraseñas, Client Secrets, tokens, API Keys ni archivos `.env` reales. Antes de cada commit, revisar con `git status`.

---

## Documentación

La documentación formal está en `MarkDown/`: requerimientos, propuesta técnica, arquitectura, MVP, PRD, SCRUM, manual técnico, manual de usuario, QA, mantenimiento y soporte, capacitación y entrega, y evaluación post-implementación.

---

## Estado del proyecto

Estado actual: **MVP funcional**.

Se realizaron pruebas funcionales QA-01 a QA-12 (autenticación, permisos por rol, flujo documental, persistencia, observabilidad, archivo, reapertura, seguridad básica, reproducibilidad local, IA multi-proveedor y su uso desde la interfaz). Resultados y evidencias en `MarkDown/QA.md`.
Además, el backend cuenta con pruebas automáticas (pytest) en `backend/tests/`; se ejecutan con `python -m pytest -q` desde `backend/`.
La implementación de CI/CD con GitHub Actions no forma parte del alcance actual.

---

## Autor

Eliab Azarel Duran Martinez