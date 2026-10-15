# Documentación QA Final — LegalTech

## Sistema de Observabilidad para Procesos Documentales

## 1. Objetivo

Validar el funcionamiento integral del Sistema de Observabilidad para Procesos Documentales, verificando el flujo documental, los permisos asociados a cada rol, la seguridad de los endpoints, la persistencia de datos y los componentes de observabilidad.

Las pruebas buscan comprobar que las funcionalidades implementadas cumplen con el comportamiento esperado antes del cierre técnico y entrega del sistema.


## 2. Alcance

Las pruebas QA cubren:

- Autenticación mediante Keycloak.
- Rol Usuario Documental.
- Rol Revisor Documental.
- Rol Administrador Documental.
- Carga y consulta de documentos.
- Flujo completo de revisión.
- Aprobación y rechazo.
- Correcciones.
- Descarga de documentos.
- Archivo de documentos aprobados y rechazados.
- Reapertura de documentos.
- Eliminación según permisos.
- Seguridad y autorización de endpoints.
- Persistencia mediante SQL Server.
- OpenTelemetry.
- OpenTelemetry Collector.
- Prometheus.
- Grafana.
- Ejecución local mediante Docker Compose.
- Integración del servicio de IA.
- Proveedor de IA configurable (Claude API, Ollama local o desactivado) y respaldo opcional.


## 3. Ambiente de pruebas

- **Sistema operativo:** Windows 11
- **Entorno:** Desarrollo local
- **Frontend:** React
- **Backend:** FastAPI
- **Autenticación:** Keycloak
- **Base de datos:** SQL Server (única base de datos)
- **ORM:** SQLAlchemy
- **Contenedores:** Docker / Docker Compose
- **Telemetría:** OpenTelemetry
- **Collector:** OpenTelemetry Collector
- **Métricas:** Prometheus
- **Visualización:** Grafana
- **IA:** Claude API (principal) y Ollama local con `qwen2.5:3b` (alternativa/respaldo)
- **Rama probada:** `main`


## 4. Casos de prueba

| ID | Caso | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|
| QA-01 | Permisos del Usuario | Usuario puede cargar y consultar sus documentos sin acceder a funciones de Revisor/Admin | Comportamiento conforme a los permisos establecidos | **Aprobado** |
| QA-02 | Permisos del Revisor | Revisor puede revisar, descargar y acceder al archivo sin realizar acciones exclusivas del Admin | Comportamiento conforme a los permisos establecidos | **Aprobado** |
| QA-03 | Permisos del Admin | Admin puede realizar las operaciones administrativas autorizadas | Operaciones administrativas ejecutadas correctamente | **Aprobado** |
| QA-04 | Flujo end-to-end | Documento completa correctamente su ciclo de vida | Flujo documental completado correctamente | **Aprobado** |
| QA-05 | Observabilidad | Operaciones generan información visible mediante las herramientas de observabilidad | Telemetría y métricas observadas correctamente | **Aprobado** |
| QA-06 | Archivado, reapertura y eliminación | Documentos finalizados pueden consultarse y gestionarse según permisos | Operaciones realizadas correctamente | **Aprobado** |
| QA-07 | Seguridad de autenticación | Operaciones protegidas rechazan accesos no autorizados | Restricciones de autenticación/autorización aplicadas correctamente | **Aprobado** |
| QA-08 | Persistencia de datos | La información permanece correctamente almacenada en SQL Server | Persistencia comprobada correctamente | **Aprobado** |
| QA-09 | Reproducibilidad local | Los componentes pueden ejecutarse correctamente en el entorno local | Sistema iniciado y operado correctamente | **Aprobado** |
| QA-10 | Servicio de IA | El servicio procesa correctamente la solicitud de análisis | Análisis realizado correctamente | **Aprobado** |
| QA-11 | IA multi-proveedor (servicio) | El servicio selecciona el proveedor configurado, controla los errores y usa el respaldo | Comportamiento esperado en todos los escenarios | **Aprobado** |
| QA-12 | IA desde la interfaz | El revisor y el admin usan la IA; el usuario no; el estado del documento no cambia | Comportamiento esperado | **Aprobado** |


## 5. Detalle de pruebas

### QA-01 — Permisos del Usuario

**Validaciones realizadas:**

- Inicio de sesión como `usuario_documental`.
- Carga de documento.
- Documento registrado con estado `recibido`.
- Visualización de documentos propios.
- Restricción de acceso a `/archive`.
- Ausencia de acciones exclusivas de Revisor/Admin.
- Acceso directo al endpoint `/documents/archive` rechazado.

**Evidencia HTTP obtenida:**

`403 Forbidden`

Respuesta:

`{"detail":"Se requiere el rol de revisor o administrador"}`

**Resultado:** Aprobado.


### QA-02 — Permisos del Revisor

**Validaciones realizadas:**

