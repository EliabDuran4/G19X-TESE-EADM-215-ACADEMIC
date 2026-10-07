# Manual Técnico

**LegalTech — Sistema de Observabilidad para Procesos Documentales**

## 1. Introducción

El presente manual técnico documenta la instalación, configuración y operación del sistema LegalTech, orientado a desarrolladores y personal técnico responsable de su despliegue y mantenimiento. Los comandos se presentan para **Windows (PowerShell)**, entorno principal del proyecto.

## 2. Objetivo

Proporcionar las instrucciones técnicas necesarias para instalar, configurar, ejecutar y verificar el sistema LegalTech en un entorno local reproducible.

## 3. Alcance

Cubre la instalación y configuración de todos los componentes del sistema (frontend, backend, base de datos, autenticación, observabilidad, IA) desplegados mediante Docker Compose. No cubre procesos de CI/CD, actualmente fuera de alcance.

### Convenciones del manual

- `<VALOR_CONFIGURADO>`: valor que depende de su instalación. Cada vez que aparece, el manual indica dónde obtenerlo o configurarlo.
- `<NOMBRE_SERVICIO>`: nombre del servicio tal como aparece en el archivo `docker-compose.yml` del proyecto. Para conocerlo, ejecute `docker compose config --services`.
- Todos los comandos se ejecutan desde la raíz del proyecto, salvo que se indique lo contrario.

## 4. Requisitos técnicos

- Windows con Docker Desktop instalado.
- Docker Compose (incluido en Docker Desktop).
- Git instalado.
- PowerShell.
- Editor de código (recomendado: VS Code).
- Cuenta con acceso al repositorio de GitHub del proyecto.
- Clave de Claude API válida, propia del titular del proyecto.
- [POR CONFIRMAR: versión mínima de Docker / recursos de hardware recomendados]

### 4.1 Verificar requisitos instalados

1. Abrir PowerShell.
2. Ejecutar:

```powershell
docker --version
docker compose version
git --version
```

3. Verificar que cada comando devuelva un número de versión. Si alguno indica que no se reconoce el comando, instalar la herramienta correspondiente antes de continuar.

## 5. Tecnologías utilizadas

| Capa | Tecnología |
|---|---|
| Frontend | React.js + Vite |
| Backend | Python + FastAPI |
| ORM | SQLAlchemy |
| Autenticación | Keycloak (JWT + autorización por roles) |
| Base de datos | SQL Server Developer Edition — observabilidad_documental |
| Contenerización | Docker / Docker Compose |
| Observabilidad | OpenTelemetry, OpenTelemetry Collector, Prometheus, Grafana |
| IA | Claude API |
| Control de versiones | Git + GitHub |

## 6. Estructura y componentes del sistema

- Frontend (React.js + Vite): interfaz de usuario.
- Backend (FastAPI + SQLAlchemy): API REST y lógica de negocio.
- Base de datos (SQL Server): persistencia única en observabilidad_documental.
- Keycloak: autenticación y emisión de JWT.
- OpenTelemetry + Collector + Prometheus + Grafana: observabilidad.
- Claude API: análisis de documentos mediante IA.
- Docker Compose: orquestación de todos los servicios.

### 6.1 Identificar los servicios del proyecto

1. Abrir PowerShell en la raíz del proyecto.
2. Ejecutar:

```powershell
docker compose config --services
```

3. Anotar los nombres devueltos. Se usarán como `<NOMBRE_SERVICIO>` en los procedimientos de este manual.

## 7. Instalación del proyecto

### 7.1 Obtener el proyecto desde GitHub

1. Abrir PowerShell.
2. Ubicarse en la carpeta donde se guardará el proyecto:

```powershell
cd <VALOR_CONFIGURADO>
```

   *(ruta de la carpeta de trabajo elegida, por ejemplo la carpeta de proyectos del equipo)*

3. Abrir el repositorio del proyecto en GitHub desde el navegador.
4. Presionar el botón **Code** y copiar la URL HTTPS del repositorio.
5. Clonar el repositorio:

```powershell
git clone <VALOR_CONFIGURADO>
```

   *(URL copiada en el paso anterior)*

6. Entrar a la carpeta del proyecto:

```powershell
cd <VALOR_CONFIGURADO>
```

   *(nombre de la carpeta creada por el clon)*

7. Verificar que se encuentra en la rama `main`:

```powershell
git branch
git status
```

8. Listar el contenido para confirmar que existen los archivos del proyecto, incluido `docker-compose.yml`:

