-- Usuario de solo lectura para reporting-service.
-- Reemplaza <CLAVE> por una clave propia (la misma que REPORTING_DB_PASSWORD en .env).
-- No subas la clave real al repositorio.
USE master;
CREATE LOGIN reporting_ro WITH PASSWORD = '<CLAVE>', CHECK_POLICY = ON;
GO
USE observabilidad_documental;
CREATE USER reporting_ro FOR LOGIN reporting_ro;
GRANT SELECT ON dbo.vw_resumen_documentos      TO reporting_ro;
GRANT SELECT ON dbo.vw_estadisticas_documentos TO reporting_ro;
GRANT SELECT ON dbo.vw_trazabilidad_documental TO reporting_ro;
GO
