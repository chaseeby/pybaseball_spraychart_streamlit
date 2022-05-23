import streamlit as st
import pandas as pd
import numpy as np
import pybaseball
from pybaseball import statcast_batter, spraychart, league_batting_stats, league_pitching_stats
from datetime import date,timedelta
from pytz import timezone

st.title("MLB BATTING STATS")  #Title Of Report

# Date selector for grabbing statcast data from pybaseball
today = date.today() - timedelta(days=2)
start_date = st.sidebar.date_input('Start date',today)
end_date = st.sidebar.date_input('End date',today)
start_dt = start_date.strftime('%Y-%m-%d')
end_dt = end_date.strftime('%Y-%m-%d')


pybaseball.cache.enable()

batting = league_batting_stats.batting_stats_range(start_dt=start_dt, end_dt=end_dt)
batting = league_batting_stats.batting_stats_range(start_dt=start_dt, end_dt=end_dt)
batter_name_id = batting[['Name','mlbID']]
#batter_name_id['Name'] = batter_name_id['Name'].str.decode(encoding = 'UTF-8')

@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

csv = convert_df(batting)

st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name= 'MLB_BATTING_STATS_' + start_dt + '_to_'+ end_dt + '.csv',
     mime='text/csv',
 )


values = batter_name_id['Name'].tolist()
options = batter_name_id['mlbID'].tolist()

dic = dict(zip(options, values))

option = st.sidebar.selectbox(
     'Which player would you like to select?',
     options,
     format_func=lambda x: dic[x]
     )

stadium = st.sidebar.selectbox(
     'Which stadium would you like to select? ',
     ('angels','astros','athletics','blue_jays','brewers','cardinals','cubs','diamondbacks',
     'dodgers','generic','giants','indians','mariners','marlins','mets','nationals','orioles','padres',
     'phillies','pirates','rangers','rays','red_sox','reds','rockies','royals','tigers','twins','white_sox','yankees')
     )

st.write('You selected:', dic[option] + ' MLB ID: ' + str(option))

st.dataframe(batting[batting['mlbID'] == option])  # Same as st.write(df)
    
data = statcast_batter(start_dt, end_dt, int(option))

player_batting = convert_df(data)
st.download_button(
     label="Download STATCAST DATA as CSV",
     data=player_batting,
     file_name= 'PLAYER_STATCAST_BATTING_'+ start_dt + '_to_'+ end_dt + '.csv',
     mime='text/csv',
 )

sprayplot = spraychart(data, stadium, title=dic[option]+ ': '+start_dt + ' to '+ end_dt)
st.write('You selected:',  stadium.capitalize() + ' home field')
st.pyplot(sprayplot.figure)


