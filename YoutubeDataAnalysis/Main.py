from dotenv import load_dotenv
from google.oauth2 import service_account
import googleapiclient
from googleapiclient.discovery import build
import json
import os
import pandas as pd
import re
from pathlib import Path
import time



def get_videometa(video_id):
    api_service_name = "youtube"
    api_version = "v3"
    service_account_file = "/Users/saisandeep/GitRepo/serivce_files/youtube-data-analysis-service.json"  # Replace with the path to your service account file

    credentials = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=["https://www.googleapis.com/auth/youtube.readonly"]
    )

    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    # Make the API request
    request = youtube.videos().list(
        # part="statistics",
        part="snippet,contentDetails,statistics,status,player,topicDetails",
        id=video_id
    )
    response = request.execute()    
    
    data = []
    for item in response['items']:
        video_info = {
            'id': item['id'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'publishedAt': item['snippet']['publishedAt'],
            'channelId': item['snippet']['channelId'],
            'channelTitle': item['snippet']['channelTitle'],
            'viewCount': item['statistics']['viewCount'],
            'likeCount': item['statistics']['likeCount'],
            'duration': item['contentDetails']['duration'],
            'privacyStatus': item['status']['privacyStatus'],
            # 'tags': ', '.join(item['snippet'].get('tags', []))
            'tags': item['snippet'].get('tags', [])
        }
        data.append(video_info)

    # Create DataFrame
    df = pd.DataFrame(data)
    return df


env_path = Path('/Users/saisandeep/GitRepo/musical-eureka/.env')
load_dotenv(env_path)
os.getenv('YOUTUBE_API_KEY')

# Load the JSON data from the file
with open('/Users/saisandeep/GitRepo/musical-eureka/YoutubeDataAnalysis/Data/Takeout/YouTube and YouTube Music/history/watch-history.json', 'r') as file:
    data = json.load(file)

# Initialize a list to hold the extracted information
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
df['video_id'] = df['titleUrl'].apply(lambda x: re.search(r'.*v=([^&]+)', x).group(1) if re.search(r'.*v=([^&]+)', x) else None)
# Convert the 'time' column to datetime with ISO8601 format
df['time'] = pd.to_datetime(df['time'], format='ISO8601')

# Extract the date from the 'time' column
df['watch_date'] = df['time'].dt.date

df=df.sort_values(by='watch_date',ascending=False)
df.to_csv('/Users/saisandeep/GitRepo/musical-eureka/YoutubeDataAnalysis/Data/watch_history.csv',index=False)
df_video_ids = df.drop_duplicates(subset=['video_id'])
df_video_ids = df_video_ids['video_id']
df_video_ids.to_csv('/Users/saisandeep/GitRepo/musical-eureka/YoutubeDataAnalysis/Data/video_ids.csv',index=False)


# Steps
# 1. Read the video_ids from the csv file
# 2. Create a set of video_ids from video_ids.csv and read the video_metadata from the csv file and create a set of video_ids from that
# 3. Compare the two sets and get the difference
# 4. From the difference get the video_ids 
# 5. Try to get the data for each video_id in the difference set
# 6. If there is an error and if it is due to limit breach store the video_id and its index in a .txt file
# 7. Incase of now error store the data in df and append it to the csv file

# Step 1: Read the video_ids from the csv file
df_video_ids = pd.read_csv('/Users/saisandeep/GitRepo/musical-eureka/YoutubeDataAnalysis/Data/video_ids.csv',header=0)
df_video_ids_set = set(df_video_ids['video_id'])

df_video_metadata_new = pd.read_csv('/Users/saisandeep/GitRepo/musical-eureka/YoutubeDataAnalysis/Data/video_metadata_new.csv',header=0)
df_video_metadata_new_set = set(df_video_metadata_new['id'])

# Step 3: Compare the two sets and get the difference
df_video_ids_diff = df_video_ids_set - df_video_metadata_new_set

# # Step 2: Read the index from in .txt file if it null or empty then start from 0 else read the last index and start from there
# index_file = '/Users/saisandeep/GitRepo/musical-eureka/YoutubeDataAnalysis/Data/index.txt'
# if os.path.exists(index_file):
#     with open(index_file, 'r') as file:
#         last_index = int(file.read())
# else:
#     last_index = 1

# Initialize an empty DataFrame to store the data
# df_data = pd.DataFrame()

# Loop through each video_id starting from the last index, with a limit of 100 every 5 minutes and 10000 every day
for index, video_id in enumerate(df_video_ids_diff):
    if index % 10000 == 0 and index != 0:  # Daily limit
        break
    try:
        print(video_id,index)
        # Step 3: Try to get the data for each video_id
        response = get_videometa(video_id)
        response.to_csv('/Users/saisandeep/GitRepo/musical-eureka/YoutubeDataAnalysis/Data/video_metadata_new.csv', mode='a', index=False, header=False)
        # Step 5: Incase of no error store the data in df and append it to the csv file
        # df_data = df_data._append(response, ignore_index=True)
        # with open(index_file, 'w') as file:
        #     file.write(str(index))
    except Exception as e:
        # Step 4: If there is an error and if it is due to limit breach store the video_id and its index in a .txt file
        if 'limit' in str(e):
            with open('/Users/saisandeep/GitRepo/musical-eureka/YoutubeDataAnalysis/Data/limit_breach.txt', 'a') as file:
                file.write(f'{video_id}: {index}\n')
        else:
            print(e)
            # If there is any other error apart from the limit breach, continue with the next video_id
            continue

# df_data.to_csv('/Users/saisandeep/GitRepo/musical-eureka/YoutubeDataAnalysis/Data/video_metadata.csv', mode='a', index=False, header=False)
# Update the last index in the index.txt file
# with open(index_file, 'w') as file:
#     file.write(str(index + last_index))