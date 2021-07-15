import requests
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
import numpy as np

#Standard python libraries
import pandas as pd
import seaborn as sns
# sns.set_context('talk')
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings(action='ignore') 

# Preprocessing tools
from sklearn.model_selection import train_test_split,cross_val_predict,cross_validate
from sklearn.preprocessing import MinMaxScaler,StandardScaler,OneHotEncoder
scaler = StandardScaler()
from sklearn import metrics

# Models & Utilities
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression,LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_score, recall_score, f1_score

# Warnings
import warnings
warnings.filterwarnings(action='ignore') 

# NLP Libraries
import nltk
import collections
# nltk.download('punkt')
from sklearn.manifold import TSNE
from nltk.tokenize import word_tokenize
from nltk import regexp_tokenize
import re
from nltk.corpus import stopwords
from nltk.collocations import *
from nltk import FreqDist
from nltk import word_tokenize
from nltk import ngrams
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('stopwords')
# !pip install wordcloud
from wordcloud import WordCloud

import json
def get_keys(path):
    with open(path) as f:
        return json.load(f)
# keys = get_keys("/Users/Johnny/.secret/yelp_api.json")
# api_key = keys['api_key']
# pip install tmdbsimple #Ctrl+? this line to install tmdbsimple
import tmdbsimple as tmdb
# tmdb.API_KEY = api_key

scrape = False

import ast
import time
import http.client, urllib.request, urllib.parse, urllib.error, base64

api_key = 'ceeaacb7cf024c7485e00ef8457e42dc'


# user = 'Drymander'

import pickle
from tqdm import tqdm

# pip install isodate

import isodate


import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

df = pd.read_csv('match.csv')

st.title('Single Match Data')



import plotly.express as px
df = df
# fig = px.bar(df, x='TotalTimePlayed', y='Gamertag', orientation='h')
# fig.show()

# df = recent_match_stats('Drymander', back_count=0)

import plotly.graph_objects as go

fig = go.Figure(go.Bar(
            x=df['TotalTimePlayed'],
            y=df['Gamertag'],
            orientation='h',
            text=df['TotalTimePlayed'].round(0),
            textposition='auto'))

import plotly.graph_objects as go
from plotly.subplots import make_subplots
st.dataframe(df)

st.plotly_chart(fig)

st.bar_chart(df['TotalTimePlayed'])

from compare_stat import compare_stat

# def compare_stat(df, column_name):

#     # Separate player and enemy teams
#     df_player = df.loc[df['PlayerTeam'] == 'Player']
#     df_enemy = df.loc[df['PlayerTeam'] == 'Enemy']

#     # Sort total time played by descending
#     df_player = df_player.sort_values(by=[column_name])
#     df_enemy = df_enemy.sort_values(by=[column_name])

#     # Assign player / enemy colors
#     if df_player['TeamColor'].iloc[0] == 'Blue':
#         player_color = 'Blue'
#         enemy_color = 'Red'
#     else:
#         player_color = 'Red'
#         enemy_color = 'Blue'
    
#     # Make subplot and X axis range
#     fig = make_subplots(rows=2, cols=1, subplot_titles=['Player Team', 'Enemy Team'])
#     x_range = df[column_name].max()
    
#     # Player team sub plot
#     fig.add_trace(go.Bar(
#                 x=df_player[column_name],
#                 y=df_player['Gamertag'],
#                 orientation='h',
#                 text=df_player[column_name].round(2),
#                 textposition='auto',
#                 marker_color=player_color),
#                     row=1, col=1)
#     fig.update_xaxes(range=[0, x_range], row=1, col=1)
    
#     # Enemy team sub plot
#     fig.add_trace(go.Bar(
#                 x=df_enemy[column_name],
#                 y=df_enemy['Gamertag'],
#                 orientation='h',
#                 text=df_enemy[column_name].round(2),
#                 textposition='auto',
#                 marker_color=enemy_color),
#                     row=2, col=1)
#     fig.update_xaxes(range=[0, x_range], row=2, col=1)
    
    # Show plot
#     fig.show()
    
#     return fig

fig = compare_stat(df, 'TotalTimePlayed')

st.plotly_chart(fig)












# fig = plt.figure()
# fig.patch.set_facecolor('white')
# fig.patch.set_alpha(0.6)

# ax = plt.axes()
# ax.set_facecolor("white")
# # OR

# plt.barh( df['Gamertag'], df['TotalTimePlayed'].sort_values())

# # setting label of y-axis
# plt.ylabel("Gamertag")
  
# # setting label of x-axis
# plt.xlabel("Hours") 
# plt.title("Time Played")
# plt.show()

