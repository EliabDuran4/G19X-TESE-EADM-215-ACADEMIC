# Manual de Usuario

**LegalTech — Sistema de Observabilidad para Procesos Documentales**

## 1. Introducción

Este manual describe el uso del sistema LegalTech para los tres perfiles de usuario: usuario_documental, revisor_documental y admin_documental. Cada función se explica en pasos numerados.

## 2. Objetivo

Guiar al usuario final en el uso correcto de las funcionalidades del sistema según su rol asignado.

## 3. Requisitos para utilizar el sistema

- Contar con un usuario y contraseña asignados en Keycloak.
- Conocer el rol asignado a su cuenta.
- Acceso a un navegador web actualizado.
- Conexión a la red donde el sistema esté desplegado.
- Tener a la mano el documento que desea subir (solo para los roles que suben documentos).

## 4. Inicio de sesión

1. Abrir el navegador web.
2. Escribir en la barra de direcciones la URL del sistema: [POR CONFIRMAR: URL de acceso] y presionar **Enter**.
3. Si el sistema lo solicita, se mostrará la pantalla de inicio de sesión de Keycloak.
4. Escribir su **usuario** en el campo correspondiente.
5. Escribir su **contraseña**.
6. Presionar el botón de inicio de sesión.
7. El sistema lo redirige automáticamente y muestra las funciones que corresponden a su rol.

## 5. Interfaz general

Tras iniciar sesión, el usuario visualiza el listado de documentos correspondiente a su rol y las acciones disponibles según sus permisos.

1. Ubicar el listado de documentos.
2. Ubicar las acciones disponibles para su rol (por ejemplo, subir, consultar, descargar o revisar, según corresponda).
3. Ubicar el menú de usuario, desde donde se cierra la sesión.

### Estados de un documento

| Estado | Significado |
|---|---|
| recibido | El documento fue cargado y está pendiente de revisión |
| en_revision | El documento está siendo revisado |
| correccion | Se solicitó una corrección sobre el documento |
| revisado | La revisión fue completada |
| aprobado | El documento fue aprobado |
| rechazado | El documento fue rechazado |

## 6. Funciones — Usuario

### Iniciar sesión

1. Abrir el navegador y entrar a la URL del sistema (ver sección 6).
2. Escribir su usuario y contraseña.
3. Presionar el botón de inicio de sesión.
4. Verificar que se muestra la pantalla principal del rol usuario.

### Subir documento

1. Iniciar sesión.
2. Seleccionar la opción de carga de documento.
3. Presionar la opción para adjuntar y seleccionar el archivo en su equipo.
4. Verificar que el nombre del archivo seleccionado aparece en el formulario.
5. Seleccionar la categoría del documento (ver el procedimiento siguiente).
6. Confirmar la carga.
7. Verificar que el documento aparece en su listado con estado **recibido**.

### Seleccionar categoría

1. En el formulario de carga de documento, ubicar el campo de categoría.
2. Abrir la lista de categorías.
3. Seleccionar la categoría que corresponde a su documento.
4. Verificar que la categoría elegida aparece en el campo antes de confirmar la carga.
### Consultar documentos propios

1. Iniciar sesión.
2. Acceder al listado de documentos.
3. Verificar que se muestran únicamente los documentos que usted subió.
4. Ubicar el documento buscado revisando el listado.

### Consultar estado

1. En el listado de documentos propios, ubicar el documento.
2. Seleccionar el documento para ver su estado actual.
3. Identificar el estado: recibido, en_revision, revisado, aprobado, rechazado o correccion (ver tabla de estados en la sección 7).
4. Si el estado es **correccion**, el revisor solicitó una corrección sobre el documento.

### Cerrar sesión

1. Abrir el menú de usuario.
2. Seleccionar la opción de cierre de sesión.
3. Verificar que el sistema muestra nuevamente la pantalla de inicio de sesión.

## 7. Funciones — Revisor

### Iniciar sesión

1. Abrir el navegador y entrar a la URL del sistema (ver sección 6).
2. Escribir su usuario y contraseña.
3. Presionar el botón de inicio de sesión.
4. Verificar que se muestra la pantalla principal del rol revisor.

### Consultar documentos

1. Iniciar sesión.
2. Acceder al listado de documentos disponibles para revisión.
3. Ubicar el documento que desea revisar.
4. Seleccionar el documento para ver su detalle y estado.

### Descargar

1. En el listado de documentos, ubicar el documento.
2. Seleccionar el documento.
3. Elegir la opción de descarga.
4. Verificar que el archivo se descargó en su equipo (carpeta de descargas del navegador).

### Iniciar revisión

1. En el listado de documentos, ubicar un documento en estado **recibido**.
2. Seleccionar el documento.
3. Elegir la opción de iniciar revisión.
4. Verificar que el estado del documento cambió a **en_revision**.

### Agregar comentarios

1. Abrir el documento en estado **en_revision**.
2. Ubicar el campo de comentarios.
3. Escribir el comentario.
4. Guardar el comentario.
5. Verificar que el comentario aparece registrado en el documento.

### Marcar como revisado

