# Propuesta Técnica

## LegalTech --- Sistema de Observabilidad para Procesos Documentales

## 1. Introducción

El presente documento describe la propuesta técnica del sistema
LegalTech, una plataforma orientada a la observabilidad de procesos
documentales dentro de un flujo de revisión y aprobación. El sistema
integra un frontend en React.js, un backend en FastAPI, persistencia en
SQL Server, autenticación centralizada mediante Keycloak, análisis
asistido por inteligencia artificial mediante Claude API, y un stack de
observabilidad basado en OpenTelemetry, Prometheus y Grafana.

## 2. Planteamiento del problema

Los procesos de gestión documental que involucran múltiples roles
(carga, revisión, aprobación) suelen carecer de mecanismos de
trazabilidad y monitoreo que permitan identificar cuellos de botella,
medir tiempos de respuesta por etapa y detectar fallos operativos u
observabilidad técnica de los servicios involucrados. LegalTech busca
resolver esta carencia mediante un sistema documental instrumentado
end-to-end.

## 3. Objetivo general

Desarrollar un sistema de gestión y observabilidad de procesos
documentales que permita a los usuarios cargar, revisar, aprobar o
rechazar documentos, con trazabilidad completa del flujo y monitoreo
técnico de la infraestructura mediante herramientas de observabilidad.

## 4. Objetivos específicos

-   Implementar un flujo documental con estados definidos (`recibido`,
    `en_revision`, `revisado`, `aprobado`, `rechazado`, `correccion`).
-   Definir y aplicar un modelo de roles y permisos diferenciados
    (usuario, revisor, admin).
-   Centralizar la autenticación mediante Keycloak con JWT.
-   Persistir la información documental en una base de datos SQL Server
    única.
-   Instrumentar frontend y backend con OpenTelemetry para
    observabilidad distribuida.
-   Exponer métricas mediante Prometheus y visualizarlas en dashboards
    de Grafana.
-   Integrar análisis de documentos mediante Claude API.
-   Contenerizar y orquestar todos los componentes mediante Docker
    Compose.

## 5. Alcance

El alcance del proyecto cubre el ciclo completo de un documento desde su
carga hasta su aprobación o rechazo, incluyendo reapertura de documentos
finalizados, el control de acceso basado en roles, la observabilidad
técnica de los servicios (métricas, trazas y logs de
backend/contenedores) y la integración con un servicio de IA para
análisis documental. No incluye la automatización de CI/CD, la cual
queda pausada hasta nuevas indicaciones.

## 6. Solución propuesta

La solución propuesta consiste en una aplicación web compuesta por un
frontend en React.js + Vite que consume una API REST construida en
FastAPI. La persistencia se realiza en una única base de datos SQL
Server (`observabilidad_documental`) mediante el ORM SQLAlchemy. La
autenticación de usuarios se delega a Keycloak mediante el protocolo
JWT. El sistema incorpora instrumentación de observabilidad mediante
OpenTelemetry, cuyos datos son recolectados por un OpenTelemetry
Collector, expuestos como métricas en Prometheus y visualizados en
Grafana. El análisis inteligente de documentos se realiza mediante
llamadas a la Claude API. Todo el conjunto de servicios se despliega
mediante Docker Compose.

## 7. Arquitectura tecnológica

La arquitectura sigue un modelo de tres capas (frontend, backend, base
de datos) con servicios transversales de autenticación, observabilidad e
inteligencia artificial. La comunicación entre frontend y backend se
realiza vía API REST; el backend centraliza el acceso a la base de datos
y a los servicios externos (Keycloak, Claude API). Ver diagrama de
arquitectura adjunto.

## 8. Tecnologías utilizadas

  -----------------------------------------------------------------------
  Capa                                Tecnología
  ----------------------------------- -----------------------------------
  Frontend                            React.js + Vite

  Backend                             Python + FastAPI

  ORM                                 SQLAlchemy

  Autenticación                       Keycloak + JWT

  Base de datos                       SQL Server Developer Edition
                                      (`observabilidad_documental`)

  Contenerización                     Docker / Docker Compose

  Observabilidad                      OpenTelemetry, OpenTelemetry
                                      Collector, Prometheus, Grafana

  Inteligencia artificial             Claude API

  Control de versiones                Git + GitHub
  -----------------------------------------------------------------------

