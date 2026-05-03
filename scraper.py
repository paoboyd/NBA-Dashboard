# scraper.py - pulls NBA data from ESPN's API using requests

import time
import psycopg2
import psycopg2.extras
import os
import requests

DATABASE_URL = os.environ.get('DATABASE_URL')

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept': 'application/json',
}

# ESPN endpoints
ESPN_TEAMS_URL = 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams'
ESPN_ROSTER_URL = 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{espn_id}/roster'
ESPN_ATHLETE_URL = 'https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba/athletes/{athlete_id}?season=2025'

# all 30 teams w/ colors for the dashboard
NBA_TEAMS = [
    {"name": "Hawks",         "city": "Atlanta",       "abbr": "ATL", "conf": "Eastern", "div": "Southeast", "arena": "State Farm Arena",              "year": 1946, "color": "#E03A3E", "accent": "#C1D32F"},
    {"name": "Celtics",       "city": "Boston",        "abbr": "BOS", "conf": "Eastern", "div": "Atlantic",  "arena": "TD Garden",                     "year": 1946, "color": "#007A33", "accent": "#BA9653"},
    {"name": "Nets",          "city": "Brooklyn",      "abbr": "BKN", "conf": "Eastern", "div": "Atlantic",  "arena": "Barclays Center",               "year": 1967, "color": "#000000", "accent": "#FFFFFF"},
    {"name": "Hornets",       "city": "Charlotte",     "abbr": "CHA", "conf": "Eastern", "div": "Southeast", "arena": "Spectrum Center",               "year": 1988, "color": "#1D1160", "accent": "#00788C"},
    {"name": "Bulls",         "city": "Chicago",       "abbr": "CHI", "conf": "Eastern", "div": "Central",   "arena": "United Center",                 "year": 1966, "color": "#CE1141", "accent": "#000000"},
    {"name": "Cavaliers",     "city": "Cleveland",     "abbr": "CLE", "conf": "Eastern", "div": "Central",   "arena": "Rocket Mortgage FieldHouse",    "year": 1970, "color": "#860038", "accent": "#FDBB30"},
    {"name": "Mavericks",     "city": "Dallas",        "abbr": "DAL", "conf": "Western", "div": "Southwest", "arena": "American Airlines Center",      "year": 1980, "color": "#00538C", "accent": "#002B5E"},
    {"name": "Nuggets",       "city": "Denver",        "abbr": "DEN", "conf": "Western", "div": "Northwest", "arena": "Ball Arena",                    "year": 1967, "color": "#0E2240", "accent": "#FEC524"},
    {"name": "Pistons",       "city": "Detroit",       "abbr": "DET", "conf": "Eastern", "div": "Central",   "arena": "Little Caesars Arena",          "year": 1941, "color": "#C8102E", "accent": "#1D42BA"},
    {"name": "Warriors",      "city": "Golden State",  "abbr": "GSW", "conf": "Western", "div": "Pacific",   "arena": "Chase Center",                  "year": 1946, "color": "#1D428A", "accent": "#FFC72C"},
    {"name": "Rockets",       "city": "Houston",       "abbr": "HOU", "conf": "Western", "div": "Southwest", "arena": "Toyota Center",                 "year": 1967, "color": "#CE1141", "accent": "#000000"},
    {"name": "Pacers",        "city": "Indiana",       "abbr": "IND", "conf": "Eastern", "div": "Central",   "arena": "Gainbridge Fieldhouse",         "year": 1967, "color": "#002D62", "accent": "#FDBB30"},
    {"name": "Clippers",      "city": "Los Angeles",   "abbr": "LAC", "conf": "Western", "div": "Pacific",   "arena": "Intuit Dome",                   "year": 1970, "color": "#C8102E", "accent": "#1D428A"},
    {"name": "Lakers",        "city": "Los Angeles",   "abbr": "LAL", "conf": "Western", "div": "Pacific",   "arena": "Crypto.com Arena",              "year": 1947, "color": "#552583", "accent": "#FDB927"},
    {"name": "Grizzlies",     "city": "Memphis",       "abbr": "MEM", "conf": "Western", "div": "Southwest", "arena": "FedExForum",                    "year": 1995, "color": "#5D76A9", "accent": "#12173F"},
    {"name": "Heat",          "city": "Miami",         "abbr": "MIA", "conf": "Eastern", "div": "Southeast", "arena": "Kaseya Center",                 "year": 1988, "color": "#98002E", "accent": "#F9A01B"},
    {"name": "Bucks",         "city": "Milwaukee",     "abbr": "MIL", "conf": "Eastern", "div": "Central",   "arena": "Fiserv Forum",                  "year": 1968, "color": "#00471B", "accent": "#EEE1C6"},
    {"name": "Timberwolves",  "city": "Minnesota",     "abbr": "MIN", "conf": "Western", "div": "Northwest", "arena": "Target Center",                 "year": 1989, "color": "#0C2340", "accent": "#236192"},
    {"name": "Pelicans",      "city": "New Orleans",   "abbr": "NOP", "conf": "Western", "div": "Southwest", "arena": "Smoothie King Center",          "year": 2002, "color": "#0C2340", "accent": "#C8102E"},
    {"name": "Knicks",        "city": "New York",      "abbr": "NYK", "conf": "Eastern", "div": "Atlantic",  "arena": "Madison Square Garden",         "year": 1946, "color": "#006BB6", "accent": "#F58426"},
    {"name": "Thunder",       "city": "Oklahoma City", "abbr": "OKC", "conf": "Western", "div": "Northwest", "arena": "Paycom Center",                 "year": 1967, "color": "#007AC1", "accent": "#EF6100"},
    {"name": "Magic",         "city": "Orlando",       "abbr": "ORL", "conf": "Eastern", "div": "Southeast", "arena": "Amway Center",                  "year": 1989, "color": "#0077C0", "accent": "#000000"},
    {"name": "76ers",         "city": "Philadelphia",  "abbr": "PHI", "conf": "Eastern", "div": "Atlantic",  "arena": "Wells Fargo Center",            "year": 1946, "color": "#006BB6", "accent": "#ED174C"},
    {"name": "Suns",          "city": "Phoenix",       "abbr": "PHX", "conf": "Western", "div": "Pacific",   "arena": "Footprint Center",              "year": 1968, "color": "#1D1160", "accent": "#E56020"},
    {"name": "Trail Blazers", "city": "Portland",      "abbr": "POR", "conf": "Western", "div": "Northwest", "arena": "Moda Center",                   "year": 1970, "color": "#E03A3E", "accent": "#000000"},
    {"name": "Kings",         "city": "Sacramento",    "abbr": "SAC", "conf": "Western", "div": "Pacific",   "arena": "Golden 1 Center",               "year": 1945, "color": "#5A2D81", "accent": "#63727A"},
    {"name": "Spurs",         "city": "San Antonio",   "abbr": "SAS", "conf": "Western", "div": "Southwest", "arena": "Frost Bank Center",             "year": 1967, "color": "#C4CED4", "accent": "#000000"},
    {"name": "Raptors",       "city": "Toronto",       "abbr": "TOR", "conf": "Eastern", "div": "Atlantic",  "arena": "Scotiabank Arena",              "year": 1995, "color": "#CE1141", "accent": "#000000"},
    {"name": "Jazz",          "city": "Utah",          "abbr": "UTA", "conf": "Western", "div": "Northwest", "arena": "Delta Center",                  "year": 1974, "color": "#002B5C", "accent": "#00471B"},
    {"name": "Wizards",       "city": "Washington",    "abbr": "WAS", "conf": "Eastern", "div": "Southeast", "arena": "Capital One Arena",             "year": 1961, "color": "#002B5C", "accent": "#E31837"},
]

