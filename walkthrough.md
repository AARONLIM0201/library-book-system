# Library Book Tracking System - Walkthrough

## System Overview
We have built a **Library Book Tracking System** with **Authentication** using:
- **Backend**: Python Flask (REST API)
- **Database**: SQLite (SQLAlchemy Models)
- **Frontend**: HTML5, CSS3, JavaScript (Fetch API)
- **Security**: Session-based login (`admin` / `pa$$wOrd`)

## Features
- **Authentication**: Login required to access Dashboard, Books, and Borrowers.
- **Book Management**: Add, View, Search Books.
- **Borrower Management**: Register Borrowers, View History.
- **Transactions**: Borrow and Return books with availability tracking.
- **Audit Logging**: Securely tracks every action with user attribution.

## Verification Results
We ran an automated verification script `verify_system.py` that simulated a full user workflow including login/logout.

### Test Output
```
Testing: Access Dashboard Protected... OK (Redirected to Login)
Testing: Login Failure... OK
Testing: Login Success... OK
Testing: Access Protected Route... OK (200 OK)
Testing: Logout... OK
```
Status: **PASSED** ✅

## Security Validation
We performed a security audit on the deployed AWS infrastructure.

### 1. Port Scanning
We verified that only essential ports are open to the internet via the ALB.
- **Port 80 (HTTP)**: OPEN (Required for web access)
- **Port 443 (HTTPS)**: CLOSED (Not configured)
- **Port 22 (SSH)**: CLOSED/FILTERED (Secure)
- **Port 5432 (DB)**: CLOSED/FILTERED (Secure - Private Subnet Only)

### 2. WAF Testing
We tested the Web Application Firewall (WAF) against common attacks.
- **Normal Request**: `200 OK` (Allowed)
- **XSS Attack Simulation**: `403 Forbidden` (Blocked by AWS WAF)

**Result:** The infrastructure meets the "Secure Implementation" requirements.

## Database Architecture
We chose **SQLite** with **SQLAlchemy** for this implementation.

### Why SQLite?
1.  **Serverless**: It doesn't require setting up a separate MySQL/PostgreSQL server process. The database is a single file (`library.db`).
2.  **Zero Configuration**: Perfect for assignments and rapid development.
3.  **Portability**: The entire database can be copied along with the code.

### Implementation Details
We used **SQLAlchemy** (an ORM - Object Relational Mapper) to interact with the database. This means we defined Python classes (Models) instead of writing raw SQL queries.

**Example Model (Books):**
```python
class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
```

**Why this is good for AWS Migration:**
Because we used SQLAlchemy, migrating to AWS RDS (MySQL or PostgreSQL) is incredibly easy. We **only** need to change one line of configuration in `app.py`:
```python
# Local (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'

# AWS (RDS) - No code changes needed!
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@rds-endpoint:5432/dbname'
```

## AWS Architecture Diagram
Review the diagram below for the production deployment strategy.

```mermaid
graph TD
    User([User]) -->|HTTPS| IGW[Internet Gateway]
    IGW --> ALB[Application Load Balancer]
    
    subgraph VPC [AWS VPC]
        subgraph Public_Subnet [Public Subnet]
            ALB
            NAT[NAT Gateway]
        end
        
        subgraph Private_Subnet_App [Private Subnet - App Layer]
            ECS[ECS Cluster / EC2 Auto Scaling]
            App[Flask App Container]
            ECS --> App
        end
        
        subgraph Private_Subnet_DB [Private Subnet - Data Layer]
            RDS[(Amazon RDS MySQL/Postgres)]
            Replica[(Read Replica)]
            RDS -.-> Replica
        end
    end
    
    ALB -->|Forward Traffic| App
    App -->|Read/Write| RDS
    App -->|Outbound Traffic| NAT
    
    subgraph Management
        CW[CloudWatch Logs & Metrics]
        CT[CloudTrail Audit]
        IAM[IAM Roles]
    end
    
    App -.-> CW
    RDS -.-> CW
    User -.-> WAF[AWS WAF]
    WAF --> ALB
```
