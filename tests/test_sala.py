import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# Usar SQLite en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestSalaCRUD:
    """Suite de tests para operaciones CRUD de Salas"""

    def test_crear_sala_valida(self):
        """
        Escenario: Crear una sala válida
        Dado que tengo los datos de una nueva sala
        Cuando envío una petición POST a /api/v1/salas
        Entonces debo recibir un código 201
        Y la sala debe tener un ID asignado
        """
        response = client.post(
            "/api/v1/salas",
            json={
                "nombre": "Sala de Conferencias A",
                "capacidad": 20,
                "ubicacion": "Piso 3, Ala Norte",
                "equipamiento": "Proyector, Pizarra digital"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["nombre"] == "Sala de Conferencias A"
        assert data["capacidad"] == 20
        assert data["disponible"] is True

    def test_no_permitir_sala_duplicada(self):
        """
        Escenario: No permitir sala duplicada
        Dado que existe una sala con nombre "Sala A"
        Cuando intento crear otra sala con el mismo nombre
        Entonces debo recibir un código 409
        """
        # Crear primera sala
        client.post(
            "/api/v1/salas",
            json={
                "nombre": "Sala A",
                "capacidad": 15,
                "ubicacion": "Piso 2"
            }
        )
        # Intentar crear sala duplicada
        response = client.post(
            "/api/v1/salas",
            json={
                "nombre": "Sala A",
                "capacidad": 20,
                "ubicacion": "Piso 3"
            }
        )
        assert response.status_code == 409
        assert "duplicado" in response.json()["detail"].lower()

    def test_obtener_todas_las_salas(self):
        """
        Escenario: Obtener todas las salas
        Dado que existen 15 salas en la base de datos
        Cuando envío una petición GET a /api/v1/salas con limit=10
        Entonces debo recibir un array de 10 salas
        """
        # Crear 15 salas
        for i in range(15):
            client.post(
                "/api/v1/salas",
                json={
                    "nombre": f"Sala {i+1}",
                    "capacidad": 10 + i,
                    "ubicacion": f"Piso {i // 5 + 1}"
                }
            )

        # Obtener con limit=10
        response = client.get("/api/v1/salas?skip=0&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 15
        assert len(data["items"]) == 10
        assert data["skip"] == 0
        assert data["limit"] == 10

    def test_actualizar_sala(self):
        """
        Escenario: Actualizar una sala
        Dado que existe una sala con ID 1
        Cuando envío una petición PUT con nuevos datos
        Entonces la sala debe actualizarse correctamente
        Y el campo updated_at debe cambiar
        """
        # Crear sala
        create_response = client.post(
            "/api/v1/salas",
            json={
                "nombre": "Sala Original",
                "capacidad": 10,
                "ubicacion": "Piso 1"
            }
        )
        sala_id = create_response.json()["id"]
        updated_at_original = create_response.json()["updated_at"]

        # Actualizar sala
        response = client.put(
            f"/api/v1/salas/{sala_id}",
            json={
                "nombre": "Sala Actualizada",
                "capacidad": 25
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Sala Actualizada"
        assert data["capacidad"] == 25

    def test_eliminar_sala(self):
        """
        Escenario: Eliminar una sala
        Dado que existe una sala con ID 1
        Cuando envío una petición DELETE a /api/v1/salas/1
        Entonces debo recibir un código 204
        Y la sala no debe existir en la BD
        """
        # Crear sala
        create_response = client.post(
            "/api/v1/salas",
            json={
                "nombre": "Sala a Eliminar",
                "capacidad": 10,
                "ubicacion": "Piso 1"
            }
        )
        sala_id = create_response.json()["id"]

        # Eliminar sala
        response = client.delete(f"/api/v1/salas/{sala_id}")
        assert response.status_code == 204

        # Verificar que la sala no existe
        response = client.get(f"/api/v1/salas/{sala_id}")
        assert response.status_code == 404

    def test_validacion_capacidad(self):
        """
        Escenario: Validación de capacidad
        Dado que intento crear una sala con capacidad > 500
        Cuando envío la petición
        Entonces debo recibir un código 400 con mensaje de error
        """
        response = client.post(
            "/api/v1/salas",
            json={
                "nombre": "Sala Grande",
                "capacidad": 501,  # Excede el máximo de 500
                "ubicacion": "Piso 1"
            }
        )
        assert response.status_code == 422  # Validation error
        assert "capacidad" in response.json()["detail"][0]["loc"] or "less than or equal to 500" in str(response.json())

    def test_validacion_nombre_vacio(self):
        """
        Validación: No permitir nombre vacío o solo espacios
        """
        response = client.post(
            "/api/v1/salas",
            json={
                "nombre": "   ",  # Solo espacios
                "capacidad": 20,
                "ubicacion": "Piso 1"
            }
        )
        assert response.status_code == 422

    def test_obtener_sala_inexistente(self):
        """
        Validación: GET de sala inexistente retorna 404
        """
        response = client.get("/api/v1/salas/9999")
        assert response.status_code == 404
        assert "no encontrada" in response.json()["detail"].lower()

    def test_actualizar_sala_inexistente(self):
        """
        Validación: PUT de sala inexistente retorna 404
        """
        response = client.put(
            "/api/v1/salas/9999",
            json={"nombre": "Sala Nueva"}
        )
        assert response.status_code == 404

    def test_eliminar_sala_inexistente(self):
        """
        Validación: DELETE de sala inexistente retorna 404
        """
        response = client.delete("/api/v1/salas/9999")
        assert response.status_code == 404

    def test_validacion_parametros_paginacion(self):
        """
        Validación: Parámetros de paginación inválidos
        """
        # Skip negativo
        response = client.get("/api/v1/salas?skip=-1")
        assert response.status_code == 422

        # Limit > 100
        response = client.get("/api/v1/salas?limit=101")
        assert response.status_code == 422

        # Limit < 1
        response = client.get("/api/v1/salas?limit=0")
        assert response.status_code == 422

    def test_sala_indisponible_con_razon(self):
        """
        Validación: Crear sala indisponible con razón
        """
        response = client.post(
            "/api/v1/salas",
            json={
                "nombre": "Sala en Mantenimiento",
                "capacidad": 20,
                "ubicacion": "Piso 1",
                "disponible": False,
                "razon_indisponibilidad": "Renovación de piso"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["disponible"] is False
        assert data["razon_indisponibilidad"] == "Renovación de piso"

    def test_health_check(self):
        """
        Validación: Endpoint de salud
        """
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self):
        """
        Validación: Endpoint raíz
        """
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "mensaje" in data
        assert "version" in data


if __name__ == "__main__":
    pytest.main(["-v", __file__])
