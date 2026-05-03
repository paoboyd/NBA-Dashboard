# seed_data.py - fallback data for when ESPN API is unavailable
import os

DATABASE_URL = os.environ.get('DATABASE_URL')

TEAMS = [
    ("Hawks","Atlanta","ATL","Eastern","Southeast","State Farm Arena",1946,"#E03A3E","#C1D32F"),
    ("Celtics","Boston","BOS","Eastern","Atlantic","TD Garden",1946,"#007A33","#BA9653"),
    ("Nets","Brooklyn","BKN","Eastern","Atlantic","Barclays Center",1967,"#000000","#FFFFFF"),
    ("Hornets","Charlotte","CHA","Eastern","Southeast","Spectrum Center",1988,"#1D1160","#00788C"),
    ("Bulls","Chicago","CHI","Eastern","Central","United Center",1966,"#CE1141","#000000"),
    ("Cavaliers","Cleveland","CLE","Eastern","Central","Rocket Mortgage FieldHouse",1970,"#860038","#FDBB30"),
    ("Mavericks","Dallas","DAL","Western","Southwest","American Airlines Center",1980,"#00538C","#002B5E"),
    ("Nuggets","Denver","DEN","Western","Northwest","Ball Arena",1967,"#0E2240","#FEC524"),
    ("Pistons","Detroit","DET","Eastern","Central","Little Caesars Arena",1941,"#C8102E","#1D42BA"),
    ("Warriors","Golden State","GSW","Western","Pacific","Chase Center",1946,"#1D428A","#FFC72C"),
    ("Rockets","Houston","HOU","Western","Southwest","Toyota Center",1967,"#CE1141","#000000"),
    ("Pacers","Indiana","IND","Eastern","Central","Gainbridge Fieldhouse",1967,"#002D62","#FDBB30"),
    ("Clippers","Los Angeles","LAC","Western","Pacific","Intuit Dome",1970,"#C8102E","#1D428A"),
    ("Lakers","Los Angeles","LAL","Western","Pacific","Crypto.com Arena",1947,"#552583","#FDB927"),
    ("Grizzlies","Memphis","MEM","Western","Southwest","FedExForum",1995,"#5D76A9","#12173F"),
    ("Heat","Miami","MIA","Eastern","Southeast","Kaseya Center",1988,"#98002E","#F9A01B"),
    ("Bucks","Milwaukee","MIL","Eastern","Central","Fiserv Forum",1968,"#00471B","#EEE1C6"),
    ("Timberwolves","Minnesota","MIN","Western","Northwest","Target Center",1989,"#0C2340","#236192"),
    ("Pelicans","New Orleans","NOP","Western","Southwest","Smoothie King Center",2002,"#0C2340","#C8102E"),
    ("Knicks","New York","NYK","Eastern","Atlantic","Madison Square Garden",1946,"#006BB6","#F58426"),
    ("Thunder","Oklahoma City","OKC","Western","Northwest","Paycom Center",1967,"#007AC1","#EF6100"),
    ("Magic","Orlando","ORL","Eastern","Southeast","Amway Center",1989,"#0077C0","#000000"),
    ("76ers","Philadelphia","PHI","Eastern","Atlantic","Wells Fargo Center",1946,"#006BB6","#ED174C"),
    ("Suns","Phoenix","PHX","Western","Pacific","Footprint Center",1968,"#1D1160","#E56020"),
    ("Trail Blazers","Portland","POR","Western","Northwest","Moda Center",1970,"#E03A3E","#000000"),
    ("Kings","Sacramento","SAC","Western","Pacific","Golden 1 Center",1945,"#5A2D81","#63727A"),
    ("Spurs","San Antonio","SAS","Western","Southwest","Frost Bank Center",1967,"#C4CED4","#000000"),
    ("Raptors","Toronto","TOR","Eastern","Atlantic","Scotiabank Arena",1995,"#CE1141","#000000"),
    ("Jazz","Utah","UTA","Western","Northwest","Delta Center",1974,"#002B5C","#00471B"),
    ("Wizards","Washington","WAS","Eastern","Southeast","Capital One Arena",1961,"#002B5C","#E31837"),
]