```powershell
dir
```

### 7.2 Abrir el proyecto en el editor

1. Desde la carpeta del proyecto, ejecutar:

```powershell
code .
```

2. Confirmar que el editor muestra las carpetas del frontend, backend y los archivos de Docker Compose.

## 8. Configuración

Antes de iniciar los servicios se debe preparar el archivo de variables de entorno y verificar que Docker esté en ejecución.

### 8.1 Iniciar Docker Desktop

1. Abrir **Docker Desktop** desde el menú Inicio de Windows.
2. Esperar a que el indicador de estado muestre que Docker está en ejecución (*Engine running*).
3. Verificar desde PowerShell:

```powershell
docker info
```

4. Si el comando devuelve información del servidor sin errores, Docker está listo.

## 9. Variables de entorno

### 9.1 Crear el archivo `.env`

1. Abrir PowerShell en la raíz del proyecto.
2. Verificar si existe un archivo de ejemplo de variables:

```powershell
dir -Force
```

3. Si existe un archivo de ejemplo (por ejemplo `.env.example`), copiarlo como `.env`:

```powershell
Copy-Item <VALOR_CONFIGURADO> .env
```

   *(nombre del archivo de ejemplo encontrado en el paso anterior)*

4. Si no existe archivo de ejemplo, crear el archivo:

```powershell
New-Item -Path .env -ItemType File
```

5. Abrir `.env` en el editor.
6. Completar las variables según la tabla siguiente.
7. Guardar el archivo.
8. Verificar que `.env` figura en `.gitignore` para que **no se suba a GitHub**:

```powershell
Select-String -Path .gitignore -Pattern "\.env"
```

9. Si no aparece, agregar la línea `.env` al archivo `.gitignore`.

### 9.2 Variables y dónde obtener cada valor

```env
DB_SERVER=<VALOR_CONFIGURADO>
DB_NAME=observabilidad_documental
DB_USER=<VALOR_CONFIGURADO>
DB_PASSWORD=<VALOR_CONFIGURADO>
KEYCLOAK_URL=<VALOR_CONFIGURADO>
KEYCLOAK_REALM=<VALOR_CONFIGURADO>
KEYCLOAK_CLIENT_ID=<VALOR_CONFIGURADO>
JWT_SECRET=<VALOR_CONFIGURADO>
CLAUDE_API_KEY=<VALOR_CONFIGURADO>
OTEL_EXPORTER_OTLP_ENDPOINT=<VALOR_CONFIGURADO>
PROMETHEUS_URL=<VALOR_CONFIGURADO>
GRAFANA_URL=<VALOR_CONFIGURADO>
```

| Variable | Dónde obtener / configurar el valor |
|---|---|
| `DB_SERVER` | Nombre del servicio de SQL Server en `docker-compose.yml` (si el backend corre en Docker) o host y puerto publicados por el contenedor (si el backend corre fuera de Docker). |
| `DB_NAME` | Fijo: `observabilidad_documental`. |
| `DB_USER` / `DB_PASSWORD` | Usuario y contraseña definidos al configurar SQL Server (sección 15.1). Deben coincidir con los usados por el contenedor de SQL Server. |
| `KEYCLOAK_URL` | URL base con la que se abre la consola de Keycloak desde el navegador (sección 13.1). |
| `KEYCLOAK_REALM` | Nombre exacto del Realm seleccionado o creado en la sección 13.3. |
| `KEYCLOAK_CLIENT_ID` | Campo *Client ID* del cliente configurado en la sección 13.4. |
| `JWT_SECRET` | Solo si el backend lo requiere en su configuración: generarlo localmente (ver 11.3). |
| `CLAUDE_API_KEY` | Clave generada por su cuenta en la consola de Anthropic (sección 20.1). |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Dirección del OpenTelemetry Collector: nombre del servicio del Collector en `docker-compose.yml` y el puerto OTLP configurado en su archivo de configuración. |
| `PROMETHEUS_URL` | Nombre de servicio y puerto de Prometheus en `docker-compose.yml`. |
| `GRAFANA_URL` | Nombre de servicio y puerto de Grafana en `docker-compose.yml`. |

[POR CONFIRMAR: lista definitiva de variables que exige el proyecto; contrastar con el archivo de ejemplo o con la sección `environment` de `docker-compose.yml`]

### 9.3 Generar un valor secreto local (opcional)

1. Abrir PowerShell.
2. Ejecutar:

