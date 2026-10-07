# Plan de Mantenimiento y Soporte

**LegalTech — Sistema de Observabilidad para Procesos Documentales**

## 1. Introducción

Este documento define el plan de mantenimiento y soporte del sistema LegalTech, estableciendo actividades preventivas, correctivas y evolutivas, así como el esquema de soporte multinivel aplicable durante la etapa académica del proyecto.

## 2. Objetivo

Establecer los lineamientos de mantenimiento y soporte necesarios para garantizar la disponibilidad y correcto funcionamiento del sistema LegalTech.

## 3. Alcance

Cubre el mantenimiento de los componentes desplegados mediante Docker Compose (frontend, backend, base de datos, Keycloak, observabilidad), así como el esquema de soporte para incidencias reportadas durante la operación del sistema.

## 4. Mantenimiento preventivo

- Revisión periódica del estado de los contenedores Docker.
- Monitoreo de métricas en Grafana para detectar anomalías antes de que se conviertan en fallas.
- Verificación periódica de espacio en disco y recursos de la base de datos.

## 5. Mantenimiento correctivo

- Corrección de errores identificados en backend, frontend o configuración de servicios.
- Resolución de incidencias reportadas por los usuarios según el esquema de soporte multinivel.

## 6. Mantenimiento evolutivo

- Incorporación de mejoras funcionales fuera del alcance del MVP actual.
- Evaluación futura de automatización CI/CD cuando se reciban indicaciones.

## 7. Frecuencia recomendada de mantenimiento

| Actividad | Frecuencia propuesta |
|---|---|
| Revisión de contenedores Docker | Semanal |
| Revisión de SQL Server | Semanal |
| Respaldo de base de datos | Semanal / antes de cambios relevantes |
| Revisión de Keycloak | Mensual |
| Revisión de Prometheus/Grafana | Mensual |
| Actualización de dependencias | Trimestral / según necesidad |

## 8. Revisión de Docker

Verificar periódicamente que todos los contenedores definidos en Docker Compose se encuentren en ejecución y sin reinicios inesperados, revisando logs cuando corresponda.

## 9. Revisión de SQL Server

Verificar el estado del servicio de base de datos, el uso de espacio y la integridad de la base observabilidad_documental.

## 10. Respaldos de la base de datos

Ejecutar respaldos periódicos de la base observabilidad_documental, almacenándolos en una ubicación segura. [POR CONFIRMAR: mecanismo y ubicación de respaldo]

## 11. Revisión de Keycloak

Verificar la correcta configuración del realm, clientes y roles (usuario_documental, revisor_documental, admin_documental), así como la vigencia de las credenciales de servicio.

## 12. Revisión de Prometheus/Grafana

Verificar que el OpenTelemetry Collector envíe correctamente las métricas a Prometheus y que los dashboards de Grafana reflejen el estado actual del sistema.

## 13. Actualización de dependencias

Actualizar de forma controlada las dependencias del backend (Python/FastAPI/SQLAlchemy) y del frontend (React/Vite), validando el correcto funcionamiento tras cada actualización.

## 14. Registro de incidencias

Toda incidencia debe registrarse indicando fecha, descripción, componente afectado, nivel de soporte asignado y estado de resolución. [POR CONFIRMAR: herramienta de registro de incidencias]

## 15. Soporte multinivel

### Nivel 1 — Soporte operativo/básico

Atiende consultas de uso general del sistema por parte de los usuarios.

### Nivel 2 — Soporte técnico/desarrollador

Atiende fallas técnicas de configuración y funcionamiento de los componentes del sistema.

### Nivel 3 — Desarrollo especializado

Atiende requerimientos de desarrollo especializado o cambios estructurales en la arquitectura.

Como el proyecto corresponde actualmente a un desarrollo académico individual, el mismo desarrollador puede asumir los roles de Nivel 2 y Nivel 3 durante esta etapa. El modelo de tres niveles representa el esquema previsto para una futura operación formal del sistema.

| Nivel | Responsable | Tipo de incidencia | Ejemplo | Escalamiento propuesto |
|---|---|---|---|---|
| Nivel 1 | Soporte operativo/básico [POR CONFIRMAR] | Consultas de uso, dudas operativas | Usuario no sabe cómo subir un documento | A Nivel 2 si no se resuelve en 24 h (tiempo propuesto, no SLA) |
| Nivel 2 | Desarrollador (asume el rol durante esta etapa académica) | Fallas técnicas, configuración, errores de backend/frontend | Error al iniciar sesión por configuración de Keycloak | A Nivel 3 si no se resuelve en 48 h (tiempo propuesto, no SLA) |
| Nivel 3 | Desarrollador (asume el rol durante esta etapa académica) | Desarrollo especializado, cambios estructurales | Ajuste del modelo de datos o de la arquitectura de observabilidad | No aplica escalamiento adicional |

Los tiempos de escalamiento indicados son tiempos propuestos para el esquema de soporte y no constituyen acuerdos de nivel de servicio (SLA) contractuales.

## 16. Estrategia de respaldo

Se recomienda mantener respaldos periódicos de la base de datos y del código fuente (mediante el repositorio Git/GitHub), asegurando la posibilidad de restaurar el sistema ante una falla mayor.

## 17. Recuperación básica

- Restaurar el último respaldo disponible de la base de datos observabilidad_documental.
- Reconstruir los contenedores mediante docker compose up -d --build.
- Verificar la integridad de los servicios mediante los dashboards de Grafana.

## 18. Conclusión

El presente plan establece las bases para el mantenimiento preventivo, correctivo y evolutivo del sistema LegalTech, así como un esquema de soporte multinivel adaptado a la etapa académica actual del proyecto, con proyección hacia una operación formal futura.