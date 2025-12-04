from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

app = FastAPI()

# 1. OPTIMAL CORS SETUP (Connects to Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. DATABASE HELPER (Raw SQL for speed, or swap for ORM)
DB_NAME = "../database/app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # EXAMPLE TABLE - Replace this during interview
    conn.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

# 3. HEALTH CHECK (Frontend verifies this first)
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is ready"}

# 4. EXAMPLE ENDPOINT
@app.get("/items")
def read_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return items
