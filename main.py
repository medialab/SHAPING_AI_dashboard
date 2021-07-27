import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px

st.title("SHAPING AI MEDIA DASHBOARD")
st.write("""This dashboard will present the exploratory analysis of the Freanch media discourse aroud AI from 2011 to 2021.""")

#Titles and Mode selections
st.sidebar.title("About")
st.sidebar.info(
    """
    This app is Open Source dashboard.
    """
)
st.sidebar.info("Feel free to collaborate and comment on the work. The github link can be found "
                "[here](https://github.com/yuliianikolaenko/SHAPING_AI_dashboard).")


df1 = pd.read_csv('dist_month.csv')

fig = px.histogram(df1, x='date_month', template='plotly_white', title='Complaint counts by date')
fig.update_xaxes(categoryorder='category descending', title='Date').update_yaxes(title='Number of complaints')
fig.show()

#------------------------Module 1--------------------------
#HtmlFile = open("lda.html", 'r', encoding='utf-8')
#source_code = HtmlFile.read()
#print(source_code)
#components.html(source_code, height = 1000, width = 2000)

#------------------------Module 2--------------------------
DATA = ('topics.csv')
DATE_COLUMN = 'date_year'
df2 = pd.read_csv(DATA, parse_dates=[DATE_COLUMN])


#------------------------Module 3--------------------------
st.title("Top words discussed in each topic")
st.subheader('Choose Year')

option_1_s = st.selectbox('',[2011,2012,2013,2014,2015,2016,2017,2018,2019,2020])

st.subheader('Choose Topic')

option_2_s = st.selectbox('',['Topic 1','Topic 2','Topic 3','Topic 4','Topic 5','Topic 6','Topic 7','Topic 8','Topic 9','Topic 10'])

st.subheader("Number of results")
num = st.slider("",5,20)

st.subheader('Topic proportion over time')
st.write('Click on the topics to compare:')
def draw_map_topics():
    fig = px.area(df, x="date_year", y="count", color="Topic", line_group="Topic", hover_name="Topic", width = 1200, height = 500, groupnorm='fraction')
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='Topic Count')
    return fig
st.plotly_chart(draw_map_topics())

