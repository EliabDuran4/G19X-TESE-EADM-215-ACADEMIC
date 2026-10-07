# LegalTech — Sistema de Observabilidad para Procesos Documentales

LegalTech es un sistema web de gestión y observabilidad de procesos documentales jurídicos, desarrollado como proyecto académico durante una estancia en **PluriOne**.

El sistema permite cargar, consultar, revisar, corregir, aprobar, rechazar, archivar y descargar documentos mediante un flujo controlado por roles. Integra persistencia en **SQL Server**, autenticación y autorización mediante **Keycloak**, observabilidad con **OpenTelemetry, Prometheus y Grafana**, y análisis documental asistido por Inteligencia Artificial mediante **Claude API**.

> La Inteligencia Artificial funciona únicamente como herramienta de apoyo al análisis documental. No aprueba, rechaza ni modifica automáticamente el estado de los documentos; la decisión final corresponde a los usuarios autorizados.

---

## Tabla de contenido

- [Arquitectura](#arquitectura)
- [Tecnologías](#tecnologías)
- [Roles del sistema](#roles-del-sistema)
- [Flujo documental](#flujo-documental)
- [Inteligencia Artificial](#inteligencia-artificial)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [Observabilidad](#observabilidad)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Seguridad](#seguridad)
- [Documentación](#documentación)
- [Estado del proyecto](#estado-del-proyecto)
- [Autor](#autor)

---

## Arquitectura

LegalTech utiliza una arquitectura web compuesta por frontend, backend, autenticación, persistencia, observabilidad e integración con Inteligencia Artificial.

```text
                    ┌─────────────────────┐
                    │   React.js + Vite   │
                    │      Frontend       │
                    └──────────┬──────────┘
                               │ HTTP / REST
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │       Backend       │
                    └─────┬─────┬─────┬───┘
                          │     │     │
              ┌───────────┘     │     └──────────────┐
              ▼                 ▼                    ▼
       ┌─────────────┐   ┌─────────────┐      ┌─────────────┐
       │  Keycloak   │   │ SQL Server  │      │ Claude API  │
       │ Auth / JWT  │   │ Persistencia│      │ Análisis IA │
       └─────────────┘   └─────────────┘      └─────────────┘
              │
              │ autenticación
              │ y autorización
              ▼

       Backend + OpenTelemetry SDK
                    │
                    ▼
       OpenTelemetry Collector
                    │
                    ▼
              Prometheus
                    │
                    ▼
                Grafana
```

La base de datos utilizada actualmente es una única instancia de **SQL Server Developer Edition**, con la base:

```text
observabilidad_documental
```

La arquitectura inicial contemplaba múltiples shards; sin embargo, la versión actual del proyecto utiliza una sola base de datos SQL Server para optimizar el consumo de recursos del entorno de desarrollo.

Los servicios principales se ejecutan y administran mediante **Docker Compose**.

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
| Métricas | Prometheus |
| Visualización | Grafana |
| Inteligencia Artificial | Claude API (Anthropic) |
| Contenerización | Docker + Docker Compose |
| Control de versiones | Git + GitHub |

---

## Roles del sistema

LegalTech implementa tres roles principales:

| Rol | Permisos principales |
|---|---|
| `usuario_documental` | Iniciar sesión, subir documentos y consultar sus propios documentos y estados. |
| `revisor_documental` | Subir, consultar y descargar documentos; iniciar revisión, realizar comentarios, marcar como revisado, solicitar correcciones, consultar documentos aprobados/rechazados y reabrir documentos finalizados. |
| `admin_documental` | Subir, consultar y descargar documentos; aprobar o rechazar, consultar el archivo, reabrir documentos finalizados y eliminar documentos según los permisos disponibles. |

El acceso a las funcionalidades está controlado mediante tokens **JWT** y roles administrados desde Keycloak.

---

## Flujo documental

El flujo principal de los documentos es:

```text
recibido
   │
   ▼
en_revision
   │
   ▼
revisado
   │
   ├──────────────► aprobado
   │
   └──────────────► rechazado
```

Cuando un documento necesita modificaciones:

```text
en_revision
     │
     ▼
 correccion
     │
     ▼
en_revision
```

Los documentos finalizados también pueden volver al proceso de revisión:

```text
aprobado ──┐
           ├──► en_revision
rechazado ─┘
```

Esta reapertura es intencional y permite que un documento previamente finalizado pueda volver a ser revisado cuando sea necesario.

---

## Inteligencia Artificial

LegalTech integra **Claude API** como herramienta de apoyo al proceso de revisión documental.

El análisis puede proporcionar información como:

- Resumen del documento.
- Observaciones relevantes.
- Posibles inconsistencias.
- Puntos que requieren revisión.
- Recomendaciones.
- Conclusión orientativa.

La funcionalidad de análisis está destinada a los roles autorizados de revisión y administración.

La IA **no puede**:

- Aprobar documentos.
- Rechazar documentos.
- Cambiar estados automáticamente.
- Sustituir la decisión del revisor o administrador.

El sistema está diseñado para continuar funcionando aunque el servicio de IA no se encuentre disponible o no exista una API Key válida.

---

## Requisitos previos

Para ejecutar el proyecto localmente se recomienda contar con:

- Windows 10/11 o sistema compatible con Docker.
- Docker Desktop.
- Docker Compose.
- Git.
- PowerShell, Terminal o equivalente.
- Navegador web.
- Cuenta/API Key de Anthropic únicamente si se utilizará el análisis con IA.

> La funcionalidad principal del sistema no depende de Claude API para operar.

---

## Instalación

Clonar el repositorio:

```powershell
git clone https://github.com/EliabDuran4/G19X-TESE-EADM-215-ACADEMIC.git
```

Ingresar al proyecto:

```powershell
cd G19X-TESE-EADM-215-ACADEMIC
```

---

## Configuración

### 1. Variables de entorno

El archivo de ejemplo se encuentra en:

```text
backend/.env.example
```

Crear una copia:

```powershell
Copy-Item backend/.env.example backend/.env
```

Completar en `backend/.env` las variables requeridas por el proyecto, como:

- Conexión con SQL Server.
- Configuración de Keycloak.
- Configuración de OpenTelemetry.
- `ANTHROPIC_API_KEY`, cuando se utilice el análisis con IA.

### 2. Seguridad de las variables

El archivo real:

```text
backend/.env
```

no debe subirse al repositorio.

Antes de realizar un commit se recomienda verificar:

```powershell
git status
```

El repositorio únicamente debe contener el archivo de ejemplo:

```text
backend/.env.example
```

### 3. Configuración adicional

La configuración de SQL Server, Keycloak, observabilidad y demás componentes se encuentra detallada en:

```text
MarkDown/Manual_Tecnico.md
```

---

## Ejecución

Construir e iniciar los servicios:

```powershell
docker compose up -d --build
```

Comprobar el estado:

```powershell
docker compose ps
```

### Servicios principales

| Servicio | Dirección |
|---|---|
| Frontend | `http://localhost:5173` |
| Backend / API | `http://localhost:8000` |
| Swagger | `http://localhost:8000/docs` |
| Keycloak | `http://localhost:8080` |
| SQL Server | `localhost:1438` |
| Prometheus | `http://localhost:9090` |
| Grafana | `http://localhost:3000` |

La configuración inicial de Keycloak, incluyendo realm, client, roles y usuarios, se encuentra documentada en el manual técnico.

---

## Observabilidad

El proyecto incorpora observabilidad para facilitar el monitoreo del funcionamiento de la aplicación.

### Trazas

El backend utiliza **OpenTelemetry SDK** para instrumentar la aplicación y enviar telemetría al **OpenTelemetry Collector**.

### Métricas

Prometheus recopila las métricas expuestas por la infraestructura de observabilidad.

Entre las métricas utilizadas se encuentran indicadores relacionados con:

- Número de peticiones.
- Tasa de peticiones.
- Latencia.
- Disponibilidad de componentes.
- Estado general del sistema.

### Dashboards

Grafana permite visualizar las métricas mediante paneles configurados para supervisar el comportamiento del sistema.

### Alertas

Se dispone de reglas de alerta para detectar condiciones anómalas o indisponibilidad de componentes de observabilidad.

### Logs

Los registros se consultan mediante los logs generados por el backend y los contenedores Docker.

El proyecto **no utiliza Grafana Loki** actualmente.

Para consultar logs:

```powershell
docker compose logs
```

o seguirlos en tiempo real:

```powershell
docker compose logs -f
```

---

## Estructura del proyecto

```text
G19X-TESE-EADM-215-ACADEMIC/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── database.py
│   │   │   ├── security.py
│   │   │   └── telemetry.py
│   │   ├── models/
│   │   │   └── document.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   └── documents.py
│   │   ├── services/
│   │   │   └── ai_service.py
│   │   ├── config.py
│   │   └── main.py
│   ├── .env.example
│   ├── create_tables.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── DocumentRow.jsx
│   │   ├── pages/
│   │   │   ├── Archive.jsx
│   │   │   ├── Documents.jsx
│   │   │   └── Login.jsx
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── authService.js
│   │   │   └── documentService.js
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── package-lock.json
│
├── observability/
│   ├── otel-collector-config.yaml
│   └── prometheus.yml
│
├── MarkDown/
│   ├── Documento_de_Arquitectura.md
│   ├── Documento_de_Requerimientos.md
│   ├── Evaluacion_Postimplementacion_Cierre.md
│   ├── MVP.md
│   ├── Manual_Tecnico.md
│   ├── Manual_Usuario.md
│   ├── PRD.md
│   ├── Plan_Capacitacion.md
│   ├── Plan_Mantenimiento.md
│   ├── Propuesta_Tecnica.md
│   ├── QA.md
│   └── SCRUM.md
│
├── .gitignore
└── docker-compose.yml
```

---

## Seguridad

LegalTech contempla diferentes medidas básicas de seguridad:

- Autenticación mediante Keycloak.
- Autorización basada en roles.
- Uso de tokens JWT.
- Validación de permisos en el backend.
- Separación de credenciales mediante variables de entorno.
- Exclusión de `.env` mediante `.gitignore`.
- Restricción de determinadas operaciones según el rol.
- La API Key de Claude no se almacena directamente en el código fuente.

> Nunca deben publicarse contraseñas, Client Secrets, tokens, API Keys ni archivos `.env` reales en el repositorio.

---

## Documentación

La documentación formal del proyecto se encuentra en el directorio:

```text
MarkDown/
```

Incluye:

- Documento de requerimientos.
- Propuesta técnica.
- Documento de arquitectura.
- MVP.
- PRD.
- Planificación SCRUM, backlog y sprints.
- Manual técnico.
- Manual de usuario.
- Reporte de pruebas QA.
- Plan de mantenimiento y soporte.
- Plan de capacitación y entrega.
- Evaluación post-implementación y cierre técnico.

---

## Estado del proyecto

**Estado actual:** MVP funcional.

Se han realizado pruebas funcionales correspondientes a los casos **QA-01 a QA-10**, incluyendo autenticación, permisos por rol, flujo documental, persistencia, observabilidad, archivo documental, reapertura, seguridad básica, reproducibilidad local y análisis documental mediante IA.

Los resultados y evidencias se encuentran documentados en:

```text
MarkDown/QA.md
```

La implementación de **CI/CD mediante GitHub Actions no forma parte del alcance actual** y queda considerada como posible mejora futura.

---

## Contexto académico

El proyecto LegalTech se desarrolla en **PluriOne** como parte de las actividades académicas realizadas durante la estancia del alumno en modalidad dual.

El proyecto busca aplicar conocimientos de desarrollo de software, bases de datos, sistemas distribuidos, seguridad, Inteligencia Artificial y observabilidad sobre un caso práctico de gestión documental.

---

## Autor

**Eliab Duran**  
Ingeniería en Sistemas Computacionales  
Tecnológico de Estudios Superiores de Ecatepec (TESE)

Proyecto desarrollado en **PluriOne**.