# PRD — Product Requirements Document

## LegalTech — Sistema de Observabilidad para Procesos Documentales

## 1. Objetivo del producto

Desarrollar un sistema web para gestionar y supervisar el ciclo de vida de documentos legales, desde su carga hasta su revisión, aprobación o rechazo.

LegalTech incorpora autenticación y autorización basada en roles, almacenamiento mediante SQL Server y herramientas de observabilidad para supervisar el comportamiento del sistema.


## 2. Usuarios y roles

### Usuario documental
`usuario_documental`

Puede:
- Iniciar sesión.
- Subir documentos.
- Consultar sus documentos.
- Consultar su estado.

No puede realizar operaciones de revisión o administración.

### Revisor documental
`revisor_documental`

Puede:
- Subir y consultar documentos.
- Descargar documentos.
- Iniciar revisiones.
- Agregar comentarios.
- Marcar documentos como revisados.
- Solicitar correcciones.
- Consultar Aprobados/Rechazados.
- Volver a colocar documentos finalizados en revisión.

No puede aprobar o rechazar definitivamente.

### Administrador documental
`admin_documental`

Puede:
- Subir y consultar documentos.
- Descargar documentos.
- Aprobar documentos.
- Rechazar documentos.
- Consultar Aprobados/Rechazados.
- Volver a colocar documentos finalizados en revisión.
- Eliminar documentos según los permisos establecidos.


## 3. Requisitos funcionales

### RF-01 — Autenticación
El sistema debe autenticar usuarios mediante Keycloak.

### RF-02 — Autorización
Los endpoints protegidos deben validar el token JWT y los roles correspondientes.

### RF-03 — Carga
El sistema debe permitir cargar documentos y seleccionar una categoría.

El estado inicial será:

`recibido`

### RF-04 — Consulta
Los documentos visibles deben determinarse según los permisos del usuario.

### RF-05 — Revisión
El Revisor podrá realizar:

`recibido → en_revision`

`en_revision → revisado`

`en_revision → correccion`

### RF-06 — Corrección
El sistema permitirá:

`correccion → en_revision`

### RF-07 — Decisión administrativa
El Administrador podrá realizar:

`revisado → aprobado`

`revisado → rechazado`

### RF-08 — Comentarios
El sistema permitirá registrar comentarios durante el proceso de revisión.

### RF-09 — Archivo documental
Revisor y Administrador podrán consultar documentos:

- Aprobados.
- Rechazados.

### RF-10 — Descarga
Revisor y Administrador podrán descargar documentos autorizados.

### RF-11 — Reapertura
Se permitirá:

`aprobado → en_revision`

`rechazado → en_revision`

### RF-12 — Eliminación
Los documentos podrán eliminarse de acuerdo con los permisos establecidos.

### RF-13 — Inteligencia Artificial
El sistema dispondrá de integración con Claude API para análisis mediante IA.

**Estado:** implementado, pendiente de prueba en vivo por disponibilidad de créditos.

### RF-14 — Observabilidad
El backend deberá proporcionar información de observabilidad mediante métricas, trazas y logs.

### RF-15 — Dashboard
Grafana permitirá visualizar las métricas recopiladas.

### RF-16 — Alertas
Grafana permitirá configurar alertas relacionadas con el comportamiento del sistema.


## 4. Flujo documental

Flujo principal:

`recibido → en_revision → revisado → aprobado/rechazado`

Corrección:

`en_revision → correccion → en_revision`

Reapertura:

`aprobado/rechazado → en_revision`


## 5. Requisitos no funcionales

### RNF-01 — Seguridad
Autenticación mediante Keycloak y tokens JWT.

### RNF-02 — Control de acceso
Los permisos deben validarse en backend y no depender únicamente de la interfaz.

### RNF-03 — Persistencia
La información debe almacenarse mediante SQL Server.

### RNF-04 — Reproducibilidad
Los componentes deben poder ejecutarse localmente mediante Docker Compose.

### RNF-05 — Observabilidad
El backend debe estar instrumentado mediante OpenTelemetry.

### RNF-06 — Métricas
Prometheus debe recolectar las métricas disponibles.

### RNF-07 — Visualización
Grafana debe permitir visualizar las métricas.

### RNF-08 — Trazabilidad
Las operaciones relevantes deben generar información que facilite su supervisión y diagnóstico.


## 6. Arquitectura

| Componente | Tecnología |
|---|---|
| Frontend | React |
| Backend/API | FastAPI |
| Autenticación | Keycloak |
| Base de datos | SQL Server Developer Edition |
| ORM | SQLAlchemy |
| Instrumentación | OpenTelemetry |
| Collector | OpenTelemetry Collector |
| Métricas | Prometheus |
| Dashboards/alertas | Grafana |
| IA | Claude API |
| Contenedores | Docker / Docker Compose |

La arquitectura actual utiliza una única base de datos SQL Server.


## 7. Observabilidad

Flujo general:

`FastAPI → OpenTelemetry → OpenTelemetry Collector → Prometheus/Grafana`

La solución contempla:

- Trazas.
- Métricas.
- Logs.
- Dashboard Grafana.
- Alertas.


## 8. Alcance

El producto contempla:

- Autenticación y autorización.
- Tres roles.
- Gestión documental.
- Categorías.
- Revisión.
- Comentarios.
- Correcciones.
- Aprobación/rechazo.
- Archivo de documentos finalizados.
- Descarga.
- Reapertura.
- Eliminación según permisos.
- SQL Server.
- Observabilidad.
- Integración con IA.
- Docker Compose.


## 9. Fuera de alcance

- Versionado de documentos.
- Notificaciones por correo.
- Búsqueda full-text.
- Gestión avanzada de clientes/expedientes.
- Arquitectura de cuatro shards.
- Multi-tenancy.
- Despliegue productivo en cloud.
- Integraciones empresariales externas.


## 10. Criterios de aceptación

El producto deberá permitir:

1. Autenticación correcta de los tres roles.
2. Aplicación de permisos según rol.
3. Carga de documentos.
4. Ejecución correcta del flujo documental.
5. Revisión y comentarios.
6. Aprobación/rechazo.
7. Consulta de documentos finalizados.
8. Descarga y reapertura según permisos.
9. Protección de endpoints.
10. Persistencia en SQL Server.
11. Generación de telemetría.
12. Consulta de métricas en Prometheus.
13. Visualización mediante Grafana.


## 11. Estado actual

El sistema se encuentra implementado y en etapa de validación QA y documentación.

### QA confirmado

- QA-01 — Permisos Usuario: **APROBADO**
- QA-02 — Permisos Revisor: **APROBADO**

### Pendiente

- QA del Administrador.
- Transiciones inválidas.
- Casos límite.
- Validaciones finales de observabilidad.
- Prueba en vivo del módulo IA.
- Resto del plan QA.