1. Abrir el documento en estado **en_revision**.
2. Completar la revisión del documento (y agregar los comentarios necesarios).
3. Elegir la opción de marcar como revisado.
4. Verificar que el estado del documento cambió a **revisado**.

### Solicitar corrección

1. Abrir el documento en estado **en_revision**.
2. Elegir la opción de solicitud de corrección.
3. Indicar el motivo de la corrección.
4. Confirmar la solicitud.
5. Verificar que el estado del documento cambió a **correccion**.
6. Cuando el documento vuelva a revisión, retomarlo desde el paso de comentarios o marcar como revisado.

### Consultar Aprobados/Rechazados

1. Iniciar sesión.
2. Acceder a la sección de documentos finalizados.
3. Elegir la vista de **Aprobados** o **Rechazados** según lo que desea consultar.
4. Seleccionar un documento para ver su detalle.

### Volver a revisión

1. Acceder a la sección de documentos finalizados (Aprobados/Rechazados).
2. Ubicar el documento que desea reabrir.
3. Seleccionar el documento.
4. Elegir la opción de reapertura.
5. Confirmar la acción.
6. Verificar que el estado del documento cambió a **en_revision**.

### Cerrar sesión

1. Abrir el menú de usuario.
2. Seleccionar la opción de cierre de sesión.
3. Verificar que el sistema muestra nuevamente la pantalla de inicio de sesión.

## 8. Funciones — Admin

### Iniciar sesión

1. Abrir el navegador y entrar a la URL del sistema (ver sección 6).
2. Escribir su usuario y contraseña.
3. Presionar el botón de inicio de sesión.
4. Verificar que se muestra la pantalla principal del rol admin.

### Consultar documentos

1. Iniciar sesión.
2. Acceder al listado general de documentos.
3. Ubicar el documento buscado.
4. Seleccionar el documento para ver su detalle y estado.

### Descargar

1. En el listado de documentos, ubicar el documento.
2. Seleccionar el documento.
3. Elegir la opción de descarga.
4. Verificar que el archivo se descargó en su equipo (carpeta de descargas del navegador).

### Aprobar

1. En el listado de documentos, ubicar un documento en estado **revisado**.
2. Seleccionar el documento.
3. Elegir la opción de aprobar.
4. Confirmar la aprobación.
5. Verificar que el estado del documento cambió a **aprobado**.

### Rechazar

1. En el listado de documentos, ubicar un documento en estado **revisado**.
2. Seleccionar el documento.
3. Elegir la opción de rechazar.
4. Confirmar el rechazo.
5. Verificar que el estado del documento cambió a **rechazado**.

### Consultar Aprobados/Rechazados

1. Iniciar sesión.
2. Acceder a la sección de documentos finalizados.
3. Elegir la vista de **Aprobados** o **Rechazados** según lo que desea consultar.
4. Seleccionar un documento para ver su detalle.

### Volver a revisión

1. Acceder a la sección de documentos finalizados (Aprobados/Rechazados).
2. Ubicar el documento que desea reabrir.
3. Seleccionar el documento.
4. Elegir la opción de reapertura.
5. Confirmar la acción.
6. Verificar que el estado del documento cambió a **en_revision**.

### Eliminar documento

1. En el listado de documentos, ubicar el documento que desea eliminar.
2. Seleccionar el documento.
3. Elegir la opción de eliminación (disponible solo si su permiso lo habilita).
4. Confirmar la eliminación.
5. Verificar que el documento ya no aparece en el listado.

**Importante:** verifique que se trata del documento correcto antes de confirmar.

### Cerrar sesión

1. Abrir el menú de usuario.
2. Seleccionar la opción de cierre de sesión.
3. Verificar que el sistema muestra nuevamente la pantalla de inicio de sesión.

## 9. Recomendaciones básicas

- Verificar el documento antes de subirlo para evitar solicitudes de corrección.
- Seleccionar la categoría correcta al subir un documento.
- Cerrar sesión al finalizar el uso del sistema, especialmente en equipos compartidos.
- Revisar el estado del documento periódicamente durante el proceso de revisión.
- No compartir su usuario ni su contraseña.

## 10. Mensajes y errores comunes

| Mensaje/Error | Causa probable / qué hacer |
|---|---|
| Credenciales inválidas | 1. Revisar que el usuario y la contraseña estén bien escritos. 2. Verificar que no esté activada la tecla de mayúsculas. 3. Si persiste, contactar a soporte. |
| Documento no disponible | 1. Verificar que su rol permite ver ese documento. 2. Actualizar la página. 3. Si persiste, contactar a soporte. |
| Acción no permitida | La operación no corresponde a su rol. Consultar en este manual las funciones de su rol. |
| Sesión expirada | 1. Cerrar la pestaña o ventana. 2. Abrir nuevamente el sistema. 3. Iniciar sesión otra vez. |
| La cuenta no está completamente configurada | Contactar al administrador técnico para completar el perfil de su usuario. |

## 11. Conclusión

Este manual permite a los usuarios de LegalTech —usuario, revisor y admin— operar el sistema de forma correcta conforme a los permisos definidos para cada rol.