# some ESPN abbreviations differ from the standard ones
ESPN_ABBR_MAP = {
    'GSW': 'GS', 'NOP': 'NO', 'NYK': 'NY',
    'SAS': 'SA', 'UTA': 'UTAH', 'WAS': 'WSH',
}


def _get(url, timeout=15):
    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def _parse_height(display_height):
    # convert 6' 8" to 6-8
    if not display_height:
        return ''
    return display_height.replace("'", "-").replace('"', '').strip()


def _get_espn_team_ids():
    data = _get(ESPN_TEAMS_URL)
    teams = data['sports'][0]['leagues'][0]['teams']
    espn_map = {}
    for entry in teams:
        t = entry['team']
        espn_map[t['abbreviation']] = t['id']
    return espn_map


def _get_roster(espn_team_id):
    url = ESPN_ROSTER_URL.format(espn_id=espn_team_id)
    data = _get(url)
    return data.get('athletes', [])


def _get_athlete_stats(athlete_id):
    # grab per-game stats from ESPN
    url = ESPN_ATHLETE_URL.format(athlete_id=athlete_id)
    try:
        data = _get(url)
        athlete = data.get('athlete', {})
        summary = athlete.get('statsSummary', {})
        stats_list = summary.get('statistics', [])
        result = {'ppg': 0.0, 'rpg': 0.0, 'apg': 0.0, 'fg_pct': 0.0}
        for s in stats_list:
            name = s.get('name', '')
            val = s.get('value', 0.0) or 0.0
            if name == 'avgPoints':
                result['ppg'] = round(float(val), 1)
            elif name == 'avgRebounds':
                result['rpg'] = round(float(val), 1)
            elif name == 'avgAssists':
                result['apg'] = round(float(val), 1)
            elif name == 'fieldGoalPct':
                result['fg_pct'] = round(float(val) / 100, 3)
        return result
    except Exception:
        return {'ppg': 0.0, 'rpg': 0.0, 'apg': 0.0, 'fg_pct': 0.0}


