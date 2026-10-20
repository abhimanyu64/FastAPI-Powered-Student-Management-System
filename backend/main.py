from pathlib import Path
import sqlite3
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "students.db"

app = FastAPI(title="Student Database API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=150)
    course: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1, le=8)


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[str] = Field(default=None, min_length=3, max_length=150)
    course: Optional[str] = Field(default=None, min_length=1, max_length=100)
    year: Optional[int] = Field(default=None, ge=1, le=8)


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS students (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                course TEXT NOT NULL,
                year INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
def set_starting_student_id():
    with connect() as db:
        existing = db.execute(
            "SELECT MAX(id) FROM students"
        ).fetchone()[0]

        if existing is None:
            db.execute(
                "DELETE FROM sqlite_sequence WHERE name = 'students'"
            )
            db.execute(
                "INSERT INTO sqlite_sequence (name, seq) VALUES ('students', 500)"
            )

@app.on_event("startup")
def startup():
    initialize_database()
    set_starting_student_id()


def row_to_dict(row):
    return dict(row) if row else None


@app.get("/health")
def health():
    return {"status": "ok", "message": "Student Database API is running"}


@app.get("/students")
def list_students(search: str = Query(default="", max_length=150)):
    with connect() as db:
        if search.strip():
            pattern = f"%{search.strip()}%"
            rows = db.execute(
                """SELECT * FROM students
                   WHERE name LIKE ? OR email LIKE ? OR course LIKE ?
                   ORDER BY id DESC""",
                (pattern, pattern, pattern),
            ).fetchall()
        else:
            rows = db.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    return [row_to_dict(row) for row in rows]


@app.get("/students/{student_id}")
def get_student(student_id: int):
    with connect() as db:
        row = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return row_to_dict(row)


@app.post("/students", status_code=201)
def create_student(student: StudentCreate):
    try:
        with connect() as db:
            cursor = db.execute(
                "INSERT INTO students (name, email, course, year) VALUES (?, ?, ?, ?)",
                (student.name.strip(), student.email.strip().lower(), student.course.strip(), student.year),
            )
            row = db.execute("SELECT * FROM students WHERE id = ?", (cursor.lastrowid,)).fetchone()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="A student with this email already exists")
    return row_to_dict(row)


@app.put("/students/{student_id}")
def replace_student(student_id: int, student: StudentCreate):
    try:
        with connect() as db:
            cursor = db.execute(
                """UPDATE students SET name = ?, email = ?, course = ?, year = ?
                   WHERE id = ?""",
                (student.name.strip(), student.email.strip().lower(), student.course.strip(), student.year, student_id),
            )
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Student not found")
            row = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="A student with this email already exists")
    return row_to_dict(row)


@app.patch("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    updates = student.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided to update")
    if "email" in updates and updates["email"] is not None:
        updates["email"] = updates["email"].strip().lower()
    if "name" in updates and updates["name"] is not None:
        updates["name"] = updates["name"].strip()
    if "course" in updates and updates["course"] is not None:
        updates["course"] = updates["course"].strip()
    columns = ", ".join(f"{key} = ?" for key in updates)
    values = list(updates.values()) + [student_id]
    try:
        with connect() as db:
            cursor = db.execute(f"UPDATE students SET {columns} WHERE id = ?", values)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Student not found")
            row = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="A student with this email already exists")
    return row_to_dict(row)


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    with connect() as db:
        cursor = db.execute("DELETE FROM students WHERE id = ?", (student_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