```powershell
[Convert]::ToBase64String((1..48 | ForEach-Object { Get-Random -Maximum 256 }) -as [byte[]])
```

3. Copiar el resultado en la variable correspondiente de `.env`.
4. No compartir ni publicar este valor.

### 9.4 Verificar que Docker Compose lee las variables

1. Ejecutar:

```powershell
docker compose config
```

2. Confirmar que el resultado no muestra variables vacías ni advertencias de variables no definidas.

## 10. Ejecución mediante Docker Compose

### 10.1 Levantar los servicios

1. Confirmar que Docker Desktop está en ejecución (sección 10.1).
2. Abrir PowerShell en la raíz del proyecto.
3. Construir e iniciar todos los servicios:

```powershell
docker compose up -d --build
```

4. Esperar a que finalice el proceso sin errores.

### 10.2 Comprobar los contenedores

1. Ejecutar:

```powershell
docker compose ps
```

2. Verificar que todos los servicios aparecen con estado `running` (o `healthy`, si tienen *healthcheck*).
3. Si algún servicio aparece como `exited` o reiniciándose, revisar sus logs:

```powershell
docker compose logs --tail 100 <NOMBRE_SERVICIO>
```

4. También puede verificarse en Docker Desktop, sección **Containers**.

## 11. Configuración de Keycloak

### 11.1 Abrir la consola administrativa

1. Confirmar que el contenedor de Keycloak está en ejecución (`docker compose ps`).
2. Abrir el navegador.
3. Ingresar a la URL de Keycloak: `<VALOR_CONFIGURADO>` *(host y puerto publicados por el contenedor de Keycloak en `docker-compose.yml`)*.
4. Seleccionar **Administration Console**.
5. Iniciar sesión con el usuario administrador definido en la configuración de Keycloak del proyecto: `<VALOR_CONFIGURADO>` *(usuario y contraseña de administrador definidos en `docker-compose.yml` o en `.env`)*.

### 11.2 Ubicar el menú de Realms

1. En la parte superior izquierda de la consola, abrir el selector de Realm (muestra el Realm activo, por ejemplo *master*).
2. Revisar la lista de Realms existentes.

### 11.3 Crear o seleccionar el Realm

**Si el Realm del proyecto ya existe:**

1. Seleccionarlo en el selector de Realm.
2. Anotar su nombre exacto y colocarlo en `KEYCLOAK_REALM` del archivo `.env`.

**Si el Realm no existe:**

1. En el selector de Realm, presionar **Create Realm**.
2. En *Realm name*, escribir el nombre elegido para el proyecto: `<VALOR_CONFIGURADO>`.
3. Verificar que *Enabled* esté activo.
4. Presionar **Create**.
5. Anotar el nombre y colocarlo en `KEYCLOAK_REALM` del archivo `.env`.

### 11.4 Crear o configurar el Client

1. Con el Realm del proyecto seleccionado, ir a **Clients** en el menú lateral.
2. Si el cliente ya existe, abrirlo y pasar al paso 6.
3. Si no existe, presionar **Create client**.
4. En *Client type*, seleccionar **OpenID Connect**.
5. En *Client ID*, escribir el identificador elegido: `<VALOR_CONFIGURADO>`. Presionar **Next**.
6. En *Capability config*, habilitar **Standard flow** y presionar **Next**.
7. En *Login settings*, completar:
   - **Valid redirect URIs**: URL del frontend, tal como se abre en el navegador: `<VALOR_CONFIGURADO>`.
   - **Web origins**: el origen del frontend: `<VALOR_CONFIGURADO>`.
8. Presionar **Save**.
9. Colocar el *Client ID* en `KEYCLOAK_CLIENT_ID` del archivo `.env`.

### 11.5 Crear los tres roles del Realm

1. En el menú lateral, ir a **Realm roles**.
2. Presionar **Create role**.
3. En *Role name*, escribir `usuario_documental`. Presionar **Save**.
4. Volver a **Realm roles** y presionar **Create role**.
5. Escribir `revisor_documental`. Presionar **Save**.
6. Volver a **Realm roles** y presionar **Create role**.
7. Escribir `admin_documental`. Presionar **Save**.
8. Verificar en la lista de **Realm roles** que aparecen los tres roles con estos nombres exactos.

[INSERTAR CAPTURA: Keycloak mostrando los tres roles creados en Realm roles]

### 11.6 Crear o seleccionar usuarios

