USE observabilidad_documental;
GO

CREATE OR ALTER VIEW dbo.vw_estadisticas_documentos
AS
SELECT
    category AS Categoria,
    status AS Estado,
    COUNT(*) AS TotalDocumentos
FROM dbo.documents
GROUP BY category, status;
GO
