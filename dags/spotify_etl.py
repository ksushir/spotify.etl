import sqlalchemy
import pandas as pd
import datetime
import json
import requests
import sqlite3
from consts import TOKEN, URL



def check_if_valid_data(df : pd.DataFrame) -> bool:
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False

#primary key check
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception('Primary key check is violated')

#check for nulls
    if df.isnull().values.any():
        raise Exception('Null valued found')

# check that all timestamps is yesterday's date
    # yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    # yesterday = yesterday.replace(hour=0,minute=0,second=0,microsecond=0)

    # timestamps = df['timestamp'].tolist()
    # for timestamp in timestamps:
    #     if datetime.datetime.strptime(timestamp, '%Y-%m-%d') == yesterday:
    #         raise Exception('At least one of returned songs does not come from within the last 24 hours')
    # return True 



def run_spotify_etl():
    DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"

    res = requests.get(url=URL, headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
        'Authorization': 'Bearer {}'.format(TOKEN)
    }, params={"limit":40})

    #print(res)
    data = res.json()


    # class Spotify:
    #     artists = []
    #     def __init__(self, data):
    #         self.data = data

    #     def display_info(self):
    #         return f"Artist: {self.data}"

    #     van = data.items(artist)
    #     van.display_info()

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in data['items']:
        song_names.append(song['track']['name'])
        artist_names.append(song['track']['album']['artists'][0]['name'])
        played_at_list.append(song['played_at'])
        timestamps.append(song['played_at'][0:10])

    song_dict = {
        'song_name' : song_names,
        'artist_name' : artist_names,
        'played_at' : played_at_list,
        'timestamp' : timestamps
    }

    song_df = pd.DataFrame(song_dict, columns= ['song_name','artist_name', 'played_at', 'timestamp'])
    print(song_df)


    #Validate
    if check_if_valid_data(song_df):
        print("Data valid, proceed to load stage")

    #Load
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = """
        CREATE TABLE IF NOT EXISTS my_played_tracks(
            song_name VARCHAR(200),
            artist_name VARCHAR(200),
            played_at VARCHAR(200),
            timestamp VARCHAR(200),
            CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
        )
        """

    cursor.execute(sql_query)
    print("Opened database succesfully")

    try:
        song_df.to_sql('my_played_tracks', engine, index=False, if_exists='append')
    except:
        print('Data alredy exists in the database')

    conn.close()
    print('Close database')