1. En el menú lateral, ir a **Users**.
2. Si el usuario ya existe, abrirlo y pasar a la sección 13.7.
3. Si no existe, presionar **Create new user** (o **Add user**).
4. Completar los datos personales requeridos: **Username**, **Email**, **First name** y **Last name** (ver 13.7).
5. Verificar que *Enabled* esté activo.
6. Presionar **Create**.
7. Abrir la pestaña **Credentials**.
8. Presionar **Set password**.
9. Escribir la contraseña del usuario y confirmarla.
10. Desactivar **Temporary** si el usuario no debe cambiar la contraseña en su primer inicio de sesión.
11. Presionar **Save** y confirmar.

Repetir el procedimiento para cada persona que usará el sistema.

### 11.7 Configuración de perfil de usuario

Keycloak puede bloquear el inicio de sesión con el mensaje *Account is not fully set up* si el perfil del usuario está incompleto.

1. Ir a **Users** y abrir el usuario.
2. En la pestaña **Details**, verificar que estén completos **Email**, **First name** y **Last name**.
3. Verificar que **Required user actions** esté vacío.
4. Presionar **Save**.
5. Para revisar qué atributos exige el Realm, ir a **Realm settings** → pestaña **User profile**.
6. Revisar qué atributos están marcados como requeridos y completarlos en todos los usuarios.

### 11.8 Asignar el rol a cada usuario

1. Ir a **Users** y abrir el usuario.
2. Abrir la pestaña **Role mapping**.
3. Presionar **Assign role**.
4. Si se muestran roles de Client, cambiar el filtro a **Filter by realm roles**.
5. Seleccionar el rol correspondiente (`usuario_documental`, `revisor_documental` o `admin_documental`).
6. Presionar **Assign**.
7. Verificar que el rol aparece en la lista de **Role mapping** del usuario.

### 11.9 Verificar la configuración

1. Abrir el frontend del sistema en el navegador.
2. Iniciar sesión con un usuario de cada rol.
3. Confirmar que el sistema permite el acceso y muestra únicamente las funciones del rol (sección 14).
4. Si el inicio de sesión falla, revisar la sección 23.

## 12. Roles

| Rol | Permisos |
|---|---|
| usuario_documental | Login, subir documentos, consultar propios documentos, consultar estado |
| revisor_documental | Login, subir, consultar, descargar, iniciar revisión, comentar, marcar revisado, solicitar corrección, ver aprobados/rechazados, reabrir finalizados |
| admin_documental | Login, subir, consultar, descargar, aprobar, rechazar, ver aprobados/rechazados, reabrir finalizados, eliminar según permisos |

## 13. Base de datos SQL Server

El sistema utiliza una única base de datos SQL Server Developer Edition denominada observabilidad_documental. No se utiliza arquitectura de shards ni enrutamiento hacia bases diferenciadas.

### 13.1 Configurar SQL Server

1. Abrir `docker-compose.yml` y ubicar el servicio de SQL Server.
2. Verificar que define la aceptación de la licencia y la contraseña del usuario `sa` mediante variables de entorno, tomadas de `.env`.
3. Verificar que el servicio publica un puerto y usa un volumen para la persistencia de datos.
4. Colocar en `.env` los valores de `DB_SERVER`, `DB_USER` y `DB_PASSWORD` coherentes con esa configuración.
5. Iniciar el servicio:

```powershell
docker compose up -d <NOMBRE_SERVICIO>
```

   *(servicio de SQL Server)*

6. Esperar a que aparezca como `running` en `docker compose ps`.

### 13.2 Comprobar la conexión a SQL Server

1. Abrir una consola dentro del contenedor de SQL Server:

```powershell
docker compose exec <NOMBRE_SERVICIO> bash
```

2. Conectarse con `sqlcmd` (la ruta puede variar según la imagen; probar primero `/opt/mssql-tools18/bin/sqlcmd` y luego `/opt/mssql-tools/bin/sqlcmd`):

```bash
/opt/mssql-tools18/bin/sqlcmd -S localhost -U <VALOR_CONFIGURADO> -P '<VALOR_CONFIGURADO>' -C
```

   *(usuario y contraseña definidos en `.env`)*

3. Si la conexión es correcta, aparece el indicador `1>`.

### 13.3 Comprobar la base de datos

1. Dentro de `sqlcmd`, ejecutar:

```sql
SELECT name FROM sys.databases;
GO
```

2. Confirmar que aparece `observabilidad_documental`.
3. Para revisar sus tablas:

```sql
USE observabilidad_documental;
GO
SELECT name FROM sys.tables;
GO
```