- Inicio de sesión como `revisor_documental`.
- Transición `recibido → en_revision`.
- Transición `en_revision → revisado`.
- Descarga de documentos.
- Acceso a documentos aprobados/rechazados.
- Reapertura de documentos.
- Restricción de acciones exclusivas del Administrador.
- Ausencia de Aprobar/Rechazar.
- Ausencia de Eliminar en las áreas restringidas al Admin.

**Resultado:** Aprobado.


### QA-03 — Permisos del Administrador

Se comprobaron las funciones administrativas y las restricciones correspondientes al rol `admin_documental`.

**Resultado:** Aprobado.


### QA-04 — Flujo end-to-end

Se verificó el flujo documental desde la carga inicial hasta su resolución final, incluyendo las transiciones correspondientes entre Usuario, Revisor y Administrador.

**Resultado:** Aprobado.


### QA-05 — Observabilidad

Se verificó el funcionamiento de los componentes de observabilidad y la disponibilidad de información relacionada con las operaciones realizadas sobre el sistema.

**Componentes comprobados:**

- OpenTelemetry.
- OpenTelemetry Collector.
- Prometheus.
- Grafana.
- Dashboard.
- Alertas.

**Resultado:** Aprobado.


### QA-06 — Archivado, reapertura y eliminación

Se verificó:

- Consulta de documentos aprobados.
- Consulta de documentos rechazados.
- Descarga.
- Reapertura mediante `Volver a revisión`.
- Aplicación de permisos de eliminación.

**Resultado:** Aprobado.


### QA-07 — Seguridad de autenticación

Se comprobaron las restricciones de acceso asociadas a los roles y la protección de las operaciones del backend.

Los usuarios sin los permisos correspondientes no pudieron ejecutar operaciones protegidas.

**Resultado:** Aprobado.


### QA-08 — Persistencia de datos

Se comprobó que los documentos y sus estados se almacenan correctamente mediante SQL Server y permanecen disponibles para las operaciones posteriores del sistema.

**Resultado:** Aprobado.


### QA-09 — Reproducibilidad local

Se comprobó el funcionamiento del sistema en el entorno local y la comunicación entre los componentes necesarios para su operación.

**Resultado:** Aprobado.


### QA-10 — Servicio de IA

Se comprobó la integración del servicio de inteligencia artificial y su capacidad para procesar las solicitudes de análisis definidas por el sistema.

**Resultado:** Aprobado.


### QA-11 — IA multi-proveedor (servicio)

Se comprobó el servicio con los proveedores `claude`, `ollama` y `none`, mediante los siguientes escenarios:

- IA desactivada.
- Proveedor inválido.
- Clave de Claude no configurada.
- Ollama sin conexión.
- Modelo local inexistente.
- Análisis con PDF.
- Análisis sin PDF, con aviso de análisis limitado.
- Uso del proveedor de respaldo.

**Resultado:** Aprobado.


### QA-12 — IA desde la interfaz

Se comprobó desde el frontend:

- El revisor y el administrador obtienen el análisis con el aviso "ANÁLISIS GENERADO POR IA".
- El usuario documental no tiene acceso a la función.
- El estado del documento no cambia tras el análisis.
- Los errores del proveedor se muestran con mensajes claros.
- El flujo documental sin IA no se ve afectado.

**Resultado:** Aprobado.


## 6. Resumen de resultados

| Estado | Cantidad |
|---|---:|
| Aprobadas | 12 |
| Fallidas | 0 |
| Pendientes | 0 |
| Total | 12 |

**Porcentaje de aprobación:** 100 %


## 7. Incidencias y correcciones

Durante el desarrollo se realizaron ajustes sobre funcionalidades, permisos y arquitectura antes de completar la validación final.

Las pruebas finales no presentaron incidencias bloqueantes que impidan el funcionamiento del MVP.

Las pruebas QA-11 y QA-12, correspondientes al proveedor de IA configurable, tampoco presentaron incidencias bloqueantes. Durante su preparación, la descarga del modelo local mediante el contenedor Docker falló por un error de certificado TLS de la red (`x509: certificate signed by unknown authority`); se resolvió utilizando la instalación nativa de Ollama.


## 8. Conclusión

Las pruebas QA realizadas permitieron validar el funcionamiento de las principales características de LegalTech, incluyendo autenticación, autorización por roles, gestión documental, flujo de revisión, persistencia y observabilidad.

Los 12 casos de prueba definidos fueron ejecutados satisfactoriamente, obteniendo un 100 % de aprobación y sin detectar incidencias bloqueantes en la validación final.

Asimismo, se validó el proveedor de IA configurable (Claude API, Ollama local o desactivado), su manejo controlado de errores y la no alteración del estado de los documentos.

Con base en los resultados obtenidos, el MVP cumple con las funcionalidades evaluadas y se encuentra en condiciones de continuar con la documentación final, mantenimiento, capacitación, evaluación post-implementación y cierre técnico.