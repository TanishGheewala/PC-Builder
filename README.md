# PC Builder
## Overview 
PC Builder is a website that takes in a user's budget, preferences, and use case, and recommends the best possible PC components. The goal is to simplify the PC buying and building process, especially for beginners.

>MVP: A one-page website where an user can enter a budget and some basic preferences, and get one recommended, compatible PC build with a total price and per-part breakdown, plus a way to export it.

### Core Features
- Accepts user budget, use case, brand preferences, aesthetic preferences, and other details.
- Generates a recommended build.
- Displays total cost and per-part breakdown.
- Allow users to search for, filter by price and specs, swap parts, and update quantities.
- Allow users to export builds for later.
### Optional Upgrades
- Basic user registration/login, allowing users to view/edit/delete saved builds.
- Display the most popular parts from users.
- Compare two builds side-by-side.
- Live price tracking.
- Build templates.

### Teck Stack
| Layer | Technology |
|---|---|
| Frontend | React + Next.js |
| Backend | FastAPI + Pydantic |
| Database | SQLAlchemy |
| Server | Uvicorn |
| Authentication | Python-Jose + Passlib (JWT) |
| Middleware | CORS + Logging |
| Code Quality | Ruff + Pre-Commit |

## Setup Development Environment

List of virtual enviroment dependencies can be found in `pyproject.toml`.

### Prerequisites
- VS Code with an integrated PowerShell terminal.
- This repository cloned locally.
- Python installed matching `.python-version`.

### Setup Pre-Commit
```powershell
py -m pip install -U pip pre-commit

pre-commit install

pre-commit run --all-files
```

### Setup Virtual Environment

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

uv venv

.venv\Scripts\activate

uv pip install -e ./backend
```
In VS Code, make sure the Python interpreter is set to the one in .venv\scripts\activate

### Authentication
- `python-jose` for JWT creation/verification.
- `passlib` for password hashing.

### Middleware
- CORS to allow the frontend to connect with the backend.
- Request logging.