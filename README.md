
# ACEest Fitness & Gym — Flask + HTML Form + Pytest + Docker + GitHub Actions

This project demonstrates a foundational fitness/gym management system with:
- Flask web backend (`app.py`)
- HTML homepage with workout form (`templates/index.html`)
- REST APIs for workouts (JSON)
- Pytest tests (`tests/`)
- Dockerfile for containerization
- GitHub Actions CI/CD pipeline

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Visit `http://localhost:5000/` for the HTML homepage.

## Run tests
```bash
pytest -q
```

## Docker
```bash
docker build -t aceest-fitness-app:dev .
docker run --rm -p 5000:5000 aceest-fitness-app:dev
```

## GitHub Actions (CI/CD Pipeline)

This project uses a two-stage GitHub Actions workflow defined in `.github/workflows/ci.yml`:

1. **Unit Tests (Host Environment)**
   - Checks out the repo
   - Sets up Python 3.10
   - Installs dependencies
   - Runs `pytest` directly on the runner

2. **Docker Tests (Containerized Environment)**
   - Builds a Docker image using the `Dockerfile`
   - Runs `pytest` inside the container

✅ If both jobs succeed, the workflow is marked green.  
⚠️ If either job fails, the workflow is marked red and logs will show which step failed.

This ensures:
- Code works in a standard Python environment
- Code works reliably inside a production-like Docker container

**Benefit:** This double testing strategy reduces "works on my machine" issues and validates both code and container reliability before deployment.

