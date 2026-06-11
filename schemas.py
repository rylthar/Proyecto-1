from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime


class SalaBase(BaseModel):
    """Schema base para Sala con validaciones comunes"""
    nombre: str = Field(..., min_length=1, max_length=100)
    capacidad: int = Field(..., ge=1, le=500)
    ubicacion: str = Field(..., min_length=1, max_length=255)
    equipamiento: Optional[str] = Field(default="Básico", max_length=500)
    disponible: bool = Field(default=True)
    razon_indisponibilidad: Optional[str] = Field(None, max_length=255)

    @field_validator('nombre')
    @classmethod
    def nombre_no_vacio(cls, v: str) -> str:
        """Validar que el nombre no sea solo espacios en blanco"""
        if not v or v.strip() == "":
            raise ValueError("El nombre no puede estar vacío o contener solo espacios")
        return v.strip()

    @model_validator(mode='after')
    def validar_razon_cuando_indisponible(self):
        """Si disponible=False, razon_indisponibilidad es recomendado"""
        if not self.disponible and not self.razon_indisponibilidad:
            self.razon_indisponibilidad = "No especificada"
        return self


class SalaCreate(SalaBase):
    """Schema para crear una nueva Sala"""
    pass


class SalaUpdate(BaseModel):
    """Schema para actualizar una Sala"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    capacidad: Optional[int] = Field(None, ge=1, le=500)
    ubicacion: Optional[str] = Field(None, min_length=1, max_length=255)
    equipamiento: Optional[str] = Field(None, max_length=500)
    disponible: Optional[bool] = None
    razon_indisponibilidad: Optional[str] = Field(None, max_length=255)

    @field_validator('nombre')
    @classmethod
    def nombre_no_vacio(cls, v: str) -> str:
        """Validar que el nombre no sea solo espacios en blanco"""
        if v is not None:
            if not v.strip():
                raise ValueError("El nombre no puede estar vacío o contener solo espacios")
            return v.strip()
        return v


class SalaResponse(SalaBase):
    """Schema para respuestas de Sala"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SalaListResponse(BaseModel):
    """Schema para lista paginada de Salas"""
    total: int
    skip: int
    limit: int
    items: list[SalaResponse]
