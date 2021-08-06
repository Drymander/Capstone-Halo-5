### YOUR API KEY ###
api_key = 'ceeaacb7cf024c7485e00ef8457e42dc'

#Standard Packages
import pandas as pd
pd.set_option('display.max_columns', None)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pickle
import warnings
warnings.filterwarnings(action='ignore') 

# Packages used for API calls and data processing
import requests
import json
def get_keys(path):
    with open(path) as f:
        return json.load(f)
import ast
import time
import http.client, urllib.request, urllib.parse, urllib.error, base64
gamertag = 'Drymander'
from tqdm import tqdm
# !pip install isodate
import isodate
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

###################################### Pickle files

# Loading GameBaseVariantId metadata dictionary pulled from API
with open('data/GameBaseVariantId.pkl', 'rb') as GameBaseVariantId_pickle:
    GameBaseVariantId_dic = pickle.load(GameBaseVariantId_pickle)

# Loading PlaylistId metadata dictionary pulled from API
with open('data/PlaylistId_dic.pkl', 'rb') as PlaylistId_dic_pickle:
    PlaylistId_dic = pickle.load(PlaylistId_dic_pickle)

# Loading map_list metadata dictionary pulled from API
with open('data/map_list.pkl', 'rb') as map_list_pickle:
    map_list = pickle.load(map_list_pickle)


# Prepare gamertag for API
def gamertag_for_api(gamertag):
    
    # Replace spaces with '+'
    gamertag = gamertag.replace(' ','+')
    return gamertag