4. Para salir:

```sql
EXIT
```

5. Si la base no existe, revisar los logs del backend y del contenedor de SQL Server (sección 19.6), ya que la creación depende de cómo el proyecto inicializa la base. [POR CONFIRMAR: mecanismo de creación/inicialización de la base y tablas]

### 13.4 Respaldo básico de la base de datos

1. Crear una carpeta de respaldo dentro del contenedor:

```powershell
docker compose exec <NOMBRE_SERVICIO> mkdir -p /var/opt/mssql/backup
```

2. Ejecutar el respaldo desde `sqlcmd` (ver 15.2):

```sql
BACKUP DATABASE observabilidad_documental
TO DISK = '/var/opt/mssql/backup/observabilidad_documental.bak'
WITH INIT, FORMAT;
GO
```

3. Verificar que el comando finaliza con el mensaje de respaldo exitoso.
4. Copiar el archivo al equipo anfitrión:

```powershell
docker compose cp <NOMBRE_SERVICIO>:/var/opt/mssql/backup/observabilidad_documental.bak <VALOR_CONFIGURADO>
```

   *(ruta local donde se guardarán los respaldos)*

5. Guardar el archivo en una ubicación segura, fuera del repositorio Git.

## 14. Backend FastAPI

El backend expone la API REST consumida por el frontend, gestiona la lógica del flujo documental, valida los tokens JWT emitidos por Keycloak y se comunica con SQL Server mediante SQLAlchemy.

### 14.1 Verificar el backend en Docker Compose

1. Confirmar que el servicio del backend está en ejecución:

```powershell
docker compose ps
```

2. Revisar sus logs recientes:

```powershell
docker compose logs --tail 100 <NOMBRE_SERVICIO>
```

   *(servicio del backend)*

3. Confirmar que los logs indican que la aplicación inició sin errores de conexión a SQL Server ni a Keycloak.

### 14.2 Ejecutar el backend manualmente (opcional, modo desarrollo)

1. Abrir PowerShell en la carpeta del backend: `cd <VALOR_CONFIGURADO>`.
2. Crear y activar un entorno virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

4. Iniciar el servidor:

```powershell
uvicorn app.main:app --reload
```

5. Verificar que la consola muestra que el servidor está escuchando.

INFO:     Will watch for changes in these directories: ['C:']
INFO:     Uvicorn running on http:..... (Press CTRL+C to quit)
INFO:     Started reloader process [8260] using WatchFiles
INFO:     Started server process [32536]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

### 14.3 Acceder y probar Swagger

1. Abrir el navegador.
2. Ingresar a la URL del backend `<VALOR_CONFIGURADO>` *(host y puerto publicados del servicio del backend)* agregando la ruta `/docs`.
3. Verificar que se muestra la documentación interactiva de FastAPI (Swagger UI) con los endpoints disponibles.
4. Si la página no carga, revisar los logs del backend (16.1). [POR CONFIRMAR: si la documentación `/docs` está habilitada en el proyecto]
5. Para probar un endpoint protegido, obtener primero un token JWT (ver 18.2) y presionar **Authorize** en Swagger, si está disponible.
6. Expandir un endpoint, presionar **Try it out** y luego **Execute**.
7. Verificar el código de respuesta: `200` (correcto), `401` (sin token o token inválido) o `403` (rol sin permiso).


## 15. Frontend React/Vite

El frontend se ejecuta mediante Vite y consume la API expuesta por el backend.

### 16.1 Verificar el frontend en Docker Compose

1. Confirmar que el servicio del frontend está en `running` con `docker compose ps`.
2. Abrir el navegador y entrar a la URL del frontend: `<VALOR_CONFIGURADO>` *(host y puerto publicados del servicio del frontend)*.
3. Verificar que se muestra la pantalla de inicio de sesión de LegalTech.

### 16.2 Ejecutar el frontend manualmente (opcional, modo desarrollo)

1. Abrir PowerShell en la carpeta del frontend: `cd <VALOR_CONFIGURADO>`.
2. Instalar las dependencias:

```powershell
npm install
```

3. Iniciar el servidor de desarrollo:

```powershell
npm run dev
```

4. Abrir en el navegador la URL que Vite muestra en la consola.
5. Verificar que la aplicación carga y permite iniciar sesión.

## 17. Seguridad y JWT

La autenticación se realiza mediante Keycloak, que emite un token JWT tras el login. El backend valida el token en cada solicitud y aplica autorización según el rol contenido en él.

