import sqlite3
import json
from datetime import datetime

DB_PATH = "reports.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            plan TEXT,
            research TEXT,
            summary TEXT,
            report TEXT,
            review TEXT,
            sources TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_report(topic, plan, research, summary, report, review, sources):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reports (topic, plan, research, summary, report, review, sources, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (topic, plan, research, summary, report, review, json.dumps(sources), datetime.now().isoformat()))
    conn.commit()
    report_id = cursor.lastrowid
    conn.close()
    return report_id

def get_all_reports():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, topic, created_at FROM reports ORDER BY id DESC LIMIT 20")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_report_by_id(report_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports WHERE id = ?", (report_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        data = dict(row)
        data["sources"] = json.loads(data["sources"]) if data["sources"] else []
        return data
    return None

def delete_report(report_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reports WHERE id = ?", (report_id,))
    conn.commit()
    conn.close()