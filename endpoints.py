from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from database import get_db
from service import SalaService
from schemas import SalaCreate, SalaUpdate, SalaResponse, SalaListResponse
from typing import Optional

router = APIRouter(prefix="/salas", tags=["salas"])


@router.get(
    "",
    response_model=SalaListResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener todas las salas",
    description="Obtiene un listado paginado de todas las salas registradas"
)
def obtener_salas(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros a devolver"),
    db: Session = Depends(get_db)
) -> SalaListResponse:
    """
    Obtener todas las salas con paginación.

    **Parámetros de consulta:**
    - skip: número de salas a saltar (default: 0)
    - limit: número máximo de salas a devolver, máximo 100 (default: 10)

    **Respuestas:**
    - 200 OK: Array de salas con información de paginación
    - 400 Bad Request: Parámetros inválidos
    """
    return SalaService.obtener_todas_salas(db, skip, limit)


@router.get(
    "/{sala_id}",
    response_model=SalaResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener sala por ID",
    description="Obtiene los detalles de una sala específica por su identificador"
)
def obtener_sala(
    sala_id: int,
    db: Session = Depends(get_db)
) -> SalaResponse:
    """
    Obtener una sala específica por su ID.

    **Parámetros de ruta:**
    - sala_id: identificador único de la sala

    **Respuestas:**
    - 200 OK: Datos completos de la sala
    - 404 Not Found: La sala no existe
    """
    return SalaService.obtener_sala(db, sala_id)


@router.post(
    "",
    response_model=SalaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva sala",
    description="Crea una nueva sala de conferencias en el sistema"
)
def crear_sala(
    sala_data: SalaCreate,
    db: Session = Depends(get_db)
) -> SalaResponse:
    """
    Crear una nueva sala.

    **Validaciones requeridas:**
    - nombre: único, entre 1-100 caracteres, no solo espacios en blanco
    - capacidad: entre 1-500 personas
    - ubicacion: entre 1-255 caracteres
    - equipamiento: opcional, máximo 500 caracteres (default: "Básico")

    **Body esperado:**
    ```json
    {
        "nombre": "Sala de Conferencias A",
        "capacidad": 20,
        "ubicacion": "Piso 3, Ala Norte",
        "equipamiento": "Proyector, Pizarra digital"
    }
    ```

    **Respuestas:**
    - 201 Created: Sala creada exitosamente con ID asignado
    - 400 Bad Request: Datos de entrada inválidos
    - 409 Conflict: Nombre de sala duplicado
    """
    return SalaService.crear_sala(db, sala_data)


@router.put(
    "/{sala_id}",
    response_model=SalaResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar una sala",
    description="Actualiza los datos de una sala existente"
)
def actualizar_sala(
    sala_id: int,
    sala_data: SalaUpdate,
    db: Session = Depends(get_db)
) -> SalaResponse:
    """
    Actualizar una sala existente.

    **Parámetros de ruta:**
    - sala_id: identificador de la sala a actualizar

    **Campos actualizables:**
    - nombre, capacidad, ubicacion, equipamiento, disponible, razon_indisponibilidad
    - Los campos id y created_at no pueden modificarse
    - Todos los campos son opcionales

    **Body esperado:**
    ```json
    {
        "nombre": "Sala de Conferencias A (Actualizada)",
        "capacidad": 25,
        "disponible": false,
        "razon_indisponibilidad": "En mantenimiento"
    }
    ```

    **Respuestas:**
    - 200 OK: Sala actualizada exitosamente
    - 400 Bad Request: Datos de entrada inválidos
    - 404 Not Found: La sala no existe
    - 409 Conflict: Nombre duplicado
    """
    return SalaService.actualizar_sala(db, sala_id, sala_data)


@router.delete(
    "/{sala_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una sala",
    description="Elimina una sala del sistema de forma permanente"
)
def eliminar_sala(
    sala_id: int,
    db: Session = Depends(get_db)
) -> None:
    """
    Eliminar una sala.

    **Parámetros de ruta:**
    - sala_id: identificador de la sala a eliminar

    **Respuestas:**
    - 204 No Content: Sala eliminada exitosamente
    - 404 Not Found: La sala no existe
    """
    SalaService.eliminar_sala(db, sala_id)
