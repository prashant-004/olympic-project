import  streamlit as st
import  pandas as pd

import data
import  matplotlib.pyplot as plt
import  seaborn as sns
import  plotly.express as px
import plotly.figure_factory as ff



athlete = pd.read_csv('athlete_events.csv')
noc = pd.read_csv('noc_regions.csv')

df = data.preprocess()
medal_tally = data.medal()

st.sidebar.header('Olympics Analysis')
menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)


if menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = data.country_year_list()

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal = data.fetch_medal_tally(selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal)

if menu == 'Overall Analysis':

    st.header('Top Statistics')
    year = df['Year'].nunique()
    event = df['Event'].nunique()
    sport = df['Sport'].nunique()
    country = df['region'].nunique()
    participant = df['Name'].nunique()
    city = df['City'].nunique()

    col1,col2,col3 = st.columns(3)
    col4,col5,col6 = st.columns(3)

    col1.metric("Year", year, border=True)
    col2.metric("Nations" ,country, border=True)
    col3.metric("Hosts", city, border=True)

    col4.metric("Sport", sport, border=True)
    col5.metric("Event", event, border=True)
    col6.metric("Athlete", participant, border=True)


    nation_over_year = data.data_over_year('region')
    st.title('Participating Nation over the year')
    st.line_chart(nation_over_year, x='Year', y="count")

    event_over_year = data.data_over_year('Event')
    st.title('Events over the year')
    st.line_chart(event_over_year, x='Year', y="count")

    athlete_over_year = data.data_over_year('Name')
    st.title('Athlete over the year')
    st.line_chart(athlete_over_year, x='Year', y="count")

    st.title('no of event over time')
    fig , ax =plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'region', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0), annot=True)
    st.pyplot(fig)

    sport = data.sport_name()
    sport_name = st.sidebar.selectbox('Select a Sport',sport)
    st.title('Top Most successful Athlete in the history of ' + sport_name)
    successful_athlete = data.most_successful(sport_name)
    st.table(successful_athlete)

    st.dataframe(df)

if menu == 'Country-wise Analysis':

    st.sidebar.header('country wise Medal list')
    country = data.country_list()
    selected_country = st.sidebar.selectbox('Select Country',country)
    medal_list = data.country_wise_medal(selected_country)
    st.title('Medal Tally of ' + selected_country + ' overs the year')
    st.line_chart(medal_list, x='Year', y="Medal")

    st.title('Medal Tally of ' + selected_country + ' overs the year')

    fig , ax =plt.subplots(figsize=(20, 20))
    pt = data.best_sport(selected_country)
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)


    st.title('Top 10 Athlete of ' + selected_country + ' overs the year')
    top_10_athlete = data.athlete_stats(selected_country)
    st.table(top_10_athlete)

if menu == 'Athlete wise Analysis':

    st.title('Age wise Analysis of an athlete')
    x1,x2,x3,x4= data.age_plot()
    fig = ff.create_distplot([x1,x2,x3,x4],['overall','Gold','Silver','Bronze'],show_hist=False,show_rug=False)
    st.title('Distribution of the Age')
    st.plotly_chart(fig)
    
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    x,name = data.age_distribution(df)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
    
    st.title("Men Vs Women Participation Over the Years")
    final = data.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    st.title('Height Vs Weight')
    sport = data.sport_name()
    sport_name = st.sidebar.selectbox('Select a Sport', sport)
    temp_df = data.height_weight(df, sport_name)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(data=temp_df, x='Height', y='Weight', hue='Medal', s=60, style='Sex')
    st.pyplot(fig)