def scrape_with_nba_api():
    # main scraping function - hits ESPN for all 30 teams
    print('Scraping NBA data from ESPN...')

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # insert teams
    for t in NBA_TEAMS:
        cur.execute("""
            INSERT INTO teams
                (name, city, abbreviation, conference, division,
                 arena, founded_year, primary_color, accent_color)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (name) DO NOTHING
        """, (t['name'], t['city'], t['abbr'], t['conf'], t['div'],
              t['arena'], t['year'], t['color'], t['accent']))

    # clear old player data before re-scraping
    cur.execute('DELETE FROM player_stats')
    cur.execute('DELETE FROM players')
    conn.commit()

    # map our abbreviations to db team_ids
    cur.execute('SELECT team_id, abbreviation FROM teams')
    db_team_map = {row[1]: row[0] for row in cur.fetchall()}

    # get ESPN's internal team IDs
    try:
        espn_id_map = _get_espn_team_ids()
    except Exception as e:
        print(f'Could not reach ESPN: {e}')
        cur.close()
        conn.close()
        return False
    print(f'Got {len(espn_id_map)} teams from ESPN')

    total_players = 0
    total_stats = 0

    # loop through each team and grab their roster + stats
    for our_team in NBA_TEAMS:
        our_abbr = our_team['abbr']
        espn_abbr = ESPN_ABBR_MAP.get(our_abbr, our_abbr)
        espn_team_id = espn_id_map.get(espn_abbr)
        db_team_id = db_team_map.get(our_abbr)

        if not espn_team_id or not db_team_id:
            continue

        try:
            athletes = _get_roster(espn_team_id)
            time.sleep(0.2)  # don't spam ESPN
        except Exception as e:
            print(f'{our_abbr}: roster failed - {e}')
            continue

        count = 0
        for athlete in athletes:
            first = athlete.get('firstName', '')
            last = athlete.get('lastName', '')
            if not first and not last:
                continue

            # parse bio info
            height_in = athlete.get('height', 0)
            display_height = athlete.get('displayHeight', '')
            height_str = _parse_height(display_height) if display_height else (
                f"{int(height_in // 12)}-{int(height_in % 12)}" if height_in else ''
            )
            weight = int(athlete.get('weight', 0) or 0)
            jersey_raw = athlete.get('jersey', '0')
            try:
                jersey = int(jersey_raw) if jersey_raw else 0
            except ValueError:
                jersey = 0

            position_obj = athlete.get('position', {})
            position = position_obj.get('abbreviation', '') if isinstance(position_obj, dict) else ''

            birth_place = athlete.get('birthPlace', {})
            country = birth_place.get('country', 'USA') if isinstance(birth_place, dict) else 'USA'
            if not country:
                country = 'USA'

            # get salary from contract data
            contracts_data = athlete.get('contracts', [])
            salary = 0
            if contracts_data:
                latest = max(contracts_data, key=lambda c: c.get('season', {}).get('year', 0))
                salary = int(latest.get('salary', 0) or 0)

            athlete_id = athlete.get('id', '')

            # insert player
            cur.execute("""
                INSERT INTO players
                    (first_name, last_name, height, weight, jersey_number,
                     team_id, position, salary, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING player_id
            """, (first, last, height_str, weight, jersey,
                  db_team_id, position, salary, country))

            row = cur.fetchone()
            player_db_id = row[0] if row else None

            if not player_db_id:
                cur.execute(
                    'SELECT player_id FROM players WHERE first_name=%s AND last_name=%s AND team_id=%s',
                    (first, last, db_team_id)
                )
                row = cur.fetchone()
                player_db_id = row[0] if row else None

            # grab their stats
            if athlete_id and player_db_id:
                stats = _get_athlete_stats(athlete_id)
                time.sleep(0.1)

                cur.execute("""
                    INSERT INTO player_stats
                        (player_id, season_year, games_played,
                         ppg, rpg, apg, spg, bpg, fg_pct, three_pct, ft_pct)
                    VALUES (%s, '2025-26', 0, %s, %s, %s, 0, 0, %s, 0, 0)
                    ON CONFLICT (player_id, season_year) DO NOTHING
                """, (player_db_id,
                      stats['ppg'], stats['rpg'], stats['apg'], stats['fg_pct']))
                if cur.rowcount > 0:
                    total_stats += 1

            count += 1

        conn.commit()
        total_players += count
        print(f'{our_abbr}: {count} players')

    conn.commit()
    cur.close()
    conn.close()

    print(f'Done! {total_players} players, {total_stats} stat records')
    return True


def scrape_historical_stats():
    # ESPN doesn't expose multi-season history easily
    pass


def seed_fallback_data():
    from seed_data import seed_all
    seed_all()


if __name__ == '__main__':
    from database import init_db
    init_db()

    success = scrape_with_nba_api()
    if not success:
        print('ESPN unavailable, using seed data...')
        seed_fallback_data()

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM teams')
    teams = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM players')
    players = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM player_stats')
    stats = cur.fetchone()[0]
    print(f'Final: {teams} teams, {players} players, {stats} stats')
    cur.close()
    conn.close()
