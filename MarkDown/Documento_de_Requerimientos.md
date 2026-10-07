# Documento de Requerimientos

## LegalTech --- Sistema de Observabilidad para Procesos Documentales

## 1. Introducción

Este documento especifica los requerimientos funcionales, no funcionales
y reglas de negocio del sistema LegalTech, correspondientes al estado
actual del proyecto tras el Sprint 1.

## 2. Propósito

Establecer de manera formal y trazable los requisitos que debe
satisfacer el sistema, sirviendo de base para el desarrollo, las pruebas
de calidad (QA-01 a QA-10, ya ejecutadas) y la evaluación académica del
proyecto.

## 3. Alcance

El presente documento cubre los requisitos relacionados con la gestión
del ciclo de vida documental, el control de acceso por roles, la
autenticación, la persistencia en base de datos única, la observabilidad
técnica y la integración con inteligencia artificial. No cubre
requisitos de CI/CD, pausados hasta nuevas indicaciones.

## 4. Descripción general

LegalTech es un sistema web de gestión documental con observabilidad
integrada, compuesto por un frontend en React.js + Vite y un backend en
FastAPI, con persistencia en SQL Server, autenticación mediante
Keycloak, análisis mediante Claude API y monitoreo mediante
OpenTelemetry, Prometheus y Grafana.

## 5. Actores

  -----------------------------------------------------------------------
  Actor                               Descripción
  ----------------------------------- -----------------------------------
  `usuario_documental`                Carga y consulta sus propios
                                      documentos

  `revisor_documental`                Revisa, comenta, corrige y gestiona
                                      el estado de los documentos

  `admin_documental`                  Aprueba, rechaza, elimina y
                                      administra el ciclo completo
                                      documental
  -----------------------------------------------------------------------

## 6. Requisitos funcionales

  -----------------------------------------------------------------------
  ID                      Requisito               Rol(es)
  ----------------------- ----------------------- -----------------------
  RF-01                   El sistema debe         Todos
                          permitir el login de    
                          usuarios mediante       
                          Keycloak.               

  RF-02                   El sistema debe         Usuario, Revisor, Admin
                          permitir subir          
                          documentos.             

  RF-03                   El sistema debe         Usuario
                          permitir a              
                          `usuario_documental`    
                          consultar sus propios   
                          documentos.             

  RF-04                   El sistema debe         Usuario
                          permitir consultar el   
                          estado de un documento. 

  RF-05                   El sistema debe         Revisor
                          permitir a              
                          `revisor_documental`    
                          consultar documentos.   

  RF-06                   El sistema debe         Revisor
                          permitir iniciar la     
                          revisión de un          
                          documento.              

  RF-07                   El sistema debe         Revisor
                          permitir agregar        
                          comentarios a un        
                          documento.              

  RF-08                   El sistema debe         Revisor
                          permitir marcar un      
                          documento como          
                          revisado.               

  RF-09                   El sistema debe         Revisor
                          permitir solicitar      
                          corrección de un        
                          documento.              

  RF-10                   El sistema debe         Revisor, Admin
                          permitir descargar      
                          documentos.             

  RF-11                   El sistema debe         Revisor, Admin
                          permitir el acceso a    
                          documentos              
                          aprobados/rechazados.   

  RF-12                   El sistema debe         Revisor, Admin
                          permitir volver         
                          documentos finalizados  
                          a revisión.             

  RF-13                   El sistema debe         Admin
                          permitir a              
                          `admin_documental`      
                          consultar documentos.   

  RF-14                   El sistema debe         Admin
                          permitir aprobar un     
                          documento.              

  RF-15                   El sistema debe         Admin
                          permitir rechazar un    
                          documento.              

  RF-16                   El sistema debe         Admin
                          permitir eliminar       
                          documentos según        
                          permisos.               

  RF-17                   El sistema debe         Sistema
                          registrar el estado del 
                          documento conforme al   
                          flujo definido          
                          (`recibido`,            
                          `en_revision`,          
                          `revisado`, `aprobado`, 
                          `rechazado`,            
                          `correccion`).          

  RF-18                   El sistema debe         Sistema
                          permitir análisis de    
                          documentos mediante     
                          Claude API.             
  -----------------------------------------------------------------------

