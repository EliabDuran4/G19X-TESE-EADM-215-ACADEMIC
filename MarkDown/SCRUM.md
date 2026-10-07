# Sistema de Observabilidad para Procesos Documentales — SCRUM.md

## Product Goal
Entregar un sistema de gestión documental jurídica con trazabilidad completa del proceso
(carga → revisión → decisión final), control de acceso por rol, base de datos distribuida
por categoría, y observabilidad end-to-end (logs, métricas, trazas, alertas), reproducible
íntegramente vía Docker, dentro del periodo 31 ago - 2 oct.

## Épicas
- EP1 Autenticación y Roles
- EP2 Gestión Documental y Sharding
- EP3 Flujo de Revisión/Aprobación
- EP4 Frontend
- EP5 Observabilidad
- EP6 Inteligencia Artificial
- EP7 CI/CD
- EP8 Documentación y QA

## Product Backlog

Nota: HU01 se conserva en esta tabla como registro histórico de alcance, pero es trabajo
cerrado en Sprint 0 — no forma parte del backlog activo pendiente de ejecución.

| ID | Épica | Historia | Prioridad | SP | Dependencias | Estado |
|---|---|---|---|---|---|---|
| HU01 | EP1 | Como usuario del sistema, quiero iniciar sesión con mi rol, para acceder solo a lo que me corresponde | Alta | 5 | — | Hecho — cerrado en Sprint 0, fuera del backlog activo |
| HU02 | EP2 | Como usuario documental, quiero subir un documento eligiendo su categoría, para que se almacene en el shard correcto | Alta | 8 | HU01 | Hecho |
| HU03 | EP2 | Como revisor/admin, quiero ver el listado de documentos consolidando los 4 shards, para tener visión completa | Alta | 5 | HU02 | Hecho |
| HU04 | EP1/EP2 | Como usuario documental, quiero ver solo mis propios documentos, para no acceder a información ajena | Alta | 5 | HU03 | Hecho |
| HU05 | EP3 | Como revisor documental, quiero comentar un documento y moverlo a revisado o corrección, para filtrar antes de la decisión final | Alta | 8 | HU03 | Hecho |
| HU06 | EP3 | Como admin documental, quiero aprobar o rechazar un documento en revisión, para dar la decisión final | Alta | 5 | HU05 | Hecho |
| HU07 | EP3 | Como sistema, quiero que un documento aprobado quede de solo lectura, para preservar integridad | Media | 3 | HU06 | Hecho |
| HU08 | EP4 | Como usuario, quiero una interfaz web para autenticarme y subir documentos | Alta | 8 | HU01,HU02 | Hecho |
| HU09a | EP4 | Como revisor/admin, quiero ver el listado de documentos desde la interfaz | Alta | 5 | HU03,HU04 | Hecho |
| HU09b | EP4 | Como revisor/admin, quiero ejecutar acciones de revisión/aprobación desde la interfaz | Alta | 5 | HU05,HU06 | Hecho |
| HU10 | EP5 | Como sistema, quiero generar trazas distribuidas de cada operación, para auditar el flujo | Alta | 8 | HU02 | Hecho |
| HU11 | EP5 | Como sistema, quiero exponer métricas de uso y rendimiento, para monitorear salud del sistema | Alta | 5 | HU10 | Hecho |
| HU12 | EP5 | Como admin, quiero ver dashboards en Grafana, para observar el sistema visualmente | Alta | 5 | HU11 | Hecho |
| HU13 | EP5 | Como admin, quiero recibir alertas ante fallos, para reaccionar a tiempo | Media | 3 | HU12 | Hecho |
| HU14 | EP6 | Como revisor, quiero un análisis de IA del documento, para apoyar la decisión | Media | 5 | HU02 | Hecho |
| HU15 | EP6 | Como admin, quiero detectar anomalías en el flujo vía IA, para anticipar problemas | Baja | 5 | HU14,HU03 | Backlog abierto (sin fecha fija) |
| HU16 | EP7 | Como equipo técnico, quiero un workflow de validación automática en cada push, para detectar errores temprano | Baja | 5 | HU08 | Hecho |
| HU17 | EP8 | Como usuario final, quiero manuales técnico y de usuario, para operar el sistema | Media | 5 | Documentará las funcionalidades realmente implementadas de HU02-HU14 y HU16 al cierre del Sprint 2, sin esperar a que absolutamente todo el backlog esté cerrado | Hecho|
| HU18 | EP8 | Como equipo técnico, quiero un reporte de pruebas QA, para validar el sistema antes de entrega | Alta | 5 | HU08,HU09a,HU09b,HU10-14 | Hecho |

