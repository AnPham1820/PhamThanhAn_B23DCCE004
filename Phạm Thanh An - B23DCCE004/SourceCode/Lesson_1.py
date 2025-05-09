import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}
session.headers.update(headers)

base_url = "https://fbref.com"

def get_page(url):
    try:
        time.sleep(random.uniform(3, 6))
        
        response = session.get(url, timeout=60)
        response.raise_for_status()
        
        if 'text/html' not in response.headers.get('Content-Type', ''):
            raise ValueError("Invalid content type")
            
        return response.text
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def data_player(player_name):
    return {
        "Name": player_name,
        "Team": "N/a",
        "Nation": "N/A",
        "Position": "N/A",
        "Age": "N/a",
        "Matches Played": "N/a",
        "Starts": "N/a",
        "Minutes": "N/a",
        "Goals": "N/a",
        "Assists": "N/a",
        "Yellow Cards": "N/a",
        "Red Cards": "N/a",
        "Expected Goals (xG)": "N/a",
        "Expected Assist Goals (xAG)": "N/a",
        "Progressive Carries in Progression": "N/a",
        "Progressive Passes in Progression": "N/a",
        "Progressive Passes Received in Progression": "N/a",
        "Goals Scored per 90 minutes": "N/a",
        "Assists per 90 minutes": "N/a",
        "Expected Goals per 90 minutes": "N/a",
        "Expected Assists Goals per 90 minutes": "N/a",
        "Goals Against per 90 minutes": "N/a",
        "Save Percentage": "N/a",
        "Clean Sheets Percentage": "N/a",
        "Penalty Save Percentage": "N/a",
        "Percentage Of Shots That Are On Target": "N/a",
        "Shots on target per 90 minutes": "N/a",
        "Goals Per Shot": "N/a",
        "Average Shot Distance": "N/a",
        "Passes Completed": "N/a",
        "Pass Completion Percentage": "N/a",
        "Total Pass Distance": "N/a",
        "Short Pass Completion": "N/a",
        "Medium Pass Completion": "N/a",
        "Long Pass Completion": "N/a",
        "Key Passes": "N/a",
        "Passes into Final Third": "N/a",
        "Passes into Penalty Area": "N/a",
        "Crosses into Penalty Area": "N/a",
        "Expected Progressive Passing": "N/a",
        "Shot Creating Actions": "N/a",
        "Shot Creating Actions per 90": "N/a",
        "Goal Creating Actions": "N/a",
        "Goal Creating Actions per 90": "N/a",
        "Tackles": "N/a",
        "Tackles Won": "N/a",
        "Tackle Attempts": "N/a",
        "Tackles Lost": "N/a",
        "Blocks": "N/a",
        "Shots Blocked": "N/a",
        "Passes Blocked": "N/a",
        "Interceptions": "N/a",
        "Touches": "N/a",
        "Touches in Defensive Penalty Area": "N/a",
        "Touches in Defensive Third": "N/a",
        "Touches in Middle Third": "N/a",
        "Touches in Attacking Third": "N/a",
        "Touches in Attacking Penalty Area": "N/a",
        "Take-ons Attempted": "N/a",
        "Percentage of Take-Ons Completed Successfully": "N/a",
        "Tackled on Take-on Percentage": "N/a",
        "Carries": "N/a",
        "Progressive Carry Distance": "N/a",
        "Progressive Carries in Carries": "N/a",
        "Carries into Final Third": "N/a",
        "Carries into Penalty Area": "N/a",
        "Miscontrolls": "N/a",
        "Dispossessed": "N/a",
        "Passes Received": "N/a",
        "Progressive Passes Received in Receiving": "N/a",
        "Fouls Committed": "N/a",
        "Fouls Drawn": "N/a",
        "Offsides": "N/a",
        "Crosses": "N/a",
        "Ball Recoveries": "N/a",
        "Aerial Duels Won": "N/a",
        "Aerial Duels Lost": "N/a",
        "Aerial Duel Win Percentage": "N/a"
    }

player_dict = {}

