# Documento de Arquitectura

## LegalTech --- Sistema de Observabilidad para Procesos Documentales

## 1. Introducción

Este documento describe la arquitectura técnica actual del sistema
LegalTech, detallando sus componentes, la interacción entre ellos y las
decisiones de diseño vigentes al cierre del Sprint 1.

## 2. Objetivo

Documentar de forma clara y verificable la arquitectura de software e
infraestructura implementada, sirviendo como referencia técnica para el
desarrollo, mantenimiento y evaluación académica del proyecto.

## 3. Arquitectura general

El sistema sigue el flujo:

`Usuario → React.js + Vite (frontend) → FastAPI (backend) → SQL Server (base de datos única: observabilidad_documental)`

De forma transversal, el backend se integra con Keycloak
(autenticación), Claude API (análisis IA) y el stack de observabilidad
(OpenTelemetry, OpenTelemetry Collector, Prometheus, Grafana). Todos los
servicios se orquestan mediante Docker Compose.

> **Diagrama del documento original:** La página 2 del PDF muestra la
> arquitectura general con Usuario, Frontend, Backend, SQL Server,
> Claude API, Keycloak, OpenTelemetry, OpenTelemetry Collector,
> Prometheus y Grafana dentro de la orquestación con Docker Compose.

## 4. Descripción de componentes

  Componente                Función
  ------------------------- ------------------------------------------------------
  React.js + Vite           Interfaz de usuario (frontend SPA)
  FastAPI                   API REST / lógica de negocio (backend)
  SQLAlchemy                ORM de acceso a datos
  SQL Server                Persistencia (BD única: `observabilidad_documental`)
  Keycloak                  Autenticación y emisión de JWT
  Claude API                Análisis de documentos mediante IA
  OpenTelemetry             Instrumentación de trazas y métricas
  OpenTelemetry Collector   Recepción y procesamiento de telemetría
  Prometheus                Almacenamiento y consulta de métricas
  Grafana                   Visualización y alertas
  Docker Compose            Orquestación de contenedores

## 5. Arquitectura frontend

El frontend está construido con React.js y empaquetado mediante Vite.
Consume la API REST expuesta por FastAPI y gestiona la autenticación de
usuario mediante el flujo de Keycloak, incorporando el token JWT en las
solicitudes al backend.

## 6. Arquitectura backend

El backend está desarrollado en Python con el framework FastAPI,
utilizando SQLAlchemy como ORM para el acceso a la base de datos SQL
Server. Expone endpoints REST consumidos por el frontend, valida tokens
JWT emitidos por Keycloak, invoca la Claude API para análisis documental
y emite telemetría mediante OpenTelemetry.

## 7. Arquitectura de autenticación

La autenticación se centraliza en Keycloak, que emite tokens JWT tras el
proceso de login. El frontend obtiene el token y lo adjunta en cada
solicitud al backend, el cual valida su vigencia y extrae el rol del
usuario (`usuario_documental`, `revisor_documental`, `admin_documental`)
para autorizar las operaciones correspondientes.

## 8. Arquitectura de datos

La persistencia se realiza en una única base de datos SQL Server
Developer Edition, denominada `observabilidad_documental`. El diseño
inicial contemplaba 4 shards SQL Server separados por categoría
documental; este diseño fue eliminado. La arquitectura de datos vigente
es:

`FastAPI → SQL Server (BD única)`

Las categorías documentales pueden existir a nivel funcional, sin
determinar la base de datos de almacenamiento. No se utiliza PostgreSQL.

## 9. Flujo documental

**Flujo principal:**
`recibido → en_revision → revisado → aprobado / rechazado`

**Flujo de corrección:** `en_revision → correccion → en_revision`

**Flujo de reapertura:** `aprobado / rechazado → en_revision`

> **Diagrama del documento original:** La página 4 del PDF representa el
> flujo documental dividido por Usuario, Revisor y Admin, incluyendo los
> estados `recibido`, `en_revision`, `revisado`, `correccion`,
> `aprobado` y `rechazado`.

## 10. Arquitectura de observabilidad

OpenTelemetry instrumenta frontend y backend para la generación de
trazas y métricas. Un OpenTelemetry Collector recibe y procesa dicha
telemetría. Prometheus almacena las métricas resultantes y Grafana las
visualiza mediante dashboards y alertas. Los logs corresponden al
backend y a los contenedores; no se ha implementado Grafana Loki.

## 11. Integración IA

El backend se integra con la Claude API para realizar análisis de
documentos mediante inteligencia artificial, como parte del flujo de
revisión documental.

## 12. Arquitectura Docker

Todos los componentes del sistema (frontend, backend, base de datos,
Keycloak, OpenTelemetry Collector, Prometheus, Grafana) se despliegan y
orquestan mediante Docker Compose, garantizando reproducibilidad del
entorno local.

## 13. Seguridad

El control de acceso se basa en JWT emitidos por Keycloak y en la
verificación de rol en cada endpoint del backend, restringiendo las
operaciones según el perfil (usuario, revisor, admin).

## 14. Persistencia

La persistencia de la información documental y de estado se realiza
íntegramente en la base de datos SQL Server `observabilidad_documental`,
validada mediante pruebas de persistencia y reproducibilidad local
dentro del ciclo QA.

## 15. Control de versiones

El proyecto utiliza Git como sistema de control de versiones, con
repositorio alojado en GitHub. El Sprint 1 fue registrado mediante
commit y el código fue subido correctamente a la rama `main`.

## 16. Consideraciones de mantenimiento

-   Mantener actualizada la instrumentación de OpenTelemetry ante
    cambios en endpoints del backend.
-   Versionar cambios en el esquema de la base de datos
    `observabilidad_documental`.
-   Revisar periódicamente los dashboards de Grafana para asegurar
    cobertura de métricas relevantes.
-   Evaluar la reactivación de GitHub Actions / CI-CD cuando el proyecto
    lo requiera.

## 17. Conclusión

La arquitectura actual de LegalTech consolida un diseño simplificado
respecto a la propuesta inicial, al reemplazar el esquema de 4 shards
por una base de datos única, manteniendo la observabilidad y la
integración de IA como pilares diferenciales del sistema.
