import json
import pandas as pd

with open('/Users/saisandeep/GitRepo/musical-eureka/YoutubeDataAnalysis/Data/Takeout/YouTube and YouTube Music/history/watch-history.json', 'r') as file:
    data = json.load(file)

extracted_data = []

# Loop through each entry in the JSON data
for entry in data:
    # Extract relevant information
    entry_data = {
        'header': entry.get('header'),
        'title': entry.get('title'),
        'titleUrl': entry.get('titleUrl'),
        'subtitles': ', '.join([subtitle['name'] for subtitle in entry.get('subtitles', [])]),
        'time': entry.get('time'),
        'products': ', '.join(entry.get('products', [])),
        'activityControls': ', '.join(entry.get('activityControls', []))
    }
    extracted_data.append(entry_data)

# Create a DataFrame from the extracted data
df = pd.DataFrame(extracted_data)

# Display the DataFrame
print(df)