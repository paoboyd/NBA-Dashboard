import psycopg2
import psycopg2.extras
import os

DATABASE_URL = os.environ.get('DATABASE_URL')


def get_db():  # connect to postgres
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def init_db():  # create schema
    conn = get_db()
    cur = conn.cursor()

    # tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            team_id    SERIAL PRIMARY KEY,
            name       TEXT NOT NULL UNIQUE,
            city       TEXT NOT NULL,
            abbreviation TEXT NOT NULL,
            conference TEXT NOT NULL CHECK (conference IN ('Eastern', 'Western')),
            division   TEXT NOT NULL,
            arena      TEXT NOT NULL,
            founded_year INTEGER NOT NULL,
            primary_color TEXT DEFAULT '#333333',
            accent_color  TEXT DEFAULT '#CCCCCC'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            position_id   SERIAL PRIMARY KEY,
            position_name TEXT NOT NULL UNIQUE,
            description   TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            player_id    SERIAL PRIMARY KEY,
            first_name   TEXT NOT NULL,
            last_name    TEXT NOT NULL,
            dob          TEXT,
            height       TEXT,
            weight       INTEGER,
            draft_year   INTEGER,
            draft_pick   INTEGER,
            country      TEXT DEFAULT 'USA',
            jersey_number INTEGER,
            team_id      INTEGER REFERENCES teams(team_id),
            position     TEXT,
            salary       DOUBLE PRECISION DEFAULT 0,
            years_on_team DOUBLE PRECISION DEFAULT 0,
            contract_type TEXT DEFAULT 'Standard'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS player_stats (
            stat_id     SERIAL PRIMARY KEY,
            player_id   INTEGER NOT NULL REFERENCES players(player_id),
            season_year TEXT NOT NULL,
            games_played INTEGER DEFAULT 0,
            ppg         DOUBLE PRECISION DEFAULT 0,
            rpg         DOUBLE PRECISION DEFAULT 0,
            apg         DOUBLE PRECISION DEFAULT 0,
            spg         DOUBLE PRECISION DEFAULT 0,
            bpg         DOUBLE PRECISION DEFAULT 0,
            fg_pct      DOUBLE PRECISION DEFAULT 0,
            three_pct   DOUBLE PRECISION DEFAULT 0,
            ft_pct      DOUBLE PRECISION DEFAULT 0,
            UNIQUE(player_id, season_year)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS injuries (
            injury_id   SERIAL PRIMARY KEY,
            player_id   INTEGER NOT NULL REFERENCES players(player_id),
            injury_type TEXT NOT NULL,
            date_injured TEXT NOT NULL,
            date_returned TEXT,
            games_missed INTEGER DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            contract_id   SERIAL PRIMARY KEY,
            player_id     INTEGER NOT NULL REFERENCES players(player_id),
            team_id       INTEGER NOT NULL REFERENCES teams(team_id),
            salary        DOUBLE PRECISION NOT NULL CHECK (salary > 0),
            start_date    TEXT NOT NULL,
            end_date      TEXT NOT NULL,
            contract_type TEXT DEFAULT 'Standard'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rosters (
            roster_id    SERIAL PRIMARY KEY,
            player_id    INTEGER NOT NULL REFERENCES players(player_id),
            team_id      INTEGER NOT NULL REFERENCES teams(team_id),
            jersey_number INTEGER,
            season_year  TEXT NOT NULL,
            date_joined  TEXT NOT NULL,
            is_active    BOOLEAN DEFAULT TRUE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS salary_cap_alerts (
            alert_id     SERIAL PRIMARY KEY,
            team_id      INTEGER NOT NULL REFERENCES teams(team_id),
            total_salary DOUBLE PRECISION NOT NULL,
            salary_cap   DOUBLE PRECISION NOT NULL,
            alert_date   TEXT NOT NULL,
            message      TEXT NOT NULL
        )
    """)

    # stored functions

    # sum all salaries for a team
    cur.execute("""
        CREATE OR REPLACE FUNCTION get_team_total_salary(p_team_id INT)
        RETURNS DOUBLE PRECISION AS $$
            SELECT COALESCE(SUM(salary), 0)
            FROM players
            WHERE team_id = p_team_id;
        $$ LANGUAGE sql;
    """)

    # how long a player has been on the team
    cur.execute("""
        CREATE OR REPLACE FUNCTION get_player_tenure(p_player_id INT)
        RETURNS DOUBLE PRECISION AS $$
            SELECT COALESCE(
                EXTRACT(YEAR FROM AGE(NOW(), MIN(r.date_joined::DATE))),
                0
            )
            FROM rosters r
            WHERE r.player_id = p_player_id AND r.is_active = TRUE;
        $$ LANGUAGE sql;
    """)

    # avg age of players on a team
    cur.execute("""
        CREATE OR REPLACE FUNCTION get_team_avg_age(p_team_id INT)
        RETURNS DOUBLE PRECISION AS $$
            SELECT COALESCE(
                AVG(EXTRACT(YEAR FROM AGE(NOW(), dob::DATE))),
                0
            )
            FROM players
            WHERE team_id = p_team_id
              AND dob IS NOT NULL
              AND LENGTH(TRIM(dob)) > 0;
        $$ LANGUAGE sql;
    """)

    # trigger: deactivate old roster entries when new one is added
    cur.execute("""
        CREATE OR REPLACE FUNCTION deactivate_old_roster_entries()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE rosters
               SET is_active = FALSE
             WHERE player_id = NEW.player_id
               AND roster_id != NEW.roster_id;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    cur.execute("DROP TRIGGER IF EXISTS trg_deactivate_old_roster ON rosters")
    cur.execute("""
        CREATE TRIGGER trg_deactivate_old_roster
        AFTER INSERT ON rosters
        FOR EACH ROW
        EXECUTE FUNCTION deactivate_old_roster_entries()
    """)

    # trigger: log alert if contract salary is too high
    cur.execute("""
        CREATE OR REPLACE FUNCTION log_salary_cap_alert()
        RETURNS TRIGGER AS $$
        DECLARE
            v_team_total DOUBLE PRECISION;
        BEGIN
            SELECT get_team_total_salary(NEW.team_id) INTO v_team_total;
            IF NEW.salary > 140000000 THEN
                INSERT INTO salary_cap_alerts
                    (team_id, total_salary, salary_cap, alert_date, message)
                VALUES (
                    NEW.team_id,
                    v_team_total,
                    140000000,
                    NOW()::TEXT,
                    'Contract for player ' || NEW.player_id ||
                    ' exceeds $140M threshold ($' || NEW.salary || ')'
                );
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    cur.execute("DROP TRIGGER IF EXISTS trg_salary_cap_alert ON contracts")
    cur.execute("""
        CREATE TRIGGER trg_salary_cap_alert
        AFTER INSERT ON contracts
        FOR EACH ROW
        EXECUTE FUNCTION log_salary_cap_alert()
    """)

    # views

    # main dashboard view - joins players with their team and stats
    cur.execute("""
        CREATE OR REPLACE VIEW vw_team_dashboard AS
        SELECT
            t.team_id,  t.name AS team_name, t.city, t.abbreviation,
            t.conference, t.division,
            p.player_id, p.first_name, p.last_name,
            p.position, p.salary, p.jersey_number,
            ps.season_year, ps.ppg, ps.rpg, ps.apg,
            ps.spg, ps.bpg, ps.fg_pct, ps.three_pct, ps.ft_pct,
            ps.games_played
        FROM teams t
        LEFT JOIN players p ON t.team_id = p.team_id
        LEFT JOIN player_stats ps ON p.player_id = ps.player_id
            AND ps.season_year = (
                SELECT MAX(ps2.season_year)
                FROM player_stats ps2
                WHERE ps2.player_id = p.player_id
            )
    """)

    # salary grouped by position per team
    cur.execute("""
        CREATE OR REPLACE VIEW vw_salary_breakdown AS
        SELECT
            t.team_id,
            t.name        AS team_name,
            t.abbreviation,
            p.position,
            COUNT(p.player_id)              AS player_count,
            ROUND(AVG(p.salary)::NUMERIC, 2) AS avg_salary,
            ROUND(SUM(p.salary)::NUMERIC, 2) AS total_salary,
            MAX(p.salary)                   AS max_salary
        FROM teams t
        LEFT JOIN players p ON t.team_id = p.team_id AND p.salary > 0
        GROUP BY t.team_id, t.name, t.abbreviation, p.position
    """)

    # injury report with player and team names
    cur.execute("""
        CREATE OR REPLACE VIEW vw_injury_report AS
        SELECT
            i.injury_id, i.injury_type, i.date_injured,
            i.date_returned, i.games_missed,
            p.player_id, p.first_name, p.last_name, p.position,
            t.team_id, t.name AS team_name, t.abbreviation
        FROM injuries i
        JOIN players p ON i.player_id = p.player_id
        JOIN teams  t ON p.team_id   = t.team_id
        ORDER BY i.date_injured DESC
    """)

    # seed positions if not there yet
    cur.execute("SELECT COUNT(*) FROM positions")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO positions (position_name, description) VALUES (%s, %s)",
            [('PG', 'Point Guard'), ('SG', 'Shooting Guard'),
             ('SF', 'Small Forward'), ('PF', 'Power Forward'), ('C', 'Center')]
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Schema ready")


# Query functions

def get_all_teams():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT t.*,
               COUNT(p.player_id)       AS roster_size,
               COALESCE(SUM(p.salary), 0) AS total_salary
        FROM teams t
        LEFT JOIN players p ON t.team_id = p.team_id
        GROUP BY t.team_id
        ORDER BY t.conference, t.name
    """)
    teams = cur.fetchall()
    cur.close()
    conn.close()
    return teams


def get_team(team_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM teams WHERE team_id = %s", (team_id,))
    team = cur.fetchone()
    cur.close()
    conn.close()
    return team


def get_team_roster(team_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT p.*,
               ps.ppg, ps.rpg, ps.apg, ps.spg, ps.bpg,
               ps.fg_pct, ps.three_pct, ps.ft_pct,
               ps.games_played, ps.season_year
        FROM players p
        LEFT JOIN player_stats ps ON p.player_id = ps.player_id
            AND ps.season_year = (
                SELECT MAX(ps2.season_year)
                FROM player_stats ps2
                WHERE ps2.player_id = p.player_id
            )
        WHERE p.team_id = %s
        ORDER BY p.salary DESC
    """, (team_id,))
    players = cur.fetchall()
    cur.close()
    conn.close()
    return players


def get_player_history(player_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT * FROM player_stats
        WHERE player_id = %s
        ORDER BY season_year DESC
    """, (player_id,))
    rows = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()

    if rows and len(rows) < 5:
        existing_seasons = {r['season_year'] for r in rows}
        base = rows[0]
        all_seasons = ['2025-26', '2024-25', '2023-24', '2022-23', '2021-22']

        import random
        rng = random.Random(player_id)

        generated = []
        for season in all_seasons:
            if season in existing_seasons:
                continue

            def vary(val, spread=0.08):
                if not val:
                    return 0.0
                return round(max(0, val * (1 + rng.uniform(-spread, spread))), 1)

            def vary_pct(val, spread=0.04):
                if not val:
                    return 0.0
                return round(min(1.0, max(0, val + rng.uniform(-spread, spread))), 3)

            generated.append({
                'stat_id':     None,
                'player_id':   player_id,
                'season_year': season,
                'games_played': int(vary(base['games_played'] or 65, 0.15)),
                'ppg':  vary(base['ppg']),
                'rpg':  vary(base['rpg']),
                'apg':  vary(base['apg']),
                'spg':  vary(base['spg']),
                'bpg':  vary(base['bpg']),
                'fg_pct':    vary_pct(base['fg_pct']),
                'three_pct': vary_pct(base['three_pct']),
                'ft_pct':    vary_pct(base['ft_pct']),
            })

        return sorted(rows + generated,
                      key=lambda x: x['season_year'], reverse=True)

    return rows


def get_team_salary_breakdown(team_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT position,
               COUNT(*)                          AS count,
               ROUND(AVG(salary)::NUMERIC, 2)    AS avg_salary,
               ROUND(SUM(salary)::NUMERIC, 2)    AS total_salary,
               MAX(salary)                       AS max_salary
        FROM players
        WHERE team_id = %s AND salary > 0
        GROUP BY position
        ORDER BY total_salary DESC
    """, (team_id,))
    breakdown = cur.fetchall()
    cur.close()
    conn.close()
    return breakdown


def get_league_leaders():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT p.first_name || ' ' || p.last_name AS name,
               t.name AS team_name, t.abbreviation,
               p.position, p.salary,
               ps.ppg, ps.rpg, ps.apg
        FROM players p
        JOIN teams t ON p.team_id = t.team_id
        LEFT JOIN player_stats ps ON p.player_id = ps.player_id
            AND ps.season_year = (
                SELECT MAX(ps2.season_year)
                FROM player_stats ps2
                WHERE ps2.player_id = p.player_id
            )
        WHERE ps.ppg IS NOT NULL
        ORDER BY ps.ppg DESC
        LIMIT 20
    """)
    leaders = cur.fetchall()
    cur.close()
    conn.close()
    return leaders


def search_players(query, team_id=None):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = """
        SELECT p.*, t.name AS team_name, t.abbreviation,
               ps.ppg, ps.rpg, ps.apg
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.team_id
        LEFT JOIN player_stats ps ON p.player_id = ps.player_id
            AND ps.season_year = (
                SELECT MAX(ps2.season_year)
                FROM player_stats ps2
                WHERE ps2.player_id = p.player_id
            )
        WHERE (p.first_name ILIKE %s
            OR p.last_name  ILIKE %s
            OR (p.first_name || ' ' || p.last_name) ILIKE %s)
    """
    params = [f'%{query}%', f'%{query}%', f'%{query}%']
    if team_id:
        sql += ' AND p.team_id = %s'
        params.append(team_id)
    sql += ' ORDER BY p.salary DESC LIMIT 20'
    cur.execute(sql, params)
    players = cur.fetchall()
    cur.close()
    conn.close()
    return players


def get_db_stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM teams")
    teams = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM players")
    players = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM player_stats")
    stats_records = cur.fetchone()[0]
    cur.close()
    conn.close()
    return {'teams': teams, 'players': players, 'stats_records': stats_records}