# (first, last, team_abbr, jersey, pos, salary, ppg, rpg, apg, fg, years)
PLAYERS = [
    ("Trae","Young","ATL",11,"PG",40064220,25.3,3.1,10.8,.440,5.0),
    ("Dejounte","Murray","ATL",5,"SG",25000000,20.5,5.3,6.1,.461,1.5),
    ("Jalen","Johnson","ATL",1,"SF",4370040,16.0,8.7,3.6,.498,3.0),
    ("Clint","Capela","ATL",15,"C",22500000,9.6,10.2,1.0,.610,4.0),
    ("Bogdan","Bogdanovic","ATL",13,"SG",17000000,12.5,3.4,3.0,.415,4.0),
    ("Jayson","Tatum","BOS",0,"SF",54082550,26.9,8.1,4.6,.471,9.0),
    ("Jaylen","Brown","BOS",7,"SG",49350000,23.0,5.5,3.6,.494,10.0),
    ("Derrick","White","BOS",9,"PG",18357143,12.8,3.6,5.2,.461,4.0),
    ("Kristaps","Porzingis","BOS",8,"C",30000000,20.1,7.2,2.0,.516,2.0),
    ("Jrue","Holiday","BOS",4,"PG",36861707,12.5,5.4,4.5,.461,2.0),
    ("Mikal","Bridges","BKN",1,"SF",24000000,19.6,4.5,3.6,.442,2.0),
    ("Cameron","Johnson","BKN",2,"PF",22500000,14.4,4.3,2.4,.438,2.0),
    ("Nic","Claxton","BKN",33,"C",22000000,11.8,9.2,2.5,.634,5.0),
    ("Dennis","Schroder","BKN",17,"PG",13000000,12.1,2.8,5.8,.424,1.0),
    ("Ben","Simmons","BKN",10,"PG",7750000,6.0,7.2,5.7,.560,3.0),
    ("LaMelo","Ball","CHA",1,"PG",35100000,23.9,5.1,8.0,.436,4.0),
    ("Brandon","Miller","CHA",24,"SF",11160720,17.3,4.3,2.4,.437,2.0),
    ("Mark","Williams","CHA",5,"C",4980600,12.0,9.1,1.3,.635,2.0),
    ("Miles","Bridges","CHA",0,"PF",25000000,21.0,7.3,3.2,.465,5.0),
    ("Terry","Rozier","CHA",3,"SG",22800000,18.0,4.0,5.1,.432,4.0),
    ("Zach","LaVine","CHI",8,"SG",43000000,22.2,4.0,4.4,.471,7.0),
    ("DeMar","DeRozan","CHI",11,"SF",28600000,24.0,4.3,5.3,.497,3.0),
    ("Nikola","Vucevic","CHI",9,"C",20000000,18.0,10.5,3.5,.506,4.0),
    ("Coby","White","CHI",0,"PG",12000000,12.7,3.0,4.1,.435,5.0),
    ("Patrick","Williams","CHI",44,"PF",9000000,8.9,3.9,1.5,.470,4.0),
    ("Donovan","Mitchell","CLE",45,"SG",36578100,26.6,4.1,5.1,.475,3.0),
    ("Darius","Garland","CLE",10,"PG",36016800,18.0,2.7,6.5,.449,5.0),
    ("Evan","Mobley","CLE",4,"PF",10336152,15.7,9.4,3.2,.513,4.0),
    ("Jarrett","Allen","CLE",31,"C",20000000,13.5,10.4,1.6,.637,4.0),
    ("Max","Strus","CLE",1,"SG",15000000,10.5,3.5,2.2,.378,2.0),
    ("Luka","Doncic","DAL",77,"PG",43031940,33.9,9.2,9.8,.487,7.0),
    ("Kyrie","Irving","DAL",2,"PG",37037037,25.6,5.0,5.2,.497,3.0),
    ("Daniel","Gafford","DAL",21,"C",12400000,11.2,6.9,0.9,.702,2.0),
    ("Dereck","Lively","DAL",2,"C",5200000,8.8,6.9,1.1,.640,2.0),
    ("Tim","Hardaway Jr.","DAL",10,"SG",17000000,14.4,3.0,1.8,.416,5.0),
    ("Nikola","Jokic","DEN",15,"C",51415938,26.4,12.4,9.0,.581,9.0),
    ("Jamal","Murray","DEN",27,"PG",34000000,21.2,4.0,6.5,.459,8.0),
    ("Michael","Porter Jr.","DEN",1,"SF",35800000,17.1,7.0,1.5,.489,5.0),
    ("Aaron","Gordon","DEN",50,"PF",22000000,13.9,6.5,3.3,.536,4.0),
    ("Kentavious","Caldwell-Pope","DEN",5,"SG",14700000,10.5,2.4,1.7,.440,2.0),
    ("Cade","Cunningham","DET",2,"PG",36004800,22.7,4.4,7.5,.441,4.0),
    ("Jaden","Ivey","DET",23,"SG",8000000,16.3,3.4,4.4,.410,3.0),
    ("Ausar","Thompson","DET",5,"SF",5800000,10.5,6.2,1.9,.480,2.0),
    ("Jalen","Duren","DET",0,"C",5200000,13.0,11.0,2.4,.600,3.0),
    ("Bojan","Bogdanovic","DET",44,"SF",19000000,15.8,3.8,2.1,.440,2.0),
    ("Stephen","Curry","GSW",30,"PG",55761217,26.4,4.5,5.1,.473,17.0),
    ("Klay","Thompson","GSW",11,"SG",20000000,17.9,3.3,2.3,.436,13.0),
    ("Draymond","Green","GSW",23,"PF",24026712,8.6,7.2,6.0,.495,14.0),
    ("Andrew","Wiggins","GSW",22,"SF",24330000,13.2,4.5,1.7,.451,4.0),
    ("Jonathan","Kuminga","GSW",0,"PF",6000000,12.9,4.8,2.2,.524,4.0),
    ("Jalen","Green","HOU",4,"SG",30764520,19.6,5.2,3.6,.428,4.0),
    ("Alperen","Sengun","HOU",28,"C",5200000,21.1,9.3,5.0,.537,3.0),
    ("Jabari","Smith Jr.","HOU",10,"PF",10236480,12.5,6.0,1.5,.425,3.0),
    ("Fred","VanVleet","HOU",5,"PG",42000000,14.2,3.8,7.2,.398,2.0),
    ("Amen","Thompson","HOU",1,"SF",6500000,9.5,6.5,2.8,.540,2.0),
    ("Tyrese","Haliburton","IND",0,"PG",45000000,20.1,3.7,10.9,.440,3.0),
    ("Pascal","Siakam","IND",43,"PF",37893408,22.0,7.0,4.0,.490,1.0),
    ("Myles","Turner","IND",33,"C",20000000,17.1,6.9,1.3,.526,9.0),
    ("Bennedict","Mathurin","IND",0,"SG",5800000,14.5,4.0,1.5,.438,3.0),
    ("Aaron","Nesmith","IND",23,"SF",10000000,10.8,3.5,1.7,.480,2.0),
    ("Kawhi","Leonard","LAC",2,"SF",49350000,23.7,6.1,3.6,.510,5.0),
    ("Paul","George","LAC",13,"SF",49350000,22.6,5.2,3.5,.453,5.0),
    ("James","Harden","LAC",1,"PG",35000000,16.6,5.1,8.5,.437,2.0),
    ("Ivica","Zubac","LAC",40,"C",12000000,11.7,9.2,1.6,.620,6.0),
    ("Norman","Powell","LAC",24,"SG",18000000,13.2,2.6,1.9,.460,3.0),
    ("LeBron","James","LAL",23,"PF",47607350,25.7,7.3,8.3,.540,8.0),
    ("Anthony","Davis","LAL",3,"C",40600080,24.7,12.6,3.5,.556,7.0),
    ("Austin","Reaves","LAL",15,"SG",12015600,15.9,5.1,5.5,.485,5.0),
    ("D'Angelo","Russell","LAL",1,"PG",17000000,12.4,3.1,6.3,.432,2.0),
    ("Rui","Hachimura","LAL",28,"PF",17000000,13.6,4.3,1.2,.510,3.0),
    ("Ja","Morant","MEM",12,"PG",33468854,26.2,5.6,8.1,.466,5.0),
    ("Desmond","Bane","MEM",22,"SG",28000000,23.7,5.0,4.4,.465,4.0),
    ("Jaren","Jackson Jr.","MEM",13,"PF",28946040,22.5,5.8,1.5,.478,6.0),
    ("Marcus","Smart","MEM",36,"PG",18833712,11.8,3.5,4.4,.396,2.0),
    ("Luke","Kennard","MEM",10,"SG",14765000,8.0,2.0,2.5,.450,2.0),
    ("Jimmy","Butler","MIA",22,"SF",48798677,20.8,5.3,5.0,.499,7.0),
    ("Bam","Adebayo","MIA",13,"C",32600060,19.3,9.4,3.2,.520,9.0),
    ("Tyler","Herro","MIA",14,"SG",30000000,20.8,5.3,4.7,.440,5.0),
    ("Terry","Rozier","MIA",2,"PG",22800000,16.4,3.9,4.5,.436,1.0),
    ("Caleb","Martin","MIA",16,"SF",8000000,10.0,4.0,2.0,.445,4.0),
    ("Giannis","Antetokounmpo","MIL",34,"PF",48787676,30.4,11.5,5.7,.611,11.0),
    ("Damian","Lillard","MIL",0,"PG",45640084,24.3,4.4,7.0,.424,2.0),
    ("Khris","Middleton","MIL",22,"SF",33000000,15.1,4.7,5.3,.462,11.0),
    ("Brook","Lopez","MIL",11,"C",23000000,12.5,5.2,1.6,.480,4.0),
    ("Bobby","Portis","MIL",9,"PF",12000000,13.8,7.4,1.4,.498,4.0),
    ("Anthony","Edwards","MIN",5,"SG",42180720,25.9,5.4,5.1,.460,5.0),
    ("Karl-Anthony","Towns","MIN",32,"C",36016800,21.8,8.2,3.0,.504,9.0),
    ("Rudy","Gobert","MIN",27,"C",38200000,13.7,12.9,1.3,.660,2.0),
    ("Mike","Conley","MIN",10,"PG",14500000,10.2,2.9,5.7,.445,2.0),
    ("Jaden","McDaniels","MIN",3,"SF",16000000,10.5,3.3,1.5,.473,4.0),
    ("Zion","Williamson","NOP",1,"PF",36016800,22.9,5.8,5.0,.576,5.0),
    ("Brandon","Ingram","NOP",14,"SF",36016800,24.7,5.1,5.7,.492,5.0),
    ("CJ","McCollum","NOP",3,"SG",33333333,18.5,4.1,5.0,.444,3.0),
    ("Herb","Jones","NOP",5,"SF",9400000,11.0,3.8,2.5,.480,4.0),
    ("Jonas","Valanciunas","NOP",17,"C",14000000,12.0,8.8,2.1,.540,3.0),
    ("Jalen","Brunson","NYK",11,"PG",36090600,28.7,3.6,6.7,.479,4.0),
    ("Julius","Randle","NYK",30,"PF",28904300,24.0,10.0,5.0,.468,7.0),
    ("RJ","Barrett","NYK",9,"SF",23000000,18.4,5.6,2.9,.435,5.0),
    ("Donte","DiVincenzo","NYK",0,"SG",15000000,15.5,3.7,2.7,.448,1.0),
    ("Mitchell","Robinson","NYK",23,"C",14000000,8.5,8.5,0.5,.660,6.0),
    ("Shai","Gilgeous-Alexander","OKC",2,"PG",40064220,31.4,5.5,6.2,.535,6.0),
    ("Jalen","Williams","OKC",8,"SF",4800000,19.1,4.5,4.5,.460,3.0),
    ("Chet","Holmgren","OKC",7,"C",10886400,16.5,7.9,2.4,.530,2.0),
    ("Josh","Giddey","OKC",3,"PG",8000000,12.3,6.4,4.8,.470,4.0),
    ("Lu","Dort","OKC",5,"SG",15000000,10.3,4.0,1.6,.405,5.0),
    ("Paolo","Banchero","ORL",5,"PF",11600820,22.6,6.9,5.4,.459,3.0),
    ("Franz","Wagner","ORL",22,"SF",30000000,19.7,5.3,3.7,.461,4.0),
    ("Jalen","Suggs","ORL",4,"PG",6700000,12.6,3.1,4.4,.432,4.0),
    ("Wendell","Carter Jr.","ORL",34,"C",13000000,12.0,7.6,2.7,.520,4.0),
    ("Markelle","Fultz","ORL",20,"PG",17000000,9.0,3.0,5.5,.455,5.0),
    ("Joel","Embiid","PHI",21,"C",51415938,33.1,10.2,5.7,.540,8.0),
    ("Tyrese","Maxey","PHI",0,"PG",35000000,25.9,3.7,6.2,.445,4.0),
    ("Tobias","Harris","PHI",12,"PF",39270150,17.2,6.5,3.1,.478,5.0),
    ("Kelly","Oubre Jr.","PHI",9,"SF",11000000,15.4,5.0,1.5,.440,1.0),
    ("De'Anthony","Melton","PHI",8,"SG",8000000,11.1,3.7,3.1,.418,2.0),
    ("Devin","Booker","PHX",1,"SG",49350000,27.1,4.5,6.9,.493,9.0),
    ("Kevin","Durant","PHX",35,"SF",51179000,27.1,6.6,5.0,.523,2.0),
    ("Bradley","Beal","PHX",3,"SG",50203930,18.2,4.4,5.0,.462,1.0),
    ("Jusuf","Nurkic","PHX",20,"C",18400000,10.3,9.2,3.0,.530,1.0),
    ("Grayson","Allen","PHX",6,"SG",14000000,13.5,3.1,3.0,.470,1.0),
    ("Anfernee","Simons","POR",1,"SG",25000000,22.6,2.8,3.6,.438,6.0),
    ("Jerami","Grant","POR",9,"PF",29000000,20.3,4.5,2.4,.441,3.0),
    ("Scoot","Henderson","POR",0,"PG",8200000,11.0,2.8,4.5,.380,2.0),
    ("Deandre","Ayton","POR",2,"C",34000000,16.7,10.2,1.7,.590,2.0),
    ("Shaedon","Sharpe","POR",17,"SG",5800000,10.0,3.0,1.5,.415,3.0),
    ("De'Aaron","Fox","SAC",5,"PG",34012500,26.6,4.6,6.1,.489,8.0),
    ("Domantas","Sabonis","SAC",10,"C",26352000,19.4,13.7,7.3,.594,3.0),
    ("Keegan","Murray","SAC",13,"SF",5800000,14.5,4.5,1.7,.443,3.0),
    ("Harrison","Barnes","SAC",40,"PF",18000000,12.2,4.0,1.5,.453,5.0),
    ("Kevin","Huerter","SAC",9,"SG",15000000,12.1,3.3,3.4,.447,3.0),
    ("Victor","Wembanyama","SAS",1,"C",12960480,21.4,10.6,3.9,.465,2.0),
    ("Devin","Vassell","SAS",24,"SG",19000000,18.5,3.8,4.2,.460,4.0),
    ("Keldon","Johnson","SAS",3,"SF",20000000,16.0,4.0,2.7,.453,5.0),
    ("Jeremy","Sochan","SAS",10,"PF",5200000,11.3,5.5,3.5,.485,3.0),
    ("Tre","Jones","SAS",33,"PG",10000000,10.0,2.8,6.0,.465,4.0),
    ("Scottie","Barnes","TOR",4,"PF",11600820,19.9,8.2,6.1,.473,4.0),
    ("Pascal","Siakam","TOR",43,"PF",37893408,21.7,6.8,5.8,.480,8.0),
    ("RJ","Barrett","TOR",9,"SF",23000000,21.8,5.4,4.1,.455,1.0),
    ("Immanuel","Quickley","TOR",5,"PG",13500000,18.6,3.8,6.8,.420,1.0),
    ("Jakob","Poeltl","TOR",19,"C",19500000,12.5,9.0,2.7,.570,3.0),
    ("Lauri","Markkanen","UTA",23,"PF",18000000,25.6,8.2,1.9,.498,3.0),
    ("Collin","Sexton","UTA",2,"PG",16500000,14.9,2.6,3.2,.467,3.0),
    ("Jordan","Clarkson","UTA",0,"SG",14000000,16.0,3.4,3.9,.434,5.0),
    ("John","Collins","UTA",20,"PF",26578200,15.0,7.0,2.0,.530,1.0),
    ("Walker","Kessler","UTA",24,"C",3100000,8.0,7.5,0.7,.650,3.0),
    ("Kyle","Kuzma","WAS",33,"PF",23500000,22.2,7.2,3.7,.451,4.0),
    ("Jordan","Poole","WAS",13,"SG",27955000,17.4,2.6,5.6,.414,2.0),
    ("Bilal","Coulibaly","WAS",0,"SF",5200000,8.5,4.2,1.8,.440,2.0),
    ("Tyus","Jones","WAS",5,"PG",14000000,12.0,3.1,7.0,.465,1.0),
    ("Daniel","Gafford","WAS",21,"C",12400000,10.5,5.4,0.6,.680,2.0),
]


