from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from repository import SalaRepository
from schemas import SalaCreate, SalaUpdate, SalaResponse, SalaListResponse
from models import Sala
from typing import Optional, List
from fastapi import HTTPException, status


class SalaService:
    """Capa de servicio con lógica de negocio para Sala"""

    @staticmethod
    def crear_sala(db: Session, sala_data: SalaCreate) -> SalaResponse:
        """Crear una nueva sala con validaciones de negocio"""
        # Validar nombre único
        if SalaRepository.existe_nombre(db, sala_data.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una sala con el nombre '{sala_data.nombre}'"
            )

        try:
            sala = SalaRepository.crear(db, sala_data)
            return SalaResponse.model_validate(sala)
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Error de integridad: nombre de sala duplicado"
            )

    @staticmethod
    def obtener_sala(db: Session, sala_id: int) -> SalaResponse:
        """Obtener una sala por ID"""
        sala = SalaRepository.obtener_por_id(db, sala_id)
        if not sala:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sala con ID {sala_id} no encontrada"
            )
        return SalaResponse.model_validate(sala)

    @staticmethod
    def obtener_todas_salas(
        db: Session,
        skip: int = 0,
        limit: int = 10
    ) -> SalaListResponse:
        """Obtener todas las salas con paginación"""
        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El parámetro 'skip' no puede ser negativo"
            )
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El parámetro 'limit' debe estar entre 1 y 100"
            )

        salas, total = SalaRepository.obtener_todos(db, skip, limit)
        return SalaListResponse(
            total=total,
            skip=skip,
            limit=limit,
            items=[SalaResponse.model_validate(sala) for sala in salas]
        )

    @staticmethod
    def actualizar_sala(db: Session, sala_id: int, sala_data: SalaUpdate) -> SalaResponse:
        """Actualizar una sala existente"""
        sala = SalaRepository.obtener_por_id(db, sala_id)
        if not sala:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sala con ID {sala_id} no encontrada"
            )

        # Validar nombre único si se proporciona
        if sala_data.nombre and SalaRepository.existe_nombre(db, sala_data.nombre, sala_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una sala con el nombre '{sala_data.nombre}'"
            )

        try:
            sala_actualizada = SalaRepository.actualizar(db, sala_id, sala_data)
            return SalaResponse.model_validate(sala_actualizada)
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Error de integridad al actualizar la sala"
            )

    @staticmethod
    def eliminar_sala(db: Session, sala_id: int) -> None:
        """Eliminar una sala"""
        sala = SalaRepository.obtener_por_id(db, sala_id)
        if not sala:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sala con ID {sala_id} no encontrada"
            )

        SalaRepository.eliminar(db, sala_id)
