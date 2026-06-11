from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Sala
from schemas import SalaCreate, SalaUpdate
from typing import Optional, List


class SalaRepository:
    """Capa de repositorio para operaciones CRUD de Sala"""

    @staticmethod
    def crear(db: Session, sala_data: SalaCreate) -> Sala:
        """Crear una nueva sala en la base de datos"""
        sala = Sala(**sala_data.model_dump())
        db.add(sala)
        db.commit()
        db.refresh(sala)
        return sala

    @staticmethod
    def obtener_por_id(db: Session, sala_id: int) -> Optional[Sala]:
        """Obtener una sala por su ID"""
        return db.query(Sala).filter(Sala.id == sala_id).first()

    @staticmethod
    def obtener_por_nombre(db: Session, nombre: str) -> Optional[Sala]:
        """Obtener una sala por su nombre"""
        return db.query(Sala).filter(Sala.nombre == nombre).first()

    @staticmethod
    def obtener_todos(
        db: Session,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[Sala], int]:
        """Obtener todas las salas con paginación"""
        query = db.query(Sala)
        total = query.count()
        salas = query.offset(skip).limit(limit).all()
        return salas, total

    @staticmethod
    def actualizar(db: Session, sala_id: int, sala_data: SalaUpdate) -> Optional[Sala]:
        """Actualizar una sala existente"""
        sala = SalaRepository.obtener_por_id(db, sala_id)
        if not sala:
            return None

        datos_actualizacion = sala_data.model_dump(exclude_unset=True)
        for campo, valor in datos_actualizacion.items():
            setattr(sala, campo, valor)

        db.commit()
        db.refresh(sala)
        return sala

    @staticmethod
    def eliminar(db: Session, sala_id: int) -> bool:
        """Eliminar una sala por su ID"""
        sala = SalaRepository.obtener_por_id(db, sala_id)
        if not sala:
            return False

        db.delete(sala)
        db.commit()
        return True

    @staticmethod
    def existe_nombre(db: Session, nombre: str, sala_id: Optional[int] = None) -> bool:
        """Verificar si un nombre ya existe (excluyendo la sala actual si se proporciona ID)"""
        query = db.query(Sala).filter(Sala.nombre == nombre)
        if sala_id:
            query = query.filter(Sala.id != sala_id)
        return query.first() is not None
