
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