# Function to pull most recent match stats into JSON format
# Uses two separate API calls, one from player history and another from match details
def pull_recent_match(how_recent, api_key=api_key, explore=False, gamertag='Drymander'):
    
    # Use gamertag_for_api function to remove any spaces
    gamertag = gamertag_for_api(gamertag)
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': api_key,
    }
    # Pulls from arena mode, how_recent is how far to go back in the match history
    # 'count' refers to the number of matches to pull
    params = urllib.parse.urlencode({
        # Request parameters
        'modes': 'arena',
        'start': how_recent,
        'count': 1,
        'include-times': True,
    })
    
    # Try this, otherwise return error message
    try:
        
        # Connect to API and pull most recent match for specified gamer
        conn = http.client.HTTPSConnection('www.haloapi.com')
        conn.request("GET", f"/stats/h5/players/{gamertag}/matches?%s" % params, "{body}", headers)
        response = conn.getresponse()
        latest_match = json.loads(response.read())
        
        # Identify match ID and match date
        match_id = latest_match['Results'][0]['Id']['MatchId']
        match_date = latest_match['Results'][0]['MatchCompletedDate']['ISO8601Date']
        
        # Rest for 1.01 seconds to not get blocked by API
        time.sleep(1.01)
        
        # Using match_id, pull details from match
        conn.request("GET", f"/stats/h5/arena/matches/{match_id}?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        
        # Option to return as byte string for alternative viewing
        if explore == True:
            print(data)
        else:
            # Append match ID and date from player history API call
            match_results = json.loads(data)
            match_results['MatchId'] = match_id
            match_results['Date'] = match_date
        conn.close()
    
    # Print error if issue with calling API
    except Exception as e:
        print(f"[Errno {0}] {1}".format(e.errno, e.strerror))
    
    # Return match results as JSON
    return match_results


# Function to build the base dataframe for a single match
# Designed to take in the JSON provided by the pull_recent_match function
def build_base_dataframe(match_results, gamertag):
    
    # Build empty base match dataframe
    df = pd.DataFrame()
    columns = [
        'Finished'
        'TeamId',
        'Gamertag',
        'SpartanRank',
        'PrevTotalXP',
    ]
    df = pd.DataFrame(columns = columns)
    
    # Populate base match dataframe with player stats for each player
    i = 0
    for player in match_results['PlayerStats']:

        player_dic = {}
        # Team ID
        player_dic['DNF'] = match_results['PlayerStats'][i]['DNF']
        player_dic['TeamId'] = match_results['PlayerStats'][i]['TeamId']
        # Team Color
        player_dic['TeamColor'] = match_results['PlayerStats'][i]['TeamId']
        # Gamer Tag
        player_dic['Gamertag'] = match_results['PlayerStats'][i]['Player']['Gamertag']
        # Spartan Rank
        player_dic['SpartanRank'] = match_results['PlayerStats'][i]['XpInfo']['SpartanRank']
        # Previous Total XP
        player_dic['PrevTotalXP'] = match_results['PlayerStats'][i]['XpInfo']['PrevTotalXP']
        df = df.append(player_dic, ignore_index=True)
        i += 1
    
    ########## DATE, GAME VARIANT, MAP ID, MATCH ID, PLAYLIST ID ##########
    df['Date'] = match_results['Date']
    df['Date'] = pd.to_datetime(df['Date']).dt.tz_convert(None)
#     df['Date'] = df['Date'].floor('T')
    df['MatchId'] = match_results['MatchId']
    df['GameBaseVariantId'] = match_results['GameBaseVariantId']
    df['MapVariantId'] = match_results['MapVariantId']
    df['PlaylistId'] = match_results['PlaylistId']
    
    ########## DEFINE PLAYER TEAM ##########
    playerteam = df.loc[df['Gamertag'] == gamertag, 'TeamId'].values[0]
    if playerteam == 0:
        enemyteam = 1   
    else:
        enemyteam = 0
        
    df['PlayerTeam'] = df['TeamId'].map({playerteam:'Player', enemyteam:'Enemy'})
    
    if match_results['TeamStats'][0]['TeamId'] == playerteam:
        playerteam_stats = match_results['TeamStats'][0]
        enemyteam_stats = match_results['TeamStats'][1]
    else: 
        playerteam_stats = match_results['TeamStats'][1]
        enemyteam_stats = match_results['TeamStats'][0]
    
    ########## DETERMINE WINNER ##########
    # Tie
    if playerteam_stats['Rank'] == 1 and enemyteam_stats['Rank'] == 1:
        df['Winner'] = 'Tie'
    # Player wins
    elif playerteam_stats['Rank'] == 1 and enemyteam_stats['Rank'] == 2:
        df['Winner'] = df['TeamId'].map({playerteam:'Victory', enemyteam:'Defeat'})
    # Enemy wins
    elif playerteam_stats['Rank'] == 2 and enemyteam_stats['Rank'] == 1:
        df['Winner'] = df['TeamId'].map({enemyteam:'Victory', playerteam:'Defeat'})
    # Error handling
    else:
        winner = 'Error determining winner'
    
    ########## TEAM COLOR ##########
    df['TeamColor'] = df['TeamId'].map({0:'Red', 1:'Blue'})
    
    # Set columns
    df = df[['Date', 'MatchId', 'GameBaseVariantId', 'PlaylistId', 'MapVariantId', 'DNF',
             'TeamId', 'PlayerTeam', 'Winner', 'TeamColor', 
             'Gamertag', 'SpartanRank', 'PrevTotalXP',
            ]]
    # Sort match by winning team
    df = df.sort_values(by=['Winner'], ascending=False)
    
    return df


# Function to combine all gamertags from the match and prepare them in string
# format for the next API call
def get_player_list(df):
    
    # Create list from our df['Gamertag'] column and remove the brackets
    player_list = str(list(df['Gamertag']))[1:-1]
    
    # Format string for API
    player_list = player_list.replace(', ',',')
    player_list = player_list.replace("'",'')
    player_list = player_list.replace(' ','+')
    
    # Return in one full string
    return player_list


# Function to pull more informative information about each player in the match
# This information is not available in the two previous API calls
def get_player_history(df, readable=False):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': str(api_key),
    }
    params = urllib.parse.urlencode({
    })
    # Use our function in the block above the prepare the gamertags for the API
    player_list_api = get_player_list(df)
    
    # Try calling service records API using our player list
    try:
        conn = http.client.HTTPSConnection('www.haloapi.com')
        conn.request("GET", f"/stats/h5/servicerecords/arena?players={player_list_api}&%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        player_history = json.loads(data)
        conn.close()
    
    # Return error if issue with API
    except Exception as e:
        print(f"[Errno {0}] {1}".format(e.errno, e.strerror))
    
    # Option to view in byte string readable format
    if readable == False:
        return player_history
    else:
        return data


# Function to build secondary dataframe with more informative player stats
def build_history_dataframe(player_history, variant_id, streamlit=False):
    
    # Option to view 'streamlit' dataframe, which includes pertinent
    # information but excludes all stats for modeling
    if streamlit == True:
        vdf_columns = ['Gamertag','TotalTimePlayed','K/D','Accuracy','WinPercent']
        vdf = pd.DataFrame(columns = vdf_columns)
    else:
        stat_list = ['Gamertag', 'TotalKills', 'TotalHeadshots', 'TotalWeaponDamage', 'TotalShotsFired',
                    'TotalShotsLanded', 'TotalMeleeKills', 'TotalMeleeDamage', 'TotalAssassinations',
                    'TotalGroundPoundKills', 'TotalGroundPoundDamage', 'TotalShoulderBashKills',
                    'TotalShoulderBashDamage', 'TotalGrenadeDamage', 'TotalPowerWeaponKills',
                    'TotalPowerWeaponDamage', 'TotalPowerWeaponGrabs', 'TotalPowerWeaponPossessionTime',
                    'TotalDeaths', 'TotalAssists', 'TotalGamesCompleted', 'TotalGamesWon',
                    'TotalGamesLost', 'TotalGamesTied', 'TotalTimePlayed','TotalGrenadeKills']
        vdf = pd.DataFrame(columns = stat_list)
    
    # Set coutner variable
    i = 0
    # Loop the goes through each player in the player history JSON
    for player in player_history['Results']:
        
        # Loop that goes through each Arena Game Base Variant and locates
        # the details specific to the game vase variant of the match
        for variant in player['Result']['ArenaStats']['ArenaGameBaseVariantStats']:
            if variant['GameBaseVariantId'] == variant_id:
                variant_stats = variant
        
        # Create empty dictionary where stats will be added
        variant_dic = {}
        
        # Streamlit option - calculates specifc features
        if streamlit == True:
            variant_dic['Gamertag'] = player_history['Results'][i]['Id']
            variant_dic['TotalTimePlayed']= isodate.parse_duration(variant_stats['TotalTimePlayed']).total_seconds() / 3600
            variant_dic['K/D'] = variant_stats['TotalKills'] / variant_stats['TotalDeaths']
            variant_dic['Accuracy'] = variant_stats['TotalShotsLanded'] / variant_stats['TotalShotsFired']
            variant_dic['WinPercent'] = (variant_stats['TotalGamesWon'] / variant_stats['TotalGamesCompleted']) * 100
            vdf = vdf.append(variant_dic, True)
            i += 1
        
        # Modeling option - includes all features but does not yet calculate
        else:
            variant_dic['Gamertag'] = player_history['Results'][i]['Id']
            variant_dic['TotalTimePlayed']= isodate.parse_duration(variant_stats['TotalTimePlayed']).total_seconds() / 3600
            variant_dic['K/D'] = variant_stats['TotalKills'] / variant_stats['TotalDeaths']
            variant_dic['Accuracy'] = variant_stats['TotalShotsLanded'] / variant_stats['TotalShotsFired']
            variant_dic['WinPercent'] = (variant_stats['TotalGamesWon'] / variant_stats['TotalGamesCompleted']) * 100
            
            # Loop that appends all stats to variant dic
            for stat in stat_list[1:]:    
                variant_dic[stat] = variant_stats[stat]
            
            # Parsing ISO duration times
            variant_dic['TotalTimePlayed']= isodate.parse_duration(variant_stats['TotalTimePlayed']).total_seconds() / 3600
            variant_dic['TotalPowerWeaponPossessionTime']= isodate.parse_duration(variant_stats['TotalPowerWeaponPossessionTime']).total_seconds() / 3600
#             vdf = vdf.append(variant_dic, True)
#             i += 1
            
            # Per game stats
            per_game_stat_list = ['TotalKills', 'TotalHeadshots', 'TotalWeaponDamage', 
                                  'TotalShotsFired', 'TotalShotsLanded', 'TotalMeleeKills', 
                                  'TotalMeleeDamage', 'TotalAssassinations', 'TotalGroundPoundKills', 
                                  'TotalGroundPoundDamage', 'TotalShoulderBashKills', 
                                  'TotalShoulderBashDamage', 'TotalGrenadeDamage', 'TotalPowerWeaponKills', 
                                  'TotalPowerWeaponDamage', 'TotalPowerWeaponGrabs', 
                                  'TotalPowerWeaponPossessionTime', 'TotalDeaths', 'TotalAssists', 
                                  'TotalGrenadeKills']
            
            for stat in per_game_stat_list:
                per_game_stat_string = stat.replace('Total', '')
                per_game_stat_string = f'{per_game_stat_string}PerGame'
                variant_dic[per_game_stat_string] = variant_dic[stat] / variant_dic['TotalGamesCompleted']
            
            
            vdf = vdf.append(variant_dic, True)
            i += 1
            
    # Return the streamlit or modeling dataframe
    return vdf
    

# This function will convert codes provided by the API into a readable format
def decode_column(df, column, api_dict):
    
    # Empty list of decoded values
    decoded_list = []
    
    # Loop through each row
    for row in df[column]:
        i = 0
        
        # Loop through API dictionary
        for item in api_dict:
            
            # If code found, append it to list
            if item['id'] == row:
                name = item['name']
                decoded_list.append(name)
            
            # Otherwise keep searching until found
            else:
                i += 1
    
    # Return decoded list
    return decoded_list


# This function will convert maps to readable format
def decode_maps(df, column, api_dict):
    decoded_list = []
    
    # Loop through each row
    for row in df[column]:
        i = 0
        
        # Creating map_count variable
        map_count = len(api_dict)
        
        # For each item in API dictionary
        for item in api_dict:
            
            # If map cannot be found, name 'Custom Map'
            if (i+1) == map_count:
                name = 'Custom Map'
                decoded_list.append(name)
            
            # If found, assign value to code
            elif item['id'] == row:
                name = item['name']
                decoded_list.append(name)
            
            # Otherwise keep looping
            else:
                i += 1
    
    # Return decoded list
    return decoded_list


def recent_match_stats(gamertag, back_count=0):
    
    # Pull the match result as JSON from API
    match_results = pull_recent_match(back_count, explore=False, gamertag=gamertag)
    
    # Build the base dataframe
    base_df = build_base_dataframe(match_results, gamertag=gamertag)
    
    # Convert dates
    base_df['Date'] = base_df['Date'].dt.strftime('%B, %d %Y')
    
    # Decode GameBaseVariantId, PlaylistId, and MapVariantId
    base_df['GameBaseVariantId'] = decode_column(base_df, 'GameBaseVariantId', GameBaseVariantId_dic)    
    base_df['PlaylistId'] = decode_column(base_df, 'PlaylistId', PlaylistId_dic)
    base_df['MapVariantId'] = decode_maps(base_df, 'MapVariantId', map_list)
    
    # Sleep for 1.01 seconds to avoid issues with API
    time.sleep(1.01)
    
    # Create playerlist for player history API call
    player_list = get_player_list(base_df)
    
    # Call API to get player history JSON
    player_history = get_player_history(base_df)
    
    # Build base player stats dataframe based on player history API call
    history_df = build_history_dataframe(player_history, match_results['GameBaseVariantId'])
    
    # Merge the base dataframe and stats dataframe
    full_stats_df = pd.merge(base_df, history_df, how='inner', on = 'Gamertag')
    
    return full_stats_df


def compare_stat(df, column_name):
    
#     layout = go.Layout(
#         margin=go.layout.Margin(
#             l=100, #left margin
#             r=0, #right margin
#             b=0, #bottom margin
#             t=0))  #top margin
    
    df = df.round(2)
    # Separate player and enemy teams
    df_player = df.loc[df['PlayerTeam'] == 'Player']
    df_enemy = df.loc[df['PlayerTeam'] == 'Enemy']

    # Sort total time played by descending
    df_player = df_player.sort_values(by=[column_name])
    df_enemy = df_enemy.sort_values(by=[column_name])

    # Assign player / enemy colors
    if df_player['TeamColor'].iloc[0] == 'Blue':
        player_color = 'Blue'
        enemy_color = 'Red'
    else:
        player_color = 'Red'
        enemy_color = 'Blue'
    
    # Make subplot and X axis range
    fig = make_subplots(rows=2, cols=1, subplot_titles=[f'Player Team - {column_name}', 
                                                        f'Enemy Team - {column_name}'],
                       vertical_spacing = 0.12)
    x_range = df[column_name].max()
    
    # Player team sub plot
    fig.add_trace(go.Bar(
                x=df_player[column_name],
                y=df_player['Gamertag'],
                orientation='h',
                text=df_player[column_name],
                textposition='auto',
                marker_color=player_color),
                    row=1, col=1)
    fig.update_xaxes(range=[0, x_range], row=1, col=1)
    
    # Enemy team sub plot
    fig.add_trace(go.Bar(
                x=df_enemy[column_name],
                y=df_enemy['Gamertag'],
                orientation='h',
                text=df_enemy[column_name],
                textposition='auto',
                marker_color=enemy_color),
                    row=2, col=1)
    fig.update_xaxes(range=[0, x_range], row=2, col=1)
    fig.update_yaxes(automargin=True)
    fig['layout'].update(margin=dict(l=125,r=50,b=20,t=30))
    fig['layout'].update(showlegend=False)
#     fig.update_layout(title_text='test')
    return fig




######################################## Title and markdown
st.title('Welcome to Halo 5 Last Match!')
st.markdown('Halo 5 Last Match allows you to view performance stats for players in a recent Halo 5 Arena match. Start by entering your gamertag below. The second box will allow you to specify how many matches back you would like to go in your match history.')

######################################## Sidebar and buttons
st.sidebar.title("Additional Stats")
xp_stats = st.sidebar.button('XP / Time Played')
win_loss_stats = st.sidebar.button('Total Wins / Losses')
kd_stats = st.sidebar.button('K/D')
accuracy_stats = st.sidebar.button('Accuracy')
grenades = st.sidebar.button('Grenades')
weapon_damage = st.sidebar.button('Weapon Damage')
power_weapon_kills = st.sidebar.button('Power Weapon Kills')
power_weapon_grabs = st.sidebar.button('Power Weapon Grabs')
melee = st.sidebar.button('Melee')
assassinations = st.sidebar.button('Assassinations')
ground_pound = st.sidebar.button('Ground Pound')
shoulder_bash = st.sidebar.button('Shoulder Bash')



########################################### Input
gamertag = st.text_input("Type in your Gamertag", 'Drymander')
back_count = st.text_input("How many matches would you like to go back?  Enter 0 for most recent match, 1 to go 1 match back, 2 to go 2 matches back, etc.", 0)

st.markdown("Each stat is calculated by Game Base Variant (e.g. Slayer, Capture the Flag, Oddball, Strongholds, etc).  Below, you'll see Total Hours Played, Win Rate, and average K/D.")

st.markdown("You can also find additional stats on the sidebar.")

########################################### Dataframe
df = recent_match_stats(gamertag, back_count=back_count)
# df = pd.read_csv('match.csv')

####################################### Game type, playlist, map, win/lose/tie

df_outcome = df.loc[df['Gamertag'] == gamertag]

gamebasevariantid = df_outcome['GameBaseVariantId'].iloc[0]
playlistid = df_outcome['PlaylistId'].iloc[0]
map_name = df_outcome['MapVariantId'].iloc[0]
if df_outcome['Winner'].iloc[0] == 'Victory':
    outcome = 'VICTORY'
elif df_outcome['Winner'].iloc[0] == 'Defeat':
    outcome = 'DEFEAT'
else:
    outcome = 'TIE'
    
st.header(f"Showing stats for {gamertag}'s match on {df_outcome['Date'].iloc[0]}")
st.subheader(f'Outcome - {outcome}')
st.subheader(f'Game Mode - {gamebasevariantid}')
st.subheader(f'Playlist - {playlistid}')
st.subheader(f'Map - {map_name}')

######################################### Graphs

def show_stat(column_name, df=df, gamebasevariantid=gamebasevariantid):
    st.header(f'{column_name} - {gamebasevariantid}')
    stat_plot = compare_stat(df, column_name)
    st.plotly_chart(stat_plot)
    
if grenades:
    
    show_stat('GrenadeKillsPerGame')
    show_stat('GrenadeDamagePerGame')
    show_stat('TotalGrenadeKills')
    show_stat('TotalGrenadeDamage')
    
elif weapon_damage:
    show_stat('WeaponDamagePerGame')
    show_stat('TotalWeaponDamage')
    show_stat('PowerWeaponDamagePerGame')
    show_stat('TotalPowerWeaponDamage')

elif power_weapon_kills:
    show_stat('PowerWeaponKillsPerGame')
    show_stat('TotalPowerWeaponKills')

elif power_weapon_grabs:
    show_stat('PowerWeaponGrabsPerGame')
    show_stat('TotalPowerWeaponGrabs')
    show_stat('PowerWeaponPossessionTimePerGame')
    show_stat('TotalPowerWeaponPossessionTime')
    
elif kd_stats:
    show_stat('K/D')
    show_stat('KillsPerGame')
    show_stat('TotalKills')
    show_stat('DeathsPerGame')
    show_stat('TotalDeaths')
    show_stat('AssistsPerGame')
    show_stat('TotalAssists')
    
elif accuracy_stats:
    show_stat('Accuracy')
    show_stat('HeadshotsPerGame')
    show_stat('TotalHeadshots')
    show_stat('ShotsFiredPerGame')
    show_stat('ShotsLandedPerGame')
    show_stat('TotalShotsLanded')
    show_stat('TotalShotsFired')
    
elif melee:
    show_stat('MeleeKillsPerGame')
    show_stat('TotalMeleeKills')
    show_stat('MeleeDamagePerGame')
    show_stat('TotalMeleeDamage')
    
elif assassinations:
    show_stat('AssassinationsPerGame')
    show_stat('TotalAssassinations')

elif ground_pound:
    show_stat('GroundPoundKillsPerGame')
    show_stat('TotalGroundPoundKills')
    show_stat('GroundPoundDamagePerGame')
    show_stat('TotalGroundPoundDamage')

elif shoulder_bash:
    show_stat('ShoulderBashKillsPerGame')
    show_stat('TotalShoulderBashKills')
    show_stat('ShoulderBashDamagePerGame')
    show_stat('TotalShoulderBashDamage')
    
elif xp_stats:
    show_stat('SpartanRank')
    show_stat('PrevTotalXP')
    show_stat('TotalTimePlayed')

elif win_loss_stats:
    show_stat('WinPercent')
    show_stat('TotalGamesWon')
    show_stat('TotalGamesLost')
    show_stat('TotalGamesTied')
    show_stat('TotalGamesCompleted')

else:
    show_stat('WinPercent')
    show_stat('TotalTimePlayed')
    show_stat('K/D')
