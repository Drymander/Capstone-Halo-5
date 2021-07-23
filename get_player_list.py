
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

# get_player_list(df)