### 17.1 Verificar el flujo de autenticación

1. Abrir el frontend en el navegador.
2. Iniciar sesión con un usuario válido.
3. Confirmar que el sistema muestra las funciones del rol del usuario.
4. Cerrar sesión y confirmar que las funciones ya no están accesibles.

### 17.2 Inspeccionar el contenido del token (diagnóstico)

1. Iniciar sesión en el frontend.
2. Abrir las herramientas de desarrollador del navegador (F12) → pestaña **Network**.
3. Realizar una acción en el sistema y seleccionar una solicitud al backend.
4. En **Headers**, ubicar `Authorization: Bearer <token>`.
5. Copiar el token y decodificarlo en una herramienta local de confianza (no publicar el token).
6. Verificar que contiene el rol del usuario y una fecha de expiración vigente.

### 17.3 Verificar la autorización por rol

1. Iniciar sesión con `usuario_documental` y comprobar que **no** puede aprobar, rechazar ni eliminar.
2. Iniciar sesión con `revisor_documental` y comprobar que puede revisar y solicitar correcciones, pero no aprobar ni rechazar.
3. Iniciar sesión con `admin_documental` y comprobar que puede aprobar y rechazar.


## 18. Observabilidad

### 18.1 OpenTelemetry

Instrumenta frontend y backend para generar trazas y métricas.

1. Abrir el archivo `.env` y verificar que `OTEL_EXPORTER_OTLP_ENDPOINT` apunta al Collector (11.2).
2. Verificar que el servicio del backend define esa variable en `docker-compose.yml`.
3. Reiniciar el backend para aplicar cambios:

```powershell
docker compose restart <NOMBRE_SERVICIO>
```

4. Generar actividad en el sistema (iniciar sesión, subir un documento).
5. Revisar los logs del backend y confirmar que no aparecen errores de exportación de telemetría:

```powershell
docker compose logs --tail 100 <NOMBRE_SERVICIO>
```

### 18.2 OpenTelemetry Collector

Recibe y procesa la telemetría emitida por los servicios instrumentados.

1. Confirmar que el servicio del Collector está en `running`:

```powershell
docker compose ps
```

2. Revisar sus logs:

```powershell
docker compose logs --tail 100 <NOMBRE_SERVICIO>
```

   *(servicio del Collector)*

3. Generar actividad en el sistema y volver a revisar los logs.
4. Confirmar que no hay errores de configuración ni de conexión hacia Prometheus.


### 18.3 Prometheus

Almacena las métricas recolectadas por el Collector.

1. Abrir el navegador en la URL de Prometheus: `<VALOR_CONFIGURADO>` *(host y puerto publicados del servicio de Prometheus)*.
2. Ir al menú **Status** → **Targets**.
3. Verificar que los objetivos aparecen con estado **UP**.
4. Ir a la pestaña **Graph** y escribir el nombre de una métrica en el cuadro de expresión (puede usarse el autocompletado para ver las métricas disponibles).
5. Presionar **Execute** y confirmar que devuelve datos.
6. Si un objetivo aparece **DOWN**, revisar los logs del Collector y del servicio afectado.


### 18.4 Grafana

Visualiza las métricas mediante dashboards y gestiona alertas.

**Acceder:**

1. Abrir el navegador en la URL de Grafana: `<VALOR_CONFIGURADO>` *(host y puerto publicados del servicio de Grafana)*.
2. Iniciar sesión con las credenciales de Grafana definidas en la configuración del proyecto: `<VALOR_CONFIGURADO>`.

**Verificar el origen de datos:**

3. Ir a **Connections** → **Data sources**.
4. Confirmar que existe un origen de datos de tipo Prometheus.
5. Abrirlo y presionar **Save & test** para comprobar la conexión.

**Consultar el dashboard:**

6. Ir a **Dashboards**.
7. Abrir el dashboard del proyecto: `<VALOR_CONFIGURADO>` *(nombre del dashboard configurado)*.
8. Ajustar el rango de tiempo en la esquina superior derecha (por ejemplo, últimos 15 minutos).
9. Verificar que los paneles muestran datos.
10. Generar actividad en el sistema y comprobar que las métricas se actualizan.

**Comprobar alertas:**

11. Ir a **Alerting** → **Alert rules**.
12. Verificar que las reglas de alerta del proyecto aparecen listadas y su estado (*Normal*, *Pending* o *Firing*).
13. Abrir una regla para revisar su condición y el origen de datos asociado.