def seed_all():
    """Seed the PostgreSQL database with fallback NBA data."""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    print("[1/3] Seeding 30 NBA teams...")
    for t in TEAMS:
        cur.execute("""
            INSERT INTO teams
                (name, city, abbreviation, conference, division,
                 arena, founded_year, primary_color, accent_color)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (name) DO NOTHING
        """, t)
    conn.commit()

    cur.execute("SELECT team_id, abbreviation FROM teams")
    abbr_map = {row[1]: row[0] for row in cur.fetchall()}

    print("[2/3] Seeding players and stats...")
    seasons = ['2025-26', '2024-25', '2023-24', '2022-23', '2021-22']
    import random
    random.seed(42)

    for (first, last, abbr, jersey, pos, salary, ppg, rpg, apg, fg, yrs) in PLAYERS:
        team_id = abbr_map.get(abbr)
        if not team_id:
            continue

        contract = 'Max' if salary > 35000000 else 'Standard' if salary > 10000000 else 'Rookie'
        cur.execute("""
            INSERT INTO players
                (first_name, last_name, jersey_number, team_id,
                 position, salary, years_on_team, contract_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING player_id
        """, (first, last, jersey, team_id, pos, salary, yrs, contract))

        row = cur.fetchone()
        pid = row[0] if row else None

        if not pid:
            cur.execute(
                "SELECT player_id FROM players WHERE first_name=%s AND last_name=%s",
                (first, last)
            )
            row = cur.fetchone()
            pid = row[0] if row else None

        if pid:
            for i, season in enumerate(seasons):
                factor = 1.0 - (i * 0.04) + random.uniform(-0.03, 0.03)
                gp = random.randint(50, 78)
                cur.execute("""
                    INSERT INTO player_stats
                        (player_id, season_year, games_played, ppg, rpg, apg,
                         spg, bpg, fg_pct, three_pct, ft_pct)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (player_id, season_year) DO NOTHING
                """, (
                    pid, season, gp,
                    round(ppg * factor, 1),
                    round(rpg * factor, 1),
                    round(apg * factor, 1),
                    round(random.uniform(0.6, 1.8), 1),
                    round(random.uniform(0.2, 1.5), 1),
                    round(fg * factor, 3),
                    round(random.uniform(0.300, 0.420), 3),
                    round(random.uniform(0.720, 0.910), 3),
                ))

    conn.commit()

    cur.execute("SELECT COUNT(*) FROM players")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM player_stats")
    stats = cur.fetchone()[0]
    print(f"   -> {total} players, {stats} stat records")
    print("[3/3] Seed complete!")
    cur.close()
    conn.close()


if __name__ == '__main__':
    from database import init_db
    init_db()
    seed_all()
