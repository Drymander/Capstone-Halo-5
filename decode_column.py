
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
