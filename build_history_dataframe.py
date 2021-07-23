
# Function to build secondary dataframe with more informative player stats
def build_history_dataframe(player_history, variant_id, streamlit=False):
    
    # Option to view 'streamlit' dataframe, which includes pertinent
    # information but excludes all stats for modeling
    if streamlit == True:
        vdf_columns = ['Gamertag','TotalTimePlayed','K/D','Accuracy','WinRate']
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
            variant_dic['WinRate'] = variant_stats['TotalGamesWon'] / variant_stats['TotalGamesLost']
            vdf = vdf.append(variant_dic, True)
            i += 1
        
        # Modeling option - includes all features but does not yet calculate
        else:
            variant_dic['Gamertag'] = player_history['Results'][i]['Id']
            
            # Loop that appends all stats to variant dic
            for stat in stat_list[1:]:    
                variant_dic[stat] = variant_stats[stat]
            
            # Parsing ISO duration times
            variant_dic['TotalTimePlayed']= isodate.parse_duration(variant_stats['TotalTimePlayed']).total_seconds() / 3600
            vdf = vdf.append(variant_dic, True)
            i += 1
    
    # Return the streamlit or modeling dataframe
    return vdf
    
# build_history_dataframe(player_history, '1571fdac-e0b4-4ebc-a73a-6e13001b71d3', streamlit=False)
