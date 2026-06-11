# Sistema de Reservas de Salas - API REST CRUD

## Descripción

API REST completa para gestionar reservas y disponibilidad de salas de conferencias. Implementa operaciones CRUD con validaciones robustas, manejo de errores y documentación interactiva.

## Estructura del Proyecto

```
proyecto/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Aplicación FastAPI principal
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py             # Enrutador principal v1
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── sala.py        # Endpoints de Salas
│   ├── core/
│   │   ├── __init__.py
│   │   └── database.py            # Configuración de BD
│   ├── models/
│   │   ├── __init__.py
│   │   └── sala.py                # Modelo SQLAlchemy
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── sala.py                # Esquemas Pydantic
│   ├── repository/
│   │   ├── __init__.py
│   │   └── sala_repository.py     # Capa de repositorio
│   └── services/
│       ├── __init__.py
│       └── sala_service.py        # Capa de servicios
├── tests/
│   ├── __init__.py
│   └── test_sala.py               # Suite de tests
├── requirements.txt               # Dependencias
└── README.md                      # Este archivo
```

## Instalación

### Requisitos previos
- Python 3.10+
- pip

### Pasos

1. Clonar el repositorio
```bash
git clone <repo-url>
cd Proyecto-1
```

2. Instalar dependencias
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación
```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`

## Endpoints

### 1. Obtener todas las salas
```http
GET /api/v1/salas?skip=0&limit=10
```

**Parámetros de consulta:**
- `skip`: Número de registros a saltar (default: 0)
- `limit`: Número máximo de registros (default: 10, máximo: 100)

**Respuesta (200 OK):**
```json
{
  "total": 15,
  "skip": 0,
  "limit": 10,
  "items": [
    {
      "id": 1,
      "nombre": "Sala de Conferencias A",
      "capacidad": 20,
      "ubicacion": "Piso 3, Ala Norte",
      "equipamiento": "Proyector, Pizarra digital",
      "disponible": true,
      "razon_indisponibilidad": null,
      "created_at": "2026-06-11T16:00:00Z",
      "updated_at": "2026-06-11T16:00:00Z"
    }
  ]
}
```

### 2. Obtener sala por ID
```http
GET /api/v1/salas/{sala_id}
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "nombre": "Sala de Conferencias A",
  "capacidad": 20,
  "ubicacion": "Piso 3, Ala Norte",
  "equipamiento": "Proyector, Pizarra digital",
  "disponible": true,
  "razon_indisponibilidad": null,
  "created_at": "2026-06-11T16:00:00Z",
  "updated_at": "2026-06-11T16:00:00Z"
}
```

### 3. Crear nueva sala
```http
POST /api/v1/salas
Content-Type: application/json

{
  "nombre": "Sala de Conferencias A",
  "capacidad": 20,
  "ubicacion": "Piso 3, Ala Norte",
  "equipamiento": "Proyector, Pizarra digital, Videoconferencia"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "nombre": "Sala de Conferencias A",
  "capacidad": 20,
  "ubicacion": "Piso 3, Ala Norte",
  "equipamiento": "Proyector, Pizarra digital, Videoconferencia",
  "disponible": true,
  "razon_indisponibilidad": null,
  "created_at": "2026-06-11T16:00:00Z",
  "updated_at": "2026-06-11T16:00:00Z"
}
```

### 4. Actualizar sala
```http
PUT /api/v1/salas/{sala_id}
Content-Type: application/json

{
  "nombre": "Sala de Conferencias A (Actualizada)",
  "capacidad": 25,
  "disponible": false,
  "razon_indisponibilidad": "En mantenimiento"
}
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "nombre": "Sala de Conferencias A (Actualizada)",
  "capacidad": 25,
  "ubicacion": "Piso 3, Ala Norte",
  "equipamiento": "Proyector, Pizarra digital, Videoconferencia",
  "disponible": false,
  "razon_indisponibilidad": "En mantenimiento",
  "created_at": "2026-06-11T16:00:00Z",
  "updated_at": "2026-06-11T16:30:00Z"
}
```

### 5. Eliminar sala
```http
DELETE /api/v1/salas/{sala_id}
```

**Respuesta (204 No Content):**
```
(sin contenido)
```

## Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - Operación exitosa |
| 201 | Created - Recurso creado |
| 204 | No Content - Eliminación exitosa |
| 400 | Bad Request - Parámetros inválidos |
| 404 | Not Found - Recurso no encontrado |
| 409 | Conflict - Nombre duplicado |
| 422 | Unprocessable Entity - Validación fallida |

## Validaciones

### Campo: nombre
- ✅ Requerido
- ✅ Máximo 100 caracteres
- ✅ Único en la base de datos
- ✅ No puede ser vacío o solo espacios en blanco

### Campo: capacidad
- ✅ Requerido
- ✅ Mínimo: 1 persona
- ✅ Máximo: 500 personas

### Campo: ubicacion
- ✅ Requerido
- ✅ Máximo 255 caracteres

### Campo: equipamiento
- ✅ Opcional (default: "Básico")
- ✅ Máximo 500 caracteres

### Campo: disponible
- ✅ Booleano (default: true)

### Campo: razon_indisponibilidad
- ✅ Opcional
- ✅ Máximo 255 caracteres
- ✅ Recomendado cuando disponible=false

## Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

Ejecutar suite de tests completa:
```bash
pytest tests/ -v
```

Coberturas implementadas:
- ✅ Crear sala válida
- ✅ No permitir sala duplicada
- ✅ Obtener todas las salas con paginación
- ✅ Actualizar una sala
- ✅ Eliminar una sala
- ✅ Validación de capacidad
- ✅ Validación de nombre vacío
- ✅ GET de sala inexistente
- ✅ PUT de sala inexistente
- ✅ DELETE de sala inexistente
- ✅ Parámetros de paginación inválidos
- ✅ Sala indisponible con razón
- ✅ Health check
- ✅ Endpoints raíz

## Patrón Arquitectónico

Se utiliza el patrón **Repository-Service-Controller**:

1. **Models** (SQLAlchemy): Define la estructura de datos
2. **Schemas** (Pydantic): Validación y serialización
3. **Repository**: Capa de acceso a datos
4. **Service**: Lógica de negocio
5. **Endpoints**: Exposición HTTP

## Stack Tecnológico

- **Framework**: FastAPI 0.104.1
- **Web Server**: Uvicorn 0.24.0
- **ORM**: SQLAlchemy 2.0.23
- **Validación**: Pydantic v2 2.5.0
- **Testing**: pytest 7.4.3
- **Base de datos**: SQLite

## Autores

Equipo de desarrollo - 2026

## Licencia

MIT
