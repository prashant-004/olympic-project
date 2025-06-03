import  pandas as pd
import  matplotlib.pyplot as plt
import  seaborn as sns
from fontTools.misc.cython import returns

athlete = pd.read_csv('athlete_events.csv')
noc = pd.read_csv('noc_regions.csv')



def preprocess():
    df = athlete[athlete['Season'] == 'Summer']
    df = df.merge(noc, on='NOC', how='inner')
    df = df.drop(columns='notes')
    df.drop_duplicates(inplace=True)
    df = pd.concat([df, pd.get_dummies(df['Medal'], dtype=int)], axis=1)

    return  df

df = preprocess()

print(df.info())

def medal():
    medal_tally = df.drop_duplicates(subset = ['Team', 'NOC', 'Games','Year', 'Season', 'City','Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values('Gold',ascending= False).reset_index()
    return medal_tally

def country_year_list():
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'overall')
    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'overall')

    return  year,country

def country_list():
    country = df['region'].dropna().unique().tolist()
    country.sort()
    return  country

def fetch_medal_tally(selected_year, selected_country):
    medal_tally = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if selected_year == 'overall' and selected_country == 'overall':
        x = medal_tally

    if selected_year == 'overall' and selected_country != 'overall':
        x = medal_tally[medal_tally['region'] == selected_country]

    if selected_year != 'overall' and selected_country == 'overall':
        flag = 1
        x = medal_tally[medal_tally['Year'] == selected_year]

    if selected_year != 'overall' and selected_country != 'overall':
        x = medal_tally[(medal_tally['region'] == selected_country) & (medal_tally['Year'] == selected_year)]

    if flag == 1:
        x = x.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False).reset_index()

    else:
        x = x.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return  x

def data_over_year(col):
    data_over_year = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    return  data_over_year


def most_successful(sport):

    x = df[(df['Gold'] !=0) | (df['Silver'] !=0) | (df['Bronze'] !=0)]
    if sport != 'overall':
        x = x[x['Sport'] == sport]
    x =x['Name'].value_counts().reset_index().head(15).merge(df,how='left',left_on='Name',right_on='Name')[['Name','Sport','region','count']].drop_duplicates()
    return x

def sport_name():
    x = df[(df['Gold'] !=0) | (df['Silver'] !=0) | (df['Bronze'] !=0)]
    Sport = x['Sport'].unique().tolist()
    Sport.sort()
    Sport.insert(0,'overall')
    return Sport

def medal_stats(country):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    if country != 'overall':
        x = medal_tally.groupby(country)[['Gold','Silver','Bronze']].sum().sort_values('Gold',ascending=False)
    else:
        x = medal_tally.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values('Gold',ascending=False)

    return x

def country_wise_medal(country):
    medal_tally = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.dropna(subset='Medal')
    x = medal_tally[medal_tally['region'] == country].groupby('Year')['Medal'].count().reset_index()
    return x


def best_sport(country):
    medal_tally = df.drop_duplicates(subset = ['Team', 'NOC', 'Games','Year', 'Season', 'City','Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.dropna(subset='Medal')
    medal_tally = medal_tally[medal_tally['region'] == country]
    pt = medal_tally.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc= 'count').fillna(0).astype(int)
    return  pt

def athlete_stats(country):

    x = df[(df['Gold'] !=0) | (df['Silver'] !=0) | (df['Bronze'] !=0)]
    x = x[x['region'] == country]
    x =x['Name'].value_counts().reset_index().head(10).merge(df,how='left',left_on='Name',right_on='Name')[['Name','Sport','count']].drop_duplicates()
    return x

def age_plot():
    x = df.drop_duplicates(subset=['Name', 'region'])
    x1 = x['Age'].dropna()
    x2 = x[x['Medal'] == 'Gold']['Age'].dropna()
    x3 = x[x['Medal'] == 'Bronze']['Age'].dropna()
    x4 = x[x['Medal'] == 'Silver']['Age'].dropna()
    return x1,x2,x3,x4

x = df.drop_duplicates(subset=['Name', 'region'])
x1 = x['Age'].dropna()
x2 = x[x['Medal'] == 'Gold']['Age'].dropna()
x3 = x[x['Medal'] == 'Bronze']['Age'].dropna()
x4 = x[x['Medal'] == 'Silver']['Age'].dropna()

import plotly.figure_factory as ff
fig = ff.create_distplot([x1,x2,x3,x4],['overall','Gold','Silver','Bronze'],show_hist=False,show_rug=False)



def height_weight(df, sport):
    df = df.drop_duplicates(subset=['Name', 'region'])
    df['Medal'].fillna('no medal', inplace=True)
    if sport != 'overall':
        temp_df = df[df['Sport'] == sport]
        return  temp_df
    else:
        return  df
    

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final


def age_distribution(df):
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = df[df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    return x, name