## 7. Requisitos no funcionales

  -----------------------------------------------------------------------
  ID                                  Requisito
  ----------------------------------- -----------------------------------
  RNF-01                              El sistema debe autenticar usuarios
                                      mediante JWT emitido por Keycloak.

  RNF-02                              El backend debe exponer una API
                                      REST desarrollada en FastAPI.

  RNF-03                              La persistencia debe realizarse en
                                      una única base de datos SQL Server
                                      (`observabilidad_documental`).

  RNF-04                              El sistema debe emitir telemetría
                                      mediante OpenTelemetry hacia un
                                      OpenTelemetry Collector.

  RNF-05                              Las métricas del sistema deben
                                      almacenarse en Prometheus y
                                      visualizarse en Grafana.

  RNF-06                              Todos los componentes deben poder
                                      desplegarse mediante Docker Compose
                                      de forma reproducible.

  RNF-07                              El sistema debe mantener logs de
                                      backend y contenedores disponibles
                                      para diagnóstico.
  -----------------------------------------------------------------------

## 8. Reglas de negocio

  -----------------------------------------------------------------------
  ID                                  Regla de negocio
  ----------------------------------- -----------------------------------
  RN-01                               Un documento solo puede pasar de
                                      `en_revision` a `revisado`,
                                      `aprobado` o `rechazado` según la
                                      acción del revisor o admin
                                      correspondiente.

  RN-02                               Un documento en estado `correccion`
                                      solo puede retornar a
                                      `en_revision`.

  RN-03                               Solo `revisor_documental` y
                                      `admin_documental` pueden reabrir
                                      un documento finalizado (`aprobado`
                                      o `rechazado`) hacia `en_revision`.

  RN-04                               Solo `admin_documental` puede
                                      aprobar, rechazar o eliminar
                                      documentos según permisos.

  RN-05                               Un documento no puede almacenarse
                                      fuera de la base de datos
                                      `observabilidad_documental` (no
                                      existe enrutamiento a bases
                                      diferenciadas).
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

## 10. Flujo de estados

**Flujo principal:**
`recibido → en_revision → revisado → aprobado / rechazado`

**Flujo de corrección:** `en_revision → correccion → en_revision`

**Flujo de reapertura:** `aprobado / rechazado → en_revision`

## 11. Restricciones técnicas

-   Única base de datos SQL Server (`observabilidad_documental`); no se
    utiliza PostgreSQL.
-   No existe enrutamiento de documentos hacia diferentes bases de datos
    ni arquitectura de shards.
-   Los logs corresponden a backend y contenedores; no se implementa
    Grafana Loki.
-   Despliegue exclusivamente mediante Docker Compose.

## 12. Criterios generales de aceptación

-   Cada requisito funcional debe ser verificable mediante al menos un
    caso de prueba QA.
-   El flujo documental debe respetar estrictamente las transiciones de
    estado definidas.
-   El acceso a cada funcionalidad debe corresponder exactamente al rol
    autorizado.
-   Las métricas de observabilidad deben ser visibles en Grafana tras
    cada operación relevante.

## 13. Matriz resumida de requisitos

  Categoría                           Cantidad
  --------------------------------- ----------
  Requisitos funcionales (RF)               18
  Requisitos no funcionales (RNF)            7
  Reglas de negocio (RN)                     5
  Roles definidos                            3

## 14. Conclusión

El conjunto de requisitos documentado refleja fielmente el estado
funcional actual de LegalTech, validado mediante el ciclo de pruebas
QA-01 a QA-10 (10 aprobadas, 0 fallidas, 0 pendientes, sin incidencias
bloqueantes), constituyendo una base sólida para las siguientes etapas
del proyecto.
