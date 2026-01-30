import sqlite3
import hashlib
DB_NAME = 'football.db'
def get_db_connection():
    return sqlite3.connect(DB_NAME)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
def verify_password(stored_hash, password):
    return stored_hash == hash_password(password)
def login(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, role, password_hash FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    if row and verify_password(row[2], password):
        return (row[0], row[1])
    return None
def get_matches_by_season(season_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT m.id, t1.name AS home_team, t2.name AS away_team, m.round, m.match_date, m.home_score, m.away_score
                 FROM matches m
                 JOIN teams t1 ON m.home_team_id = t1.id
                 JOIN teams t2 ON m.away_team_id = t2.id
                 WHERE m.season_id = ?''', (season_id,))
    matches = c.fetchall()
    conn.close()
    return matches
def get_team_players(team_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT first_name, last_name, position
                 FROM players
                 WHERE team_id = ?''', (team_id,))
    players = c.fetchall()
    conn.close()
    return players
def get_match_events(match_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT p.first_name, p.last_name, me.event_type, me.minute
                 FROM match_events me
                 JOIN players p ON me.player_id = p.id
                 WHERE me.match_id = ?''', (match_id,))
    events = c.fetchall()
    conn.close()
    return events
def log_score_change(match_id, old_score, new_score):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO audit_logs (match_id, old_score, new_score)
                 VALUES (?, ?, ?)''', (match_id, old_score, new_score))
    conn.commit()
    conn.close()
def add_match_results(match_id, h_score, a_score, scorers_list):
    conn = get_db_connection()
    try:
        c= conn.cursor()
        c.execute('''UPDATE matches
                     SET home_score = ?, away_score = ?
                     WHERE id = ?''', (h_score, a_score, match_id))
        for player_id, minute in scorers_list:
            c.execute('''INSERT INTO match_events (match_id, player_id, event_type, minute)
                         VALUES (?, ?, 'goal', ?)''', (match_id, player_id, minute))
        conn.commit()
        print("Wynik i strzelcy dodani pomyslnie")
    except Exception as e:
        conn.rollback()
        print("Blad podczas dodawania wyniku i strzelcow:", e)
    finally:
        conn.close()
        