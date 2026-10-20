USE observabilidad_documental;
GO

CREATE OR ALTER VIEW dbo.vw_resumen_documentos
AS
SELECT
    d.id AS DocumentoID,
    d.original_filename AS NombreArchivo,
    d.category AS Categoria,
    d.status AS Estado,
    d.uploaded_by AS UsuarioCarga,
    d.uploaded_at AS FechaCarga,
    d.reviewed_by AS RevisadoPor,
    d.reviewed_at AS FechaRevision,
    COUNT(e.id) AS TotalEventos
FROM dbo.documents AS d
LEFT JOIN dbo.document_events AS e
    ON d.id = e.document_id
GROUP BY
    d.id, d.original_filename, d.category, d.status,
    d.uploaded_by, d.uploaded_at, d.reviewed_by, d.reviewed_at;
GO
