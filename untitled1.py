# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UNoO6mldEYXEMZnerVDnqBxJt3N8BzfM
"""

#open source library to manipulate data. Specifically data structure like tables
import pandas as pd
import numpy as np
import Recommenders as Recommenders

#load csv file in panda framework
song_1 = pd.read_csv("/content/triplets_file.csv")
#head is for read the top 5
song_1.head()

song_2 = pd.read_csv("/content/song_data.csv")
song_2.head()

# combine both data and there will be a duplicate column .Here it's song_id
#data_frame.drop_duplicates in pandas
song_df = pd.merge(song_1, song_2.drop_duplicates(['song_id']), on='song_id', how='left')
song_df.head()

print(len(song_1), len(song_2))

len(song_df)

# creating new feature combining title and artist name
song_df['song'] = song_df['title']+' - '+song_df['artist_name']
song_df.head()

# taking top 10k samples for quick results
song_df = song_df.head(10000)

# cummulative sum of listen count of the songs
# merge the song and artist_name into one column, aggregated by number of time a particular song is 
#listened
song_group = song_df.groupby(['song']).agg({'listen_count':'count'}).reset_index()
song_group.head()

grouped_sum = song_group['listen_count'].sum()
song_group['percentage'] = (song_group['listen_count'] / grouped_sum ) * 100
song_group.sort_values(['listen_count', 'song'], ascending=[0,1])

rpr = Recommenders.popularity_recommender_py()

rpr.create(song_df, 'user_id', 'song')

# display the top 10 popular songs
rpr.recommend(song_df['user_id'][5])

# It first get a unique count of user_id (ie the number of time that song was listened to in general by all user) for each song and 
#tag it as a score
rpr.recommend(song_df['user_id'][100])

#content based recommendation. Based on user history 
rir = Recommenders.item_similarity_recommender_py()
rir.create(song_df, 'user_id', 'song')

user_items = rir.get_user_items(song_df['user_id'][5])

# display user songs history
for user_item in user_items:
    print(user_item)

# give song recommendation for that user
rir.recommend(song_df['user_id'][3])

# give related songs based on the words
#We can also use our item similarity based collaborative filtering model to find similar songs
# to any songs in our dataset:


rir.get_similar_items(['Oliver James - Fleet Foxes', 'The End - Pearl Jam','One Time - Justin Bieber'])





