# main.py - Flask app for NBA dashboard

import threading
import os
from flask import Flask, render_template, jsonify, request
from database import init_db, get_all_teams, get_team, get_team_roster, \
    get_player_history, get_team_salary_breakdown, get_league_leaders, \
    search_players, get_db_stats

app = Flask(__name__)


@app.route('/')
def index():
    teams = get_all_teams()
    stats = get_db_stats()
    return render_template('index.html', teams=teams, db_stats=stats)


@app.route('/api/teams')
def api_teams():
    teams = get_all_teams()
    return jsonify([dict(t) for t in teams])


@app.route('/api/team/<int:team_id>')
def api_team(team_id):
    team = get_team(team_id)
    roster = get_team_roster(team_id)
    salary = get_team_salary_breakdown(team_id)
    return jsonify({
        'team': dict(team) if team else None,
        'roster': [dict(p) for p in roster],
        'salary_breakdown': [dict(s) for s in salary],
    })


@app.route('/api/player/<int:player_id>/history')
def api_player_history(player_id):
    history = get_player_history(player_id)
    return jsonify([dict(h) for h in history])


@app.route('/api/leaders')
def api_leaders():
    leaders = get_league_leaders()
    return jsonify([dict(l) for l in leaders])


@app.route('/api/search')
def api_search():
    q = request.args.get('q', '')
    if len(q) < 2:
        return jsonify([])
    team_id = request.args.get('team_id', type=int)
    results = search_players(q, team_id=team_id)
    return jsonify([dict(r) for r in results])


def _run_espn_scraper():
    # try to scrape live data, fall back to seed if it fails
    try:
        from scraper import scrape_with_nba_api
        print("Starting ESPN scraper...")
        scrape_with_nba_api()
        stats = get_db_stats()
        print(f"Scrape done: {stats['players']} players")
    except Exception as e:
        print(f"Scraper failed: {e}, using seed data")
        try:
            from seed_data import seed_all
            seed_all()
        except Exception as e2:
            print(f"Seed failed too: {e2}")


def setup():
    init_db()
    stats = get_db_stats()

    if stats['players'] == 0:
        # db is empty, load seed data first then try scraping
        print("No players found, seeding...")
        from seed_data import seed_all
        seed_all()
        stats = get_db_stats()
        print(f"Seeded {stats['players']} players")

        # kick off espn scrape in background
        t = threading.Thread(target=_run_espn_scraper, daemon=True)
        t.start()
    elif stats['players'] < 300:
        # only seed data, try to get real espn data
        print(f"Only {stats['players']} players, launching scraper...")
        t = threading.Thread(target=_run_espn_scraper, daemon=True)
        t.start()
    else:
        print(f"Already have {stats['players']} players, skipping scrape")

    stats = get_db_stats()
    print(f"DB: {stats['teams']} teams, {stats['players']} players, {stats['stats_records']} stats")


if __name__ == '__main__':
    setup()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