def Standard_Stats(html, team):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'stats_standard_9'})
    
    if not table:
        print("Table Standard Stats not found")
        return
    
    team_name = team
    body = table.find('tbody')
    
    stats_mapping = {
        'Nation': ('nationality', lambda x: x.split()[-1] if ' ' in x else x),
        'Position': ('position', None),
        'Age': ('age', None),
        'Matches Played': ('games', None),
        'Starts': ('games_starts', None),
        'Goals': ('goals', None),
        'Assists': ('assists', None),
        'Yellow Cards': ('cards_yellow', None),
        'Red Cards': ('cards_red', None),
        'Expected Goals (xG)': ('xg', None),
        'Expected Assist Goals (xAG)': ('xg_assist', None),
        'Progressive Carries in Progression': ('progressive_carries', None),
        'Progressive Passes in Progression': ('progressive_passes', None),
        'Progressive Passes Received in Progression': ('progressive_passes_received', None),
        'Goals Scored per 90 minutes': ('goals_per90', None),
        'Assists per 90 minutes': ('assists_per90', None),
        'Expected Goals per 90 minutes': ('xg_per90', None),
        'Expected Assists Goals per 90 minutes': ('xg_assist_per90', None)
    }
    
    for row in body.find_all('tr'):
        player_cell = row.find('th', {'data-stat': 'player'})
        if not player_cell:
            continue
            
        player_name = player_cell.find('a')
        if not player_name:
            continue
            
        minutes_cell = row.find('td', {'data-stat': 'minutes'})
        if minutes_cell:
            minutes_text = minutes_cell.text.strip().replace(',', '')
            if not minutes_text:
                continue
                
            try:
                minutes_played = int(minutes_text)
                if minutes_played < 90:
                    continue
            except ValueError:
                continue
                
        if player_name.text not in player_dict:
            player_dict[player_name.text] = data_player(player_name.text)
            player_dict[player_name.text]["Team"] = team_name
            player_dict[player_name.text]["Minutes"] = minutes_played
        
        for field, (stat, processor) in stats_mapping.items():
            element = row.find('td', {'data-stat': stat})
            if element:
                value = element.text.strip()
                if processor:
                    value = processor(value)
                player_dict[player_name.text][field] = value 

def Goalkeeping(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'stats_keeper_9'})
    
    if not table:
        print("Table Goalkeeping not found")
        return
    
    goalkeeping_stats = {
        "Goals Against per 90 minutes": "gk_goals_against_per90",
        "Save Percentage": "gk_save_pct",
        "Clean Sheets Percentage": "gk_clean_sheets_pct",
        "Penalty Save Percentage": "gk_pens_save_pct"
    }
    
    for row in table.find('tbody').find_all('tr'):
        player_cell = row.find('th', {'data-stat': 'player'})
        if not player_cell:
            continue
            
        player_name = player_cell.find('a')
        if not player_name or player_name.text not in player_dict:
            continue
        
        for stat_name, data_stat in goalkeeping_stats.items():
            stat_cell = row.find('td', {'data-stat': data_stat})
            if stat_cell and stat_cell.text.strip():
                player_dict[player_name.text][stat_name] = stat_cell.text.strip()

def Shooting(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'stats_shooting_9'})
    
    if not table:
        print("Table Shooting not found")
        return
    
    shooting_stats = {
        "Percentage Of Shots That Are On Target": "shots_on_target_pct",
        "Shots on target per 90 minutes": "shots_on_target_per90",
        "Goals Per Shot": "goals_per_shot",
        "Average Shot Distance": "average_shot_distance"
    }
    
    for row in table.find('tbody').find_all('tr'):
        player_cell = row.find('th', {'data-stat': 'player'})
        if not player_cell:
            continue
            
        player_name = player_cell.find('a')
        if not player_name or player_name.text not in player_dict:
            continue
        
        for stat_name, data_stat in shooting_stats.items():
            stat_cell = row.find('td', {'data-stat': data_stat})
            if stat_cell and stat_cell.text.strip():
                player_dict[player_name.text][stat_name] = stat_cell.text.strip()