## Definition of Done
- Código funciona sin errores en entorno Docker local
- Probado con al menos 1 caso de éxito y 1 caso de error
- Sin credenciales ni secretos hardcodeados (usa `.env`)
- Respeta el rol/permiso correspondiente si aplica control de acceso
- Cambios reflejados en el repositorio (commit)

---

## Sprint 0 — Fundacional (31 ago - 17 sep) — CERRADO
Sin ceremonias Scrum formales (planeación adoptada después de este periodo).

**Alcance cerrado:**
- Etapas 1-4 del proyecto: requerimientos, propuesta técnica, arquitectura (+ diagramas), planificación operativa
- Arranque técnico de Etapa 5: Keycloak (realm, client, 3 roles, usuarios de prueba, login funcional), backend base FastAPI, `security.py`/`auth.py`, 4 shards SQL Server Developer en Docker con base y tabla `documents` creada y verificada, `database.py` con enrutamiento por categoría

---

## Sprint 1 (18-24 sep)
**Sprint Goal:** Gestión documental multi-shard con control de acceso operando end-to-end.

**Historias:** HU02, HU03, HU04, HU05, HU06, HU07 — 34 SP

**Sprint Backlog (tareas técnicas):**
- Confirmar y cerrar endpoint de carga (HU02)
- Query consolidada de los 4 shards (HU03)
- Filtro de visibilidad por rol en el listado (HU04)
- Endpoints de revisión: comentario + transición de estado (HU05)
- Endpoints de aprobación/rechazo con `require_role("admin_documental")` (HU06)
- Bloqueo de edición en documentos con estado `aprobado` (HU07)

**Resultado:** *(pendiente de completar al cierre del sprint)*

---

## Sprint 2 (25 sep - 1 oct)
**Sprint Goal:** Sistema completo, observable, documentado y probado.

**Historias:** HU08, HU09a, HU09b, HU10, HU11, HU12, HU13, HU14, HU16, HU17, HU18 — 44 SP

**Regla de priorización ante restricción de tiempo:** el orden de protección es (1) funcionalidad
principal (HU08, HU09a, HU09b), (2) observabilidad básica (HU10, HU11, HU12), (3) QA (HU18) y
documentación (HU17). HU13, HU14 y HU16 tienen menor prioridad ante una restricción de tiempo,
sin que esto implique eliminarlas ni modificar su alcance dentro del Product Backlog.

**Sprint Backlog (tareas técnicas):**
- Frontend: login + upload (HU08)
- Frontend: listado de documentos (HU09a)
- Frontend: acciones de revisión/aprobación por rol (HU09b)
- OpenTelemetry SDK integrado en backend (HU10)
- Exportación de métricas a Prometheus (HU11)
- Dashboard en Grafana con datos reales (HU12)
- 1 regla de alerta configurada y probada (HU13)
- Endpoint de análisis con Claude API (HU14)
- 1 workflow de GitHub Actions validando backend y frontend (HU16)
- Manual técnico y manual de usuario (HU17)
- Ejecución y registro de casos de prueba QA (HU18)

**Resultado:** *(pendiente de completar al cierre del sprint)*

---

## Sprint 3 — Cierre (2 oct)
Sin desarrollo nuevo.

**Entregables:**
- Plan de Mantenimiento (documento)
- Manual de Usuario (reutilizado de HU17 como material de capacitación)
- Informe Final (HU completadas vs backlog original, lecciones aprendidas, comparación resultado esperado vs obtenido)

---

## Backlog abierto (sin sprint fijo)
- HU15 — Detección de anomalías vía IA (5 SP) — sin fecha comprometida; podrá seleccionarse
posteriormente si existe capacidad disponible y no compromete el Sprint Goal ni la entrega.

---

## Eventos Scrum (adaptados a trabajo individual)

| Evento | Cómo se maneja | Evidencia generada |
|---|---|---|
| Sprint Planning | Al inicio de cada sprint, se fija el Sprint Goal y se seleccionan las HU de este documento | Este archivo + confirmación registrada en la bitácora |
| Daily Scrum | Nota corta diaria: qué avancé, qué sigue, qué bloquea | Bitácora (sección siguiente) + historial de commits |
| Sprint Review | Demo personal al final del sprint contra el Sprint Goal | Resultado registrado en la sección del sprint + checklist de HU cerradas |
| Sprint Retrospective | Autoevaluación breve: qué funcionó, qué no, qué cambiar | Nota de cierre en la bitácora |

---

## Estructura de seguimiento — GitHub Projects
Columnas: Product Backlog → Sprint Backlog → To Do → In Progress → Review/Testing → Done.
Cada HU como tarjeta (issue), etiquetada por épica y por sprint. Vista adicional "Roadmap"
agrupando por Sprint 1 / Sprint 2 con fechas.