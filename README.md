# Secure FastAPI MySQL CRUD API 🚀

A production-ready, highly secure RESTful CRUD API built with **FastAPI**, **SQLAlchemy ORM**, and **MySQL**. This project demonstrates industry-standard security practices, including stateless JWT authentication, advanced password hashing, role-based authorization, and secure file handling.

## ✨ Features

- **Full CRUD Architecture:** Standardized REST endpoints for Creating, Reading, Updating, and Deleting user profiles.
- **Enterprise-Grade Cryptography:** Implements **Argon2id** (via `pwdlib`) for unbreakable password hashing.
- **Stateless Authentication:** Secure login system generating **JWT Access Tokens** with automatic expiration.
- **Role-Based Access Control (RBAC):** Restricts specific operations (e.g., viewing all users) exclusively to `admin` accounts.
- **Secure File Uploads:** Supports profile picture uploads using `multipart/form-data` with strict image-only validation.
- **Automated DB Schema Synchronization:** SQL generation driven directly by SQLAlchemy ORM.

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Authentication:** PyJWT & OAuth2
- **Password Hashing:** Argon2id
- **Server:** Uvicorn

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com
cd fastapi-mysql-secure-crud
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup MySQL Database
- Open MySQL Workbench or your favorite SQL client.
- Create a database named `test`.
- Update the `DATABASE_URL` in `practice.py` with your actual MySQL username and password:
```python
DATABASE_URL = "mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost:3306/test"
```

### 4. Start the Application Server
```bash
uvicorn practice:app --reload
```

### 5. Access Interactive API Docs
Once the server is running, open your browser and navigate to:
- Swagger UI Docs: `http://127.0.0`

## 🔒 API Endpoints & Security Matrix

| Method | Endpoint | Description | Auth Required | Access Level |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/amil` | User Registration / Signup | ❌ No | Public |
| **POST** | `/login` | User Login (Returns JWT) | ❌ No | Public |
| **GET** | `/profile/{user_id}` | View User Profile |  Yes (JWT) | Owner Only |
| **PATCH**| `/profile/{user_id}` | Update Profile Data |  Yes (JWT) | Owner Only |
| **POST** | `/upload` | Upload Profile Picture |  Yes (JWT) | Owner Only |
| **DELETE**| `/profile/{user_id}`| Delete Account |  Yes (JWT) | Owner Only |
| **GET** | `/admin/all-users` | Fetch All Registered Users |  Yes (JWT) | Admin Only |
