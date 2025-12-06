from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to db
DB_NAME = "../database/app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME) # db connection object
    conn.row_factory = sqlite3.Row # maps database rows to Python dictionaries
    return conn

def init_db():
    conn = get_db_connection()
    # EXAMPLE TABLE - Replace this during interview
    # Sqlite uses raw SQL for speed and syntax (swap for ORM)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit() # confirms changes to the database
    conn.close() # closes the connection to the database

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