def Passing(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'stats_passing_9'})
    
    if not table:
        print("Table Passing not found")
        return
    
    passing_stats = {
        "Passes Completed": "passes_completed",
        "Pass Completion Percentage": "passes_pct",
        "Total Pass Distance": "passes_total_distance",
        "Short Pass Completion": "passes_pct_short",
        "Medium Pass Completion": "passes_pct_medium",
        "Long Pass Completion": "passes_pct_long",
        "Key Passes": "assisted_shots",
        "Passes into Final Third": "passes_into_final_third",
        "Passes into Penalty Area": "passes_into_penalty_area",
        "Crosses into Penalty Area": "crosses_into_penalty_area",
        "Expected Progressive Passing": "progressive_passes"
    }
    
    for row in table.find('tbody').find_all('tr'):
        player_cell = row.find('th', {'data-stat': 'player'})
        if not player_cell:
            continue
            
        player_name = player_cell.find('a')
        if not player_name or player_name.text not in player_dict:
            continue
        
        for stat_name, data_stat in passing_stats.items():
            stat_cell = row.find('td', {'data-stat': data_stat})
            if stat_cell and stat_cell.text.strip():
                player_dict[player_name.text][stat_name] = stat_cell.text.strip()

def Goal_and_Shot_Creation(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'stats_gca_9'})
    
    if not table:
        print("Table Goal and Shot Creation not found")
        return
    
    STATS_CONFIG = {
        "Shot Creating Actions": "sca",
        "Shot Creating Actions per 90": "sca_per90", 
        "Goal Creating Actions": "gca",
        "Goal Creating Actions per 90": "gca_per90"
    }
    
    tbody = table.find('tbody')
    if not tbody:
        return
    
    for row in tbody.find_all('tr'):
        player_cell = row.find('th', {'data-stat': 'player'})
        if not player_cell:
            continue
            
        player_name = player_cell.find('a')
        if not player_name or player_name.text not in player_dict:
            continue
        
        for stat_name, data_stat in STATS_CONFIG.items():
            stat_value = row.find('td', {'data-stat': data_stat})
            if stat_value and stat_value.text.strip():
                player_dict[player_name.text][stat_name] = stat_value.text.strip()

def Defensive_Actions(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'stats_defense_9'})
    
    if not table:
        print("Table Defensive Actions not found")
        return
    
    DEFENSIVE_STATS = {
        "Tackles": "tackles",
        "Tackles Won": "tackles_won",
        "Tackle Attempts": "challenges",
        "Tackles Lost": "challenges_lost",
        "Blocks": "blocks",
        "Shots Blocked": "blocked_shots",
        "Passes Blocked": "blocked_passes",
        "Interceptions": "interceptions"
    }
    
    tbody = table.find('tbody')
    if not tbody:
        return
    
    for row in tbody.find_all('tr'):
        player_cell = row.find('th', {'data-stat': 'player'})
        if not player_cell:
            continue
            
        player_name = player_cell.find('a')
        if not player_name or player_name.text not in player_dict:
            continue
        
        for stat_name, data_attr in DEFENSIVE_STATS.items():
            stat_cell = row.find('td', {'data-stat': data_attr})
            if stat_cell and stat_cell.text.strip():
                player_dict[player_name.text][stat_name] = stat_cell.text.strip()

