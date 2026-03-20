import sqlite3
import os
from datetime import datetime

# ─────────────────────────────────────────
# DATABASE SETUP
# ─────────────────────────────────────────
DB_PATH = 'database/attendance.db'

def get_connection():
    """Get database connection."""
    os.makedirs('database', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Create all tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # ── USERS TABLE ──────────────────────
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT UNIQUE NOT NULL,
            password      TEXT NOT NULL,
            role          TEXT NOT NULL,
            full_name     TEXT NOT NULL,
            email         TEXT,
            created_at    TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ── DEPARTMENTS TABLE ─────────────────
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT UNIQUE NOT NULL,
            code          TEXT UNIQUE NOT NULL
        )
    ''')

    # ── COURSES TABLE ─────────────────────
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            code          TEXT UNIQUE NOT NULL,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
    ''')

    # ── BATCHES TABLE ─────────────────────
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS batches (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            year          INTEGER NOT NULL,
            course_id     INTEGER,
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    ''')

    # ── STUDENTS TABLE ────────────────────
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id    TEXT UNIQUE NOT NULL,
            full_name     TEXT NOT NULL,
            email         TEXT,
            course_id     INTEGER,
            batch_id      INTEGER,
            face_registered INTEGER DEFAULT 0,
            created_at    TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES courses(id),
            FOREIGN KEY (batch_id)  REFERENCES batches(id)
        )
    ''')

    # ── TIMETABLE TABLE ───────────────────
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id     INTEGER,
            batch_id      INTEGER,
            subject       TEXT NOT NULL,
            day_of_week   TEXT NOT NULL,
            start_time    TEXT NOT NULL,
            end_time      TEXT NOT NULL,
            lecturer_id   INTEGER,
            FOREIGN KEY (course_id)   REFERENCES courses(id),
            FOREIGN KEY (batch_id)    REFERENCES batches(id),
            FOREIGN KEY (lecturer_id) REFERENCES users(id)
        )
    ''')

    # ── ATTENDANCE TABLE ──────────────────
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id    TEXT NOT NULL,
            student_name  TEXT NOT NULL,
            course_id     INTEGER,
            batch_id      INTEGER,
            date          TEXT NOT NULL,
            time          TEXT NOT NULL,
            status        TEXT DEFAULT 'Present',
            arrival       TEXT DEFAULT 'On Time',
            marked_by     TEXT,
            session       TEXT,
            created_at    TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES courses(id),
            FOREIGN KEY (batch_id)  REFERENCES batches(id)
        )
    ''')

    # ─────────────────────────────────────
    # INSERT DEFAULT DATA
    # ─────────────────────────────────────

    # Default Admin
    cursor.execute('''
        INSERT OR IGNORE INTO users
        (username, password, role, full_name, email)
        VALUES (?, ?, ?, ?, ?)
    ''', ('admin', 'admin123', 'admin',
          'System Administrator', 'admin@nsbm.ac.lk'))

    # Default Departments
    departments = [
        ('Faculty of Computing',       'FOC'),
        ('Faculty of Business',        'FOB'),
        ('Faculty of Engineering',     'FOE'),
        ('Faculty of Science',         'FOS'),
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO departments (name, code)
        VALUES (?, ?)
    ''', departments)

    # Default Courses
    courses = [
        ('BSc Management Information Systems', 'MIS', 1),
        ('BSc Computer Science',               'CS',  1),
        ('BSc Information Technology',         'IT',  1),
        ('BSc Software Engineering',           'SE',  1),
        ('BSc Business Management',            'BM',  2),
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO courses (name, code, department_id)
        VALUES (?, ?, ?)
    ''', courses)

    # Default Batches
    batches = [
        ('Batch 21', 2021, 1),
        ('Batch 22', 2022, 1),
        ('Batch 23', 2023, 1),
        ('Batch 24', 2024, 1),
        ('Batch 21', 2021, 2),
        ('Batch 22', 2022, 2),
        ('Batch 23', 2023, 2),
        ('Batch 24', 2024, 2),
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO batches (name, year, course_id)
        VALUES (?, ?, ?)
    ''', batches)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

# ─────────────────────────────────────────
# USER FUNCTIONS
# ─────────────────────────────────────────
def verify_user(username, password):
    """Verify login credentials."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users
        WHERE username=? AND password=?
    ''', (username, password))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def add_user(username, password, role, full_name, email=''):
    """Add a new user."""
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users
            (username, password, role, full_name, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password, role, full_name, email))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_all_users():
    """Get all users."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users  = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users

# ─────────────────────────────────────────
# STUDENT FUNCTIONS
# ─────────────────────────────────────────
def add_student(student_id, full_name, email, course_id, batch_id):
    """Add a new student."""
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students
            (student_id, full_name, email, course_id, batch_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (student_id, full_name, email, course_id, batch_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_all_students():
    """Get all students with course and batch info."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.*, c.name as course_name, b.name as batch_name
        FROM students s
        LEFT JOIN courses c ON s.course_id = c.id
        LEFT JOIN batches b ON s.batch_id  = b.id
    ''')
    students = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return students

def get_student_by_id(student_id):
    """Get student by student ID."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.*, c.name as course_name, b.name as batch_name
        FROM students s
        LEFT JOIN courses c ON s.course_id = c.id
        LEFT JOIN batches b ON s.batch_id  = b.id
        WHERE s.student_id = ?
    ''', (student_id,))
    student = cursor.fetchone()
    conn.close()
    return dict(student) if student else None

