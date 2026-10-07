from app.core.database import Base, engine
from app.models.document import Document

Base.metadata.create_all(bind=engine)
print("Tabla creada en observabilidad_documental")