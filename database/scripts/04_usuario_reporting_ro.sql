-- Usuario de solo lectura para reporting-service.
-- La clave se toma de la variable sqlcmd REPORTING_DB_PASSWORD (la misma del .env).
-- No subas la clave real al repositorio.
USE observabilidad_documental;
IF NOT EXISTS (SELECT 1 FROM sys.server_principals WHERE name = 'reporting_ro')
    CREATE LOGIN reporting_ro WITH PASSWORD = '$(REPORTING_DB_PASSWORD)', CHECK_POLICY = ON;
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = 'reporting_ro')
    CREATE USER reporting_ro FOR LOGIN reporting_ro;
GRANT SELECT ON dbo.vw_resumen_documentos      TO reporting_ro;
GRANT SELECT ON dbo.vw_estadisticas_documentos TO reporting_ro;
GRANT SELECT ON dbo.vw_trazabilidad_documental TO reporting_ro;
GO