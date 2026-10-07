# MVP — Producto Mínimo Viable

## LegalTech — Sistema de Observabilidad para Procesos Documentales

## 1. Objetivo del MVP

Desarrollar una versión funcional de LegalTech que permita gestionar el flujo principal de documentos legales, desde su carga hasta su revisión, aprobación o rechazo, incorporando autenticación por roles y herramientas de observabilidad.

El MVP debe demostrar que el proceso documental puede ejecutarse correctamente y que las operaciones principales del sistema pueden ser supervisadas mediante métricas, trazas y dashboards.


## 2. Problema que resuelve

LegalTech busca solucionar la falta de trazabilidad y visibilidad operativa en procesos de gestión documental.

El sistema permite conocer quién cargó un documento, su estado actual, quién puede revisarlo y cuál fue su resolución final, además de proporcionar herramientas para observar técnicamente el funcionamiento de la aplicación.


## 3. Roles

El MVP contempla tres roles:

### Usuario documental
`usuario_documental`

Puede:
- Iniciar sesión.
- Subir documentos.
- Consultar sus propios documentos.
- Consultar el estado de sus documentos.

### Revisor documental
`revisor_documental`

Puede:
- Iniciar sesión.
- Subir documentos.
- Consultar documentos.
- Descargar documentos.
- Iniciar revisiones.
- Agregar comentarios.
- Marcar documentos como revisados.
- Solicitar correcciones.
- Consultar documentos aprobados/rechazados.
- Volver a colocar documentos finalizados en revisión.

### Administrador documental
`admin_documental`

Puede:
- Iniciar sesión.
- Subir documentos.
- Consultar documentos.
- Descargar documentos.
- Aprobar documentos.
- Rechazar documentos.
- Consultar documentos aprobados/rechazados.
- Volver a colocar documentos finalizados en revisión.
- Eliminar documentos según los permisos establecidos.


## 4. Funcionalidades incluidas

- Autenticación mediante Keycloak.
- Autorización basada en roles.
- Carga de documentos.
- Selección de categoría.
- Consulta de documentos según permisos.
- Flujo de revisión.
- Comentarios.
- Solicitud de correcciones.
- Aprobación y rechazo.
- Sección de documentos Aprobados/Rechazados.
- Descarga de documentos para Revisor/Admin.
- Reapertura de documentos finalizados.
- Eliminación según permisos.
- Persistencia mediante SQL Server.
- Instrumentación mediante OpenTelemetry.
- OpenTelemetry Collector.
- Métricas mediante Prometheus.
- Dashboard y alertas mediante Grafana.
- Ejecución mediante Docker Compose.
- Integración con Claude API para análisis mediante IA.


## 5. Flujo documental

Flujo principal:

`recibido → en_revision → revisado → aprobado/rechazado`

Flujo de corrección:

`en_revision → correccion → en_revision`

Reapertura:

`aprobado/rechazado → en_revision`


## 6. Arquitectura del MVP

El MVP utiliza:

- React — Frontend.
- FastAPI — Backend/API.
- Keycloak — Autenticación.
- SQL Server Developer Edition — Base de datos.
- SQLAlchemy — ORM.
- OpenTelemetry — Instrumentación.
- OpenTelemetry Collector — Procesamiento de telemetría.
- Prometheus — Métricas.
- Grafana — Dashboards y alertas.
- Claude API — Análisis mediante IA.
- Docker / Docker Compose — Contenedores y ejecución.

La versión actual utiliza una única base de datos SQL Server.

La arquitectura inicial de cuatro shards fue retirada del MVP actual.


## 7. Observabilidad

El MVP incluye:

- Trazas mediante OpenTelemetry.
- Collector de telemetría.
- Métricas de operaciones.
- Métricas de duración.
- Prometheus.
- Dashboard Grafana.
- Alertas Grafana.
- Logs del backend.


## 8. Inteligencia Artificial

El sistema incluye un módulo de análisis mediante Claude API.

**Estado:** implementado, pendiente de prueba en vivo por disponibilidad de créditos.


## 9. Fuera del MVP

Se consideran mejoras futuras:

- Versionado de documentos.
- Notificaciones por correo electrónico.
- Búsqueda full-text.
- Gestión avanzada de clientes y expedientes.
- Arquitectura distribuida mediante múltiples shards.
- Multi-tenancy.
- Despliegue productivo en cloud.
- Integraciones empresariales externas.


## 10. Criterio de aceptación del MVP

El MVP se considera funcional cuando los tres roles pueden realizar las operaciones correspondientes a sus permisos, el flujo documental puede completarse desde la carga hasta su resolución, los endpoints se encuentran protegidos y las operaciones principales pueden supervisarse mediante las herramientas de observabilidad.

El sistema se encuentra actualmente en etapa de pruebas QA y documentación final.