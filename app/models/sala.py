from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime


class Sala(Base):
    """Modelo de Sala en la base de datos"""
    __tablename__ = "salas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False, index=True)
    capacidad = Column(Integer, nullable=False)
    ubicacion = Column(String(255), nullable=False)
    equipamiento = Column(String(500), nullable=True, default="Básico")
    disponible = Column(Boolean, nullable=False, default=True)
    razon_indisponibilidad = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"<Sala(id={self.id}, nombre='{self.nombre}', capacidad={self.capacidad})>"
