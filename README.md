# VINdex

Vehicle Inventory with FastAPI + SQLAlchemy + SQLite

## How to start/Set up

```bash
uv sync                                     
uv run uvicorn vindex.main:app --reload      
```

## Endpoints

| Method | Path             | Status | Description        |
|--------|------------------|--------|--------------------|
| GET    | `/vehicle`       | 200    | List all vehicles  |
| POST   | `/vehicle`       | 201    | Create vehicle     |
| GET    | `/vehicle/{vin}` | 200    | Get vehicle by VIN |
| PUT    | `/vehicle/{vin}` | 200    | Update vehicle     |
| DELETE | `/vehicle/{vin}` | 204    | Delete vehicle     |

### Error Codes

| Status | Trigger                                 |
|--------|-----------------------------------------|
| 400    | Malformed JSON body                     |
| 404    | VIN not found                           |
| 409    | Duplicate VIN on create                 |
| 422    | Validation error                        |

## Design Decisions

### Money as Cents

**Why:** Floats are weird with money like with `0.1 + 0.2` doesn't actually equal `0.3` because of how computers store decimals. So Im storing everything as cents as integers to avoid those rounding errors. Pydantic handles converting between dollars and cents automatically.

### VIN Normalization

VINs get automatically converted to uppercase when you submit them. Searches are case-insensitive.

**Why:** VINs are case-insensitive.

### Custom Exceptions

Domain exceptions like (`VehicleNotFoundError`, `VehicleAlreadyExistsError`) are raised by the repository and caught by FastAPI exception handlers.

**Why:** Separates the business logic from the API layer.

### Repository Pattern

All database operations go through `VehicleRepository`.

**Why:** Single place for all database access.

### pydantic-settings

Configuration via `pydantic-settings` with `.env` file support.

**Why:** FastAPI already uses Pydantic, so `pydantic-settings` is just a natural fit.

## Project Structure

```
src/vindex/
├── main.py             
├── api/routes.py        
├── core/
│   ├── config.py        
│   ├── database.py      
│   └── exceptions.py    
├── models/vehicle.py    
├── repository/vehicle.py 
└── schemas/vehicle.py   
```

## Testing

```bash
uv run pytest tests/ -v         
uv run pytest --cov=vindex
```

**15 tests** (6 unit, 9 integration).

## Tooling

| Tool       | Purpose                                            |
|------------|----------------------------------------------------|
| **uv**     | Fast Python package manager                        |
| **Hatch**  | Project bootstrapping                              |
| **Ruff**   | Linting + formatting                               |
| **pytest** | Testing framework                                  |

## Configuration

Set `DATABASE_URL` in `.env` or environment