def update_face_registered(student_id):
    """Mark student face as registered."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE students SET face_registered=1
        WHERE student_id=?
    ''', (student_id,))
    conn.commit()
    conn.close()

# ─────────────────────────────────────────
# COURSE & BATCH FUNCTIONS
# ─────────────────────────────────────────
def get_all_courses():
    """Get all courses."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses')
    courses = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return courses

def get_batches_by_course(course_id):
    """Get batches for a specific course."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM batches WHERE course_id=?
    ''', (course_id,))
    batches = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return batches

def get_all_departments():
    """Get all departments."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM departments')
    departments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return departments

# ─────────────────────────────────────────
# ATTENDANCE FUNCTIONS
# ─────────────────────────────────────────
def mark_attendance(student_id, student_name, course_id,
                    batch_id, arrival, marked_by, session):
    """Mark attendance for a student."""
    today = datetime.now().strftime('%Y-%m-%d')
    time  = datetime.now().strftime('%H:%M:%S')

    # Check duplicate
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id FROM attendance
        WHERE student_id=? AND date=? AND session=?
    ''', (student_id, today, session))

    if cursor.fetchone():
        conn.close()
        return False, "Already marked for this session!"

    cursor.execute('''
        INSERT INTO attendance
        (student_id, student_name, course_id, batch_id,
         date, time, status, arrival, marked_by, session)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (student_id, student_name, course_id, batch_id,
          today, time, 'Present', arrival, marked_by, session))

    conn.commit()
    conn.close()
    return True, "Attendance marked successfully!"

def get_attendance_today():
    """Get today's attendance."""
    today  = datetime.now().strftime('%Y-%m-%d')
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.*, c.name as course_name, b.name as batch_name
        FROM attendance a
        LEFT JOIN courses c ON a.course_id = c.id
        LEFT JOIN batches b ON a.batch_id  = b.id
        WHERE a.date = ?
        ORDER BY a.time DESC
    ''', (today,))
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return records

def get_attendance_by_date_range(start_date, end_date):
    """Get attendance between two dates."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.*, c.name as course_name, b.name as batch_name
        FROM attendance a
        LEFT JOIN courses c ON a.course_id = c.id
        LEFT JOIN batches b ON a.batch_id  = b.id
        WHERE a.date BETWEEN ? AND ?
        ORDER BY a.date DESC, a.time DESC
    ''', (start_date, end_date))
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return records

def get_student_attendance_percentage(student_id):
    """Get attendance percentage for a student."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(DISTINCT date) as present_days
        FROM attendance WHERE student_id=?
    ''', (student_id,))
    present = cursor.fetchone()['present_days']

    cursor.execute('''
        SELECT COUNT(DISTINCT date) as total_days
        FROM attendance
    ''')
    total = cursor.fetchone()['total_days']
    conn.close()

    if total == 0:
        return 0
    return round((present / total) * 100, 1)

# ─────────────────────────────────────────
# TIMETABLE FUNCTIONS
# ─────────────────────────────────────────
def get_current_session(course_id, batch_id):
    """Get current running session from timetable."""
    now         = datetime.now()
    day         = now.strftime('%A')
    current_time = now.strftime('%H:%M')

    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.*, u.full_name as lecturer_name
        FROM timetable t
        LEFT JOIN users u ON t.lecturer_id = u.id
        WHERE t.course_id=? AND t.batch_id=?
        AND t.day_of_week=?
        AND t.start_time <= ? AND t.end_time >= ?
    ''', (course_id, batch_id, day, current_time, current_time))
    session = cursor.fetchone()
    conn.close()
    return dict(session) if session else None

def add_timetable(course_id, batch_id, subject,
                  day, start_time, end_time, lecturer_id):
    """Add timetable entry."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO timetable
        (course_id, batch_id, subject, day_of_week,
         start_time, end_time, lecturer_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (course_id, batch_id, subject, day,
          start_time, end_time, lecturer_id))
    conn.commit()
    conn.close()
    return True

def get_timetable(course_id=None, batch_id=None):
    """Get timetable entries."""
    conn   = get_connection()
    cursor = conn.cursor()
    if course_id and batch_id:
        cursor.execute('''
            SELECT t.*, u.full_name as lecturer_name,
                   c.name as course_name, b.name as batch_name
            FROM timetable t
            LEFT JOIN users u    ON t.lecturer_id = u.id
            LEFT JOIN courses c  ON t.course_id   = c.id
            LEFT JOIN batches b  ON t.batch_id    = b.id
            WHERE t.course_id=? AND t.batch_id=?
            ORDER BY t.day_of_week, t.start_time
        ''', (course_id, batch_id))
    else:
        cursor.execute('''
            SELECT t.*, u.full_name as lecturer_name,
                   c.name as course_name, b.name as batch_name
            FROM timetable t
            LEFT JOIN users u    ON t.lecturer_id = u.id
            LEFT JOIN courses c  ON t.course_id   = c.id
            LEFT JOIN batches b  ON t.batch_id    = b.id
            ORDER BY t.day_of_week, t.start_time
        ''')
    entries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return entries

# ─────────────────────────────────────────
# RUN INITIALIZATION
# ─────────────────────────────────────────
if __name__ == '__main__':
    initialize_database()
    print("\n📊 Database Tables Created:")
    print("  ✅ users")
    print("  ✅ departments")
    print("  ✅ courses")
    print("  ✅ batches")
    print("  ✅ students")
    print("  ✅ timetable")
    print("  ✅ attendance")
    print("\n🔑 Default Admin:")
    print("  Username : admin")
    print("  Password : admin123")