### 18.5 Verificación integral de observabilidad

1. Iniciar sesión en el sistema y subir un documento de prueba.
2. Esperar unos segundos.
3. Abrir el dashboard de Grafana y confirmar que se reflejó la actividad.
4. Si no hay datos, recorrer la cadena en este orden: backend (19.1) → Collector (19.2) → Prometheus (19.3) → Grafana (19.4).

### 18.6 Logs backend/contenedores

Los logs corresponden al backend y a los contenedores Docker; no se utiliza Grafana Loki.

1. Ver los logs de todos los servicios:

```powershell
docker compose logs --tail 100
```

2. Seguir en tiempo real los logs de un servicio (detener con `Ctrl + C`):

```powershell
docker compose logs -f <NOMBRE_SERVICIO>
```

3. Filtrar líneas con errores:

```powershell
docker compose logs --tail 500 <NOMBRE_SERVICIO> | Select-String -Pattern "error"
```

4. Guardar los logs en un archivo para revisión:

```powershell
docker compose logs --no-color > logs.txt
```

5. También pueden consultarse en Docker Desktop: **Containers** → seleccionar el contenedor → pestaña **Logs**.

[INSERTAR CAPTURA: logs del backend en PowerShell o en Docker Desktop]

## 19. Integración Claude API

El backend invoca la Claude API para el análisis de documentos, utilizando la variable CLAUDE_API_KEY configurada en el entorno.

### 19.1 Configurar la clave de Claude API

1. Iniciar sesión en la consola de Anthropic con la cuenta del titular del proyecto.
2. Ir a la sección de claves de API y crear una nueva clave.
3. Copiar la clave en el momento de su creación.
4. Abrir el archivo `.env` y colocar la clave: `CLAUDE_API_KEY=<VALOR_CONFIGURADO>`.
5. Guardar el archivo.
6. **No** publicar la clave en el repositorio, capturas, mensajes ni documentos.
7. Recrear el servicio del backend para aplicar la variable:

```powershell
docker compose up -d --force-recreate <NOMBRE_SERVICIO>
```

### 19.2 Verificar que la clave está configurada (sin mostrarla)

1. Ejecutar:

```powershell
docker compose exec <NOMBRE_SERVICIO> printenv CLAUDE_API_KEY
```

2. Confirmar únicamente que devuelve un valor (no vacío). No copiar ni compartir el resultado.

### 19.3 Verificar el servicio de análisis mediante IA

1. Iniciar sesión en el sistema con un rol que tenga acceso al análisis. [POR CONFIRMAR: ubicación exacta de la función de análisis mediante IA en la interfaz]
2. Ejecutar el análisis sobre un documento de prueba.
3. Confirmar que se obtiene un resultado.
4. Si falla, revisar los logs del backend (19.6) y verificar que la clave sea válida y que exista conectividad a Internet.

## 20. Control de versiones Git/GitHub

El proyecto utiliza Git como sistema de control de versiones, con repositorio en GitHub. El Sprint 1 fue registrado mediante commit y el código se encuentra en la rama main. La automatización mediante GitHub Actions/CI-CD queda fuera de alcance por el momento.

### 20.1 Revisar el estado del repositorio

1. Abrir PowerShell en la raíz del proyecto.
2. Ejecutar:

```powershell
git status
git branch
git log --oneline -5
```

3. Confirmar que se encuentra en `main` y que el commit del Sprint 1 aparece en el historial.

### 20.2 Registrar y subir cambios

1. Revisar los archivos modificados:

```powershell
git status
```

2. Confirmar que `.env` **no** aparece en la lista de archivos a subir.
3. Agregar los cambios:

```powershell
git add .
```

4. Crear el commit con un mensaje descriptivo:

```powershell
git commit -m "<VALOR_CONFIGURADO>"
```

   *(mensaje que describe el cambio realizado)*

5. Subir a GitHub:

```powershell
git push origin main
```

6. Verificar en GitHub que el commit aparece en la rama `main`.

### 20.3 Actualizar el proyecto local

1. Ejecutar:

```powershell
git pull origin main
```

2. Reconstruir los servicios si hubo cambios:

```powershell
docker compose up -d --build
```

## 21. Procedimiento básico para detener/reiniciar servicios

### 21.1 Detener los servicios (conserva datos)

1. Abrir PowerShell en la raíz del proyecto.
2. Ejecutar:

```powershell
docker compose stop
```

3. Verificar con `docker compose ps` que los servicios están detenidos.

