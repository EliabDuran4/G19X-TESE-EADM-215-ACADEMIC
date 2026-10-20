USE observabilidad_documental;
GO

CREATE OR ALTER VIEW dbo.vw_trazabilidad_documental
AS
SELECT
    e.id AS EventoID,
    d.id AS DocumentoID,
    d.original_filename AS NombreArchivo,
    d.category AS Categoria,
    e.previous_status AS EstadoAnterior,
    e.new_status AS EstadoNuevo,
    e.username AS Usuario,
    e.comment AS Comentario,
    e.created_at AS FechaEvento
FROM dbo.document_events AS e
INNER JOIN dbo.documents AS d
    ON e.document_id = d.id;
GO
