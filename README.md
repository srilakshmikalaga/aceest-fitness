# ACEest Fitness & Gym Management System

## Overview
This project is a **Flask-based fitness & gym management system** developed as part of the **Introduction to DevOps Assignment**.  
It demonstrates modern DevOps practices including:

- Flask application development  
- Git & GitHub version control  
- Automated testing with Pytest  
- Containerization using Docker  
- CI/CD pipeline implementation with GitHub Actions  

---

## Features
- Add new workouts with duration  
- Update existing workouts  
- Track statistics (total, average, longest, shortest workout)  
- Search workouts  
- Responsive HTML UI with inline CSS  
- REST APIs for integration  

---

## Tech Stack
- **Backend:** Python 3.10, Flask  
- **Testing:** Pytest  
- **Containerization:** Docker  
- **CI/CD:** GitHub Actions  
- **Version Control:** Git + GitHub  

---

## Project Structure
```
.
├── .github
│ └── workflows
│  └── ci.yml # GitHub Actions CI/CD pipeline
├── app
│ ├── init.py # Flask app with routes & logic
│ ├── main.py # Entry point when using python -m app
│ └── templates
│  └── index.html # UI for workouts
├── tests
│ └── test_app.py # Unit test cases (≈16 tests)
├── .gitignore
├── conftest.py # Pytest fixtures (e.g., test client)
├── Dockerfile # Docker container configuration
├── README.md # Documentation (this file)
└── requirements.txt # Python dependencies
```
---

## Local Setup & Usage

### 1) Clone Repository
```bash
git clone https://github.com/srilakshmikalaga/aceest-fitness.git
cd aceest-fitness
```

### 2) Setup Virtual Environment (recommended)
```bash
sudo apt install python3.10-venv   # if not installed
python3 -m venv .venv
source .venv/bin/activate
```

Alternatively (not recommended for shared systems), install globally:
```bash
pip3 install -r requirements.txt
```

### 3) Install Dependencies
```bash
pip install -r requirements.txt
```

### 4) Run the Application
```bash
flask --app app run
# or
python main.py
```
Visit: http://127.0.0.1:5000

---

## Running Tests (Locally)
```bash
pytest -q
```
Expected:

~16 tests run

All tests pass ✅

---

## Docker Setup

### Build Image
```bash
sudo docker build -t aceest-fitness .
```

### Run Application in Docker
```bash
sudo docker run -p 5000:5000 aceest-fitness
```
Visit: http://localhost:5000

### Run Tests in Docker
```bash
sudo docker run --rm aceest-fitness pytest -q
```
⚠️ If you get a Docker permission error, add your user to the docker group:
```bash
sudo usermod -aG docker $USER
# log out/in or reboot
```

---

## CI/CD with GitHub Actions
A fully automated pipeline lives in `.github/workflows/ci.yml` and runs on every push/PR:

1. Checkout source  
2. Build Docker image (`aceest-fitness`)  
3. Run Pytest inside Docker  

✅ Pass if tests succeed  
❌ Fail otherwise  

Check runs under the **Actions** tab in your GitHub repo.

---

## Author
**K N S  Srilakshmi**