### 21.2 Iniciar nuevamente los servicios detenidos

```powershell
docker compose start
```

### 21.3 Reiniciar todos los servicios o uno específico

```powershell
docker compose restart
docker compose restart <NOMBRE_SERVICIO>
```

### 21.4 Apagar y eliminar contenedores

1. Ejecutar:

```powershell
docker compose down
```

2. Este comando elimina los contenedores y la red, pero **conserva** los volúmenes de datos.
3. Para volver a iniciar: `docker compose up -d`.

**Advertencia:** el comando `docker compose down -v` elimina también los volúmenes, incluidos los datos de la base de datos. No ejecutarlo sin contar con un respaldo (15.4).

## 22. Solución básica de problemas

Procedimiento general de diagnóstico:

1. Ejecutar `docker compose ps` para identificar el servicio con problemas.
2. Revisar sus logs: `docker compose logs --tail 100 <NOMBRE_SERVICIO>`.
3. Aplicar la acción de la tabla correspondiente.
4. Reiniciar el servicio: `docker compose restart <NOMBRE_SERVICIO>`.
5. Repetir la prueba que falló.

| Problema | Diagnóstico y solución |
|---|---|
| Un contenedor no inicia | 1. `docker compose logs --tail 100 <NOMBRE_SERVICIO>`. 2. Revisar el último error. 3. Verificar variables en `.env` (11.4). 4. `docker compose up -d --build`. |
| Docker no responde | 1. Abrir Docker Desktop y esperar *Engine running*. 2. `docker info`. 3. Reiniciar Docker Desktop si persiste. |
| Puerto ocupado | 1. Identificar el proceso: `netstat -ano \| findstr :<VALOR_CONFIGURADO>` (puerto en conflicto). 2. Cerrar el proceso o cambiar el puerto publicado en `docker-compose.yml`. 3. `docker compose up -d`. |
| Error de autenticación / no permite iniciar sesión | 1. Verificar que Keycloak está en `running`. 2. Comprobar `KEYCLOAK_REALM` y `KEYCLOAK_CLIENT_ID` (13.3, 13.4). 3. Revisar *Valid redirect URIs* del Client. 4. Revisar el perfil del usuario (13.7). |
| Error 401 en la API | 1. Cerrar sesión e iniciar de nuevo (el token pudo expirar). 2. Verificar `KEYCLOAK_URL` y `KEYCLOAK_REALM` del backend. |
| Error 403 en la API | 1. Verificar el rol asignado al usuario (13.8). 2. Confirmar que el rol permite la operación (sección 14). |
| Error de conexión a base de datos | 1. Verificar que SQL Server está `running`. 2. Comprobar `DB_SERVER`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`. 3. Probar la conexión con `sqlcmd` (15.2). 4. Reiniciar el backend. |
| Métricas no visibles en Grafana | 1. Comprobar Collector (19.2). 2. Comprobar Targets en Prometheus (19.3). 3. Probar el origen de datos en Grafana (19.4). 4. Verificar `OTEL_EXPORTER_OTLP_ENDPOINT`. |
| Falla el análisis con IA | 1. Verificar `CLAUDE_API_KEY` (20.2). 2. Revisar logs del backend. 3. Confirmar conexión a Internet. |
| Frontend no carga | 1. `docker compose ps`. 2. Revisar logs del frontend. 3. Verificar la URL y el puerto. |

## 23. Mantenimiento

### 23.1 Revisión periódica

1. Ejecutar `docker compose ps` y verificar que todos los servicios están en ejecución.
2. Revisar el dashboard de Grafana (19.4).
3. Revisar los logs en busca de errores (19.6).
4. Realizar el respaldo de la base de datos (15.4).

### 23.2 Actualización controlada de dependencias

1. Realizar un respaldo de la base de datos (15.4) y confirmar que el código está registrado en Git.
2. Actualizar las dependencias del backend (`requirements.txt`) o del frontend (`package.json`).
3. Reconstruir: `docker compose up -d --build`.
4. Verificar el sistema con los pasos de la sección 18.1 y 19.5.
5. Si algo falla, restaurar la versión anterior con Git y reconstruir.

Ver Documento 3 — Plan de Mantenimiento y Soporte para el detalle completo.

## 24. Conclusión

Este manual técnico documenta los pasos necesarios para instalar, configurar, verificar y operar el sistema LegalTech en un entorno local, sirviendo de referencia para el equipo técnico responsable de su despliegue y mantenimiento.