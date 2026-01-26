# Implementation Plan - Library Book Tracking System

We have completed the **Legacy App** and **Docker Containerization**. We are now moving to **Phase 3: AWS Infrastructure**.

## User Review Required

> [!IMPORTANT]
> **Infrastructure as Code (IaC)**: We will use **Terraform** to define our AWS resources. This fulfills the "Part D" requirement of the assignment.
> **Note**: We will write the code, but *running* `terraform apply` requires active AWS credentials. For the report, showing the *code* and the *plan* is usually sufficient if you don't have a live AWS account to spend money on.

## Proposed Changes

### AWS Infrastructure (Terraform)
We will create a `terraform/` directory with the following files:

#### [NEW] [terraform/main.tf](file:///c:/Users/Aaron Lim/.gemini/antigravity/playground/Library Book Tracking System/terraform/main.tf)
- Defines the **Provider** (AWS).
- Defines **VPC**, **Subnets** (Public/Private), and **Internet Gateway**.
- Defines **Security Groups** (Firewalls).

#### [NEW] [terraform/rds.tf](file:///c:/Users/Aaron Lim/.gemini/antigravity/playground/Library Book Tracking System/terraform/rds.tf)
- Defines the **RDS Instance** (PostgreSQL/MySQL).
- Configures it to be in the *Private Subnet* (Security Best Practice).

#### [NEW] [terraform/ecs.tf](file:///c:/Users/Aaron Lim/.gemini/antigravity/playground/Library Book Tracking System/terraform/ecs.tf)
- Defines the **ECS Cluster** and **Fargate Task**.
- Defines the **Application Load Balancer (ALB)** to accept public traffic.

#### [NEW] [terraform/variables.tf](file:///c:/Users/Aaron Lim/.gemini/antigravity/playground/Library Book Tracking System/terraform/variables.tf)
- clean way to manage settings like Region, Instance Type, and Database Name.

## Verification Plan
- **Syntax Check**: Run `terraform validate` (requires Terraform installed) or manually review the code structure.
- **Assignment alignment**: ensuring we hit all rubric points:
    - [x] VPC with Public/Private subnets
    - [x] Application/Database separation
    - [x] Load Balancing
    - [x] IAM Roles
