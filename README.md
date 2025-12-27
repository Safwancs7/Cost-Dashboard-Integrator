# AWS Cost Dashboard Integrator

## 📌 Overview
The **AWS Cost Dashboard Integrator** is a backend utility that aggregates AWS resource and cost data stored in a PostgreSQL database and exposes it in a structured JSON format suitable for frontend dashboards.

The project demonstrates:
- Database querying and joins
- Cost aggregation logic
- Backend-to-frontend data contracts
- JSON-based API design

This solution supports both:
- JSON file generation
- REST API exposure using Flask

---

## 🎯 Objectives
- Query multiple PostgreSQL tables (`aws_resources`, `aws_costs`, `top_cost_resources`)
- Aggregate AWS cost data by service, subscription, and time
- Generate frontend-friendly structured JSON
- Provide the data via an API or static JSON file

---

## 🛠 Tech Stack
- **Python 3.9+**
- **PostgreSQL**
- **psycopg2-binary**
- **Flask**

---

## 📂 Project Structure
.
├── cost_dashboard.py # Core data aggregation logic
├── app.py # Flask API server
├── cost_dashboard.json # Generated sample JSON output
├── README.md # Project documentation

---

## 🗄 Database Schema Assumptions

### aws_resources
| Column | Type | Description |
|------|------|-------------|
| resource_id | VARCHAR | Unique AWS resource ID |
| resource_name | TEXT | Human-readable resource name |
| service_type | TEXT | AWS service (EC2, S3, etc.) |
| subscription_id | TEXT | AWS subscription/account |

### aws_costs
| Column | Type | Description |
|------|------|-------------|
| id | SERIAL | Primary key |
| resource_id | VARCHAR | Linked resource ID |
| cost | NUMERIC | Cost incurred |
| usage_date | DATE | Date of usage |

### top_cost_resources
| Column | Type | Description |
|------|------|-------------|
| resource_id | VARCHAR | Resource ID |
| total_cost | NUMERIC | Aggregated total cost |

> ⚠️ Note: If your schema differs, adjust SQL queries accordingly.

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/aws-cost-dashboard.git
cd aws-cost-dashboard
```
### 2️⃣ Create Virtual Environment (Recommended)
```
python -m venv venv
```
Activate:
```
python -m venv venv
```
- Windows:
```
venv\Scripts\activate
```
- Linux/Mac
```
source venv/bin/activate
```
### 3️⃣ Install Dependencies
```
pip install psycopg2-binary flask
```
### 4️⃣ Configure Database Connection
Edit DB_CONFIG in cost_dashboard.py:
```python
DB_CONFIG = {
    "host": "localhost",
    "database": "aws_cost_db",
    "user": "postgres",
    "password": "your_password",
    "port": 5432
}
```
Ensure PostgreSQL is running.
---
### ▶️ Running the Project
Option 1: Generate JSON File
```
python cost_dashboard.py
```
Output:
```pgsql
cost_dashboard.json
```
Option 2: Run Flask API
```
python app.py
```
API Endpoint:
```nginx
GET http://127.0.0.1:5000/api/cost-dashboard
```




