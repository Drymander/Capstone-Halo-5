
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

# df = build_base_dataframe(pull_recent_match(8), 'Drymander')

# df
