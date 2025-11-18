# 📝 To-Do Task Manager (Django, DRF, & Raw SQL)

This is a clean, fully-functional Task Management System designed to demonstrate a **Django/Django REST Framework (DRF)** application built exclusively on **Raw SQL** for all database interactions. It completely bypasses the Django ORM, making it an ideal project for understanding database isolation, manual API development, and clean architecture principles.

## 🚀 Features Highlights

| Feature Area       | Description                                                                                                                                                                    |
| :----------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Database Layer** | **Raw SQL Only:** All CRUD operations (Insert, Update, Delete, Fetch) are implemented using raw SQL queries within a dedicated `db.py` module. No Django ORM methods are used. |
| **Backend**        | **Django REST Framework (DRF):** Implements a full RESTful API using manual `APIView` classes and DRF Serializers. **No generic views or ViewSets** are utilized.              |
| **Frontend**       | **Bootstrap 5 UI:** Provides a responsive, modern web interface for managing tasks, including List, Add, and Edit pages.                                                       |
| **Testing**        | **Pytest & Isolation:** Comprehensive test suite using `pytest`. Each test uses a temporary, isolated SQLite database to ensure clean, repeatable results.                     |

## 📦 Tech Stack

| Category     | Tool / Framework                                                       |
| :----------- | :--------------------------------------------------------------------- |
| **Backend**  | Python, Django, Django REST Framework (DRF)                            |
| **Database** | SQLite (using standard Python `sqlite3` library for raw SQL execution) |
| **Frontend** | HTML, CSS, JavaScript, Bootstrap 5                                     |
| **Testing**  | Pytest, `pytest-django`, `monkeypatch`                                 |

## ⚙️ Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

- Python 3.8+

### 1\. Clone the Repository

```bash
git clone https://github.com/<your-username>/TODO.git
cd TODO
```

### 2\. Setup Virtual Environment

It is highly recommended to use a virtual environment.

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install Dependencies

Install all required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4\. Run the Server

The application will automatically initialize the SQLite database and create the `tasks` table upon startup.

```bash
python manage.py runserver
```

The application will be accessible at:

- **Web UI:** `http://127.0.0.1:8000/`
- **API Root:** `http://127.0.0.1:8000/api/tasks/`

---

## 🔗 REST API Endpoints

The API is fully functional for CRUD operations using raw SQL.

| Method     | Endpoint           | Description                                    |
| :--------- | :----------------- | :--------------------------------------------- |
| **GET**    | `/api/tasks/`      | List all tasks.                                |
| **POST**   | `/api/tasks/`      | Create a new task.                             |
| **GET**    | `/api/tasks/<id>/` | Retrieve a single task by ID.                  |
| **PUT**    | `/api/tasks/<id>/` | Fully update all fields of a task.             |
| **PATCH**  | `/api/tasks/<id>/` | Partially update one or more fields of a task. |
| **DELETE** | `/api/tasks/<id>/` | Delete a task by ID.                           |

### Example POST Request Body

To create a new task:

```json
{
  "title": "Learn Django",
  "description": "Practice raw SQL implementation for the database layer.",
  "due_date": "2025-12-31",
  "status": "pending"
}
```

---

## 🎨 Web UI Pages

The user interface is built with Bootstrap 5 and provides a complete visual experience for managing tasks.

| Page          | URL           | Description                                                    |
| :------------ | :------------ | :------------------------------------------------------------- |
| **Task List** | `/`           | The main dashboard displaying all tasks in a responsive table. |
| **Add Task**  | `/add/`       | Form to create a new task.                                     |
| **Edit Task** | `/edit/<id>/` | Form to modify an existing task's details.                     |

**UI Features:**

- Modern and responsive Bootstrap styling.
- Intuitive forms for adding and editing tasks.
- **AJAX-powered Delete:** Tasks are deleted directly from the list page using JavaScript/Fetch API calls to the REST endpoint.

---

## 📦 Raw SQL Database Layer (`db.py`)

All database logic is strictly isolated within the `todo_app/db.py` file. This demonstrates a clear separation of concerns, keeping the view and API logic clean.

The key functions implemented are:

- `create_tasks_table()`
- `insert_task(data)`
- `fetch_all_tasks()`
- `fetch_task(id)`
- `update_task(id, data)`
- `delete_task(id)`

**This is the core architecture of the project: Views call `db.py`, and `db.py` executes SQL.**

---

## 🧪 Running Tests (Pytest)

The project includes a robust test suite to ensure the stability of both the API and the underlying SQL logic.

### Running All Tests

```bash
pytest -v
```

### Test Philosophy

1.  **Isolation:** Each test case runs in isolation.
2.  **Temporary Database:** Pytest fixtures are used alongside `monkeypatch` to dynamically inject a **temporary SQLite database file** before each test runs.
3.  **Cleanup:** The temporary database file is deleted immediately after the test completes.
