
# Function that combines all functions above to go through each step to
# Get the match dataframe
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

# Show full dataframe for match
df = recent_match_stats('Drymander', back_count=0)
df
