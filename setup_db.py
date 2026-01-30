import sqlite3
import hashlib
def create_schema():
    conn = sqlite3.connect('football.db')
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
        role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS seasons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        city TEXT,
        stadium TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id INTEGER,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        position TEXT,
        FOREIGN KEY(team_id) REFERENCES teams(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        season_id INTEGER,
        home_team_id INTEGER,
        away_team_id INTEGER,
        round INTEGER,
        match_date TEXT,
        home_score INTEGER,
        away_score INTEGER,
        FOREIGN KEY(season_id) REFERENCES seasons(id),
        FOREIGN KEY(home_team_id) REFERENCES teams(id),
        FOREIGN KEY(away_team_id) REFERENCES teams(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS match_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        player_id INTEGER,
        event_type TEXT,
        minute INTEGER,
        FOREIGN KEY(match_id) REFERENCES matches(id),
        FOREIGN KEY(player_id) REFERENCES players(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        old_score TEXT,
        new_score TEXT,
        change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''
    CREATE TRIGGER IF NOT EXISTS log_score_change
    AFTER UPDATE OF home_score, away_score ON matches
    BEGIN
        INSERT INTO audit_logs (match_id, old_score, new_score)
        VALUES (
            OLD.id,
            OLD.home_score || ':' || OLD.away_score,
            NEW.home_score || ':' || NEW.away_score
        );
    END;
    ''')
    admin_pass=hashlib.sha256('adminpass'.encode()).hexdigest()
    try:
        c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                  ('admin', admin_pass, 'admin'))
    except sqlite3.IntegrityError:
        print("Admin juz istnieje")
    conn.commit()
    conn.close()
    print("Baza danych i tabele zostały utworzone pomyślnie.")
if __name__ == '__main__':
    create_schema()