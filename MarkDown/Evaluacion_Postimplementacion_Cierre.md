# Evaluación Post-Implementación y Cierre Técnico

**LegalTech — Sistema de Observabilidad para Procesos Documentales**

*LegalTech — Sistema de Observabilidad para Procesos Documentales*

## 1. Introducción

Este documento presenta la evaluación post-implementación del sistema y formaliza el cierre técnico del MVP correspondiente a la etapa académica actual.

## 2. Objetivo

Evaluar el desempeño funcional y técnico del sistema LegalTech tras su implementación, con base en los resultados del ciclo de pruebas QA, y declarar el cierre técnico del MVP.

## 3. Alcance

Cubre la evaluación funcional, de roles y permisos, del flujo documental, de persistencia, seguridad, observabilidad, reproducibilidad local y del servicio de IA, con base en las pruebas QA-01 a QA-12 ya ejecutadas.

## 4. Metodología de evaluación

La evaluación se basa en los resultados del ciclo de pruebas QA-01 a QA-12, ejecutado sobre el sistema desplegado localmente mediante Docker Compose, contrastando cada resultado con los requisitos funcionales y no funcionales definidos para el proyecto.

## 5. Criterios de evaluación

- Cumplimiento funcional respecto a los requisitos definidos.
- Correcta aplicación de permisos por rol.
- Respeto de las transiciones del flujo documental.
- Persistencia correcta de la información en la base de datos.
- Validación de la autenticación y autorización.
- Disponibilidad de métricas de observabilidad.
- Reproducibilidad del entorno local.
- Correcto funcionamiento del servicio de análisis mediante IA.

## 6. Evaluación funcional

Las funcionalidades de carga, consulta, revisión, aprobación, rechazo, corrección, reapertura y eliminación de documentos fueron validadas mediante el ciclo QA, con resultado satisfactorio en la totalidad de los casos.

## 7. Evaluación de roles y permisos

Se validaron los permisos correspondientes a usuario_documental, revisor_documental y admin_documental, confirmando que cada rol accede únicamente a las funcionalidades autorizadas.

## 8. Evaluación del flujo documental

Se validó el cumplimiento del flujo principal (recibido → en_revision → revisado → aprobado/rechazado), el flujo de corrección (en_revision → correccion → en_revision) y el flujo de reapertura (aprobado/rechazado → en_revision).

## 9. Evaluación de persistencia

Se confirmó la correcta persistencia de la información documental y de sus estados en la base de datos única SQL Server observabilidad_documental.

## 10. Evaluación de seguridad y autorización

Se validó el funcionamiento de la autenticación mediante Keycloak y JWT, así como la correcta autorización de operaciones según el rol autenticado.

## 11. Evaluación de observabilidad

Se verificó la generación de telemetría mediante OpenTelemetry, su recepción por el OpenTelemetry Collector, su almacenamiento en Prometheus y su visualización en dashboards de Grafana, junto con la disponibilidad de logs de backend/contenedores.

## 12. Evaluación de reproducibilidad local

Se confirmó que el sistema completo puede desplegarse de forma reproducible mediante Docker Compose en un entorno local.

## 13. Evaluación del servicio de IA

Se validó el funcionamiento de la integración de IA para el análisis de documentos dentro del flujo del sistema (QA-10). Posteriormente se incorporó un proveedor de IA configurable (Claude API, Ollama local o desactivado, con respaldo opcional), validado mediante QA-11 y QA-12: manejo controlado de errores, análisis con y sin contenido del PDF, funcionamiento del respaldo, restricción por rol y no alteración del estado del documento.

El sistema continúa operando cuando la IA no está disponible. El proveedor local se validó con el modelo `qwen2.5:3b`, cuya respuesta es más lenta y menos precisa que la de Claude.

**Lecciones aprendidas:**

- Desacoplar el proveedor de IA mediante configuración evita depender de un único servicio, de sus créditos o de su disponibilidad.
- La IA debe limitarse a recomendaciones de apoyo, de modo que su falla no afecte el flujo documental.
- La descarga de modelos locales mediante contenedores puede fallar en redes que interceptan el tráfico HTTPS; la instalación nativa de Ollama es una alternativa viable.

## 14. Resultados QA

| Indicador | Resultado |
|---|---|
| Pruebas ejecutadas | QA-01 a QA-12 (12 pruebas) |
| Pruebas aprobadas | 12 (100 %) |
| Pruebas fallidas | 0 |
| Pruebas pendientes | 0 |
| Incidencias bloqueantes | 0 |

Se validaron los permisos de Usuario, Revisor y Admin; el flujo end-to-end; la observabilidad; los estados de Aprobados/Rechazados, reapertura y eliminación; la seguridad/autenticación; la persistencia; la reproducibilidad local; el servicio de IA y el proveedor de IA configurable.

## 15. Incidencias

No se registraron incidencias bloqueantes durante el ciclo de pruebas QA-01 a QA-12.

Incidencia no bloqueante: la descarga del modelo local de IA mediante el contenedor Docker falló por un error de certificado TLS de la red (`x509: certificate signed by unknown authority`). Se resolvió utilizando la instalación nativa de Ollama, sin cambios en el código del sistema.

## 16. Estado final del MVP

El MVP del sistema LegalTech se declara cerrado técnicamente para esta etapa académica, con base en el 100 % de aprobación del ciclo QA y la ausencia de incidencias bloqueantes.

## 17. Respaldo y continuidad

Se recomienda mantener respaldos periódicos de la base de datos y del repositorio de código como medida de continuidad, conforme a lo establecido en el Plan de Mantenimiento y Soporte.

## 18. Actividades futuras

- Automatización de CI/CD cuando se reciban indicaciones al respecto.
- Evaluación de un despliegue productivo futuro.
- Incorporación de mejoras funcionales fuera del alcance del MVP actual.
- Mantenimiento evolutivo continuo del sistema.
- Evaluación de modelos de IA locales de mayor capacidad, según el equipo disponible.

## 19. Aceptación académica

**Aceptación académica: pendiente de revisión/confirmación del profesor o asesor.**

## 20. Cierre técnico

Se declara el cierre técnico del MVP de LegalTech para esta etapa académica, con base en los resultados satisfactorios del ciclo de pruebas QA y la documentación técnica y de usuario generada.

## 21. Conclusión

La evaluación post-implementación confirma que el sistema LegalTech cumple con los requisitos funcionales y no funcionales definidos, alcanzando un cierre técnico satisfactorio del MVP para la presente etapa académica, quedando pendiente únicamente la aceptación formal por parte del profesor o asesor.