## 9. Roles y permisos

  -----------------------------------------------------------------------
  Rol                                 Permisos principales
  ----------------------------------- -----------------------------------
  `usuario_documental`                Login, subir documentos, consultar
                                      propios documentos, consultar
                                      estado

  `revisor_documental`                Login, subir, consultar, iniciar
                                      revisión, comentar, marcar
                                      revisado, solicitar corrección,
                                      descargar, ver
                                      aprobados/rechazados, reabrir
                                      finalizados

  `admin_documental`                  Login, subir, consultar, aprobar,
                                      rechazar, descargar, ver
                                      aprobados/rechazados, reabrir
                                      finalizados, eliminar según
                                      permisos
  -----------------------------------------------------------------------

## 10. Flujo documental

**Flujo principal:**
`recibido → en_revision → revisado → aprobado / rechazado`

**Flujo de corrección:** `en_revision → correccion → en_revision`

**Flujo de reapertura:** `aprobado / rechazado → en_revision` (ejecutado
por revisor o admin según permisos).

## 11. Base de datos

El sistema utiliza una única base de datos SQL Server Developer Edition
denominada `observabilidad_documental`. El diseño inicial contemplaba 4
shards SQL Server separados por categoría documental; dicho diseño fue
descartado. Las categorías documentales pueden mantenerse a nivel
funcional, pero no determinan la base de datos de almacenamiento.

## 12. Seguridad

La autenticación se gestiona mediante Keycloak, emitiendo tokens JWT que
son validados por el backend en cada solicitud. El control de acceso se
aplica a nivel de rol (`usuario_documental`, `revisor_documental`,
`admin_documental`), restringiendo las operaciones disponibles según el
perfil autenticado.

## 13. Observabilidad

La observabilidad del sistema se sustenta en OpenTelemetry para la
instrumentación de frontend y backend, un OpenTelemetry Collector para
la recepción y procesamiento de la telemetría, Prometheus para el
almacenamiento de métricas y Grafana para la construcción de dashboards
y alertas. Los logs corresponden a backend y contenedores; no se
documenta Grafana Loki como componente implementado.

## 14. Inteligencia artificial

El sistema integra la Claude API para el análisis de documentos,
proporcionando capacidades de procesamiento inteligente sobre el
contenido documental cargado.

## 15. Docker y despliegue local

Todos los servicios (frontend, backend, base de datos, Keycloak,
OpenTelemetry Collector, Prometheus, Grafana) se orquestan mediante
Docker Compose, permitiendo un despliegue local reproducible.

## 16. Beneficios de la solución

-   Trazabilidad completa del ciclo de vida documental.
-   Separación clara de responsabilidades por rol.
-   Observabilidad técnica en tiempo real de los servicios.
-   Simplificación del modelo de datos al usar una única base de datos.
-   Capacidad de análisis inteligente mediante IA.

## 17. Limitaciones / fuera de alcance

-   Automatización de GitHub Actions / CI-CD (pausada).
-   Enrutamiento de documentos a bases de datos diferenciadas
    (arquitectura de shards descartada).
-   Persistencia centralizada de logs mediante Grafana Loki (no
    implementada).

## 18. Resultados esperados

Se espera contar con un sistema funcional que permita gestionar el ciclo
completo de revisión documental, con observabilidad técnica activa y
trazabilidad de métricas, validado mediante las pruebas QA-01 a QA-10,
todas aprobadas sin incidencias bloqueantes.

## 19. Conclusión

La propuesta técnica de LegalTech consolida un sistema de gestión
documental observable, con arquitectura simplificada (base de datos
única), roles bien definidos y una capa de observabilidad e inteligencia
artificial que aporta valor diferencial frente a soluciones documentales
tradicionales.