def Possession(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'stats_possession_9'})
    
    if not table:
        print("Table Possession not found")
        return
    
    POSSESSION_STATS = {
        "Touches": "touches",
        "Touches in Defensive Penalty Area": "touches_def_pen_area",
        "Touches in Defensive Third": "touches_def_3rd",
        "Touches in Middle Third": "touches_mid_3rd",
        "Touches in Attacking Third": "touches_att_3rd",
        "Touches in Attacking Penalty Area": "touches_att_pen_area",
        
        "Take-ons Attempted": "take_ons",
        "Percentage of Take-Ons Completed Successfully": "take_ons_won_pct",
        "Tackled on Take-on Percentage": "take_ons_tackled_pct",
        
        "Carries": "carries",
        "Progressive Carry Distance": "carries_progressive_distance",
        "Progressive Carries in Carries": "progressive_carries",
        "Carries into Final Third": "carries_into_final_third",
        "Carries into Penalty Area": "carries_into_penalty_area",
        "Miscontrolls": "miscontrols",
        "Dispossessed": "dispossessed",
        
        "Passes Received": "passes_received",
        "Progressive Passes Received in Receiving": "progressive_passes_received"
    }
    
    tbody = table.find('tbody')
    if not tbody:
        return
    
    for row in tbody.find_all('tr'):
        player_cell = row.find('th', {'data-stat': 'player'})
        if not player_cell:
            continue
            
        player_name = player_cell.find('a')
        if not player_name or player_name.text not in player_dict:
            continue
        
        for stat_name, data_attr in POSSESSION_STATS.items():
            stat_cell = row.find('td', {'data-stat': data_attr})
            if stat_cell and stat_cell.text.strip():
                player_dict[player_name.text][stat_name] = stat_cell.text.strip()

def Miscellaneous_Stats(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'stats_misc_9'})
    
    if not table:
        print("Table Miscellaneous Stats not found")
        return
    
    MISC_STATS = {
        "Fouls Committed": "fouls",
        "Fouls Drawn": "fouled",
        "Offsides": "offsides",
        "Crosses": "crosses",
        "Ball Recoveries": "ball_recoveries",
        "Aerial Duels Won": "aerials_won",
        "Aerial Duels Lost": "aerials_lost",
        "Aerial Duel Win Percentage": "aerials_won_pct"
    }
    
    tbody = table.find('tbody')
    if not tbody:
        return
    
    for row in tbody.find_all('tr'):
        player_cell = row.find('th', {'data-stat': 'player'})
        if not player_cell:
            continue
            
        player_name = player_cell.find('a')
        if not player_name or player_name.text not in player_dict:
            continue
        
        for stat_name, data_attr in MISC_STATS.items():
            stat_cell = row.find('td', {'data-stat': data_attr})
            if stat_cell and stat_cell.text.strip():
                player_dict[player_name.text][stat_name] = stat_cell.text.strip()

url = "https://fbref.com/en/"
htmls = get_page(url)

if htmls:
    soup = BeautifulSoup(htmls, 'html.parser')
    team_links = {}
    team_count = 1
    total_teams = 20
    
    if not (table := soup.find('table', {'id': 'results2024-202591_overall'})):
        print("Error: Results table not found")
    else:
        for row in table.find('tbody').find_all('tr'):
            if (team_cell := row.find('td', {'data-stat': 'team'})) and \
               (a_tag := team_cell.find('a')) and \
               a_tag.has_attr('href'):
                team_links[a_tag.text.strip()] = f"{base_url}{a_tag['href']}"

        for team_name, team_url in team_links.items():
            print(f"Collecting data for {team_name} ({team_count}/{total_teams})...", 
                  end=' ', flush=True)
            team_count += 1
            
            if not (team_html := get_page(team_url)):
                print(f"Error: Failed to retrieve {team_url}")
                continue

            try:
                stats_processors = [
                    (Standard_Stats, (team_html, team_name)),
                    (Goalkeeping, (team_html,)),
                    (Shooting, (team_html,)),
                    (Passing, (team_html,)),
                    (Goal_and_Shot_Creation, (team_html,)),
                    (Defensive_Actions, (team_html,)),
                    (Possession, (team_html,)),
                    (Miscellaneous_Stats, (team_html,))
                ]
            
                for processor, args in stats_processors:
                    processor(*args)
                print("Success!")
                
            except Exception as e:
                print(f"Error processing {team_name}: {str(e)}")
                
            time.sleep(random.uniform(5, 10))
else:
    print("Error: Could not access the main page")

if player_dict:
    output_file = 'results.csv'
    (pd.DataFrame.from_dict(player_dict, orient='index')
       .sort_values(by='Name')
       .to_csv(output_file, index=False, encoding='utf-8-sig'))
    print(f"Success! Data exported to {output_file}")
else:
    print("Warning: No player data was collected")