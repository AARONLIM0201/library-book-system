# Library Book System

A web-based library management system built with Flask for tracking books, borrowers, borrowing/returns, and audit activity through a simple dashboard and REST API.

## Tech Stack
- **Backend:** Python, Flask, Flask Blueprint API
- **Database/ORM:** SQLite, SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript (Fetch API)
- **Containerization:** Docker, Docker Compose
- **Infrastructure (IaC):** Terraform (AWS-focused configs)

## Project Structure
```text
library-book-system/
├── app.py
├── database.py
├── models.py
├── routes.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── LICENSE.txt
├── README.md
├── static/
│   ├── app.js
│   └── style.css
├── templates/
│   ├── layout.html
│   ├── login.html
│   ├── index.html
│   ├── books.html
│   ├── borrowers.html
│   └── audit.html
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── ecs.tf
│   ├── rds.tf
│   ├── ecr.tf
│   ├── security.tf
│   ├── iam.tf
│   ├── logging.tf
│   └── waf.tf
├── docs/
│   ├── implementation_plan.md
│   ├── walkthrough.md
│   └── reports/
│       ├── 26-1-19-CCS6344_2530_Assignment 2.pdf
│       └── TT1L_G22_Assignment 2.pdf
├── verify_system.py
├── security_check.py
└── deploy.ps1
```

## Setup and Run

### 1) Local Python Setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open: `http://localhost:5000`

Default login:
- Username: `admin`
- Password: `pa$$wOrd`

### 2) Run with Docker Compose
```bash
docker-compose up --build
```

Open: `http://localhost:5000`

### 3) Run Basic Verification
```bash
python verify_system.py
```

## Notes
- The app uses SQLite by default (`instance/library.db`).
- Terraform files are included for AWS infrastructure provisioning and deployment architecture.
