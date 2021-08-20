import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly as py
import plotly.graph_objs as go
from plotly.offline import plot
import random

def app():
    st.title('APP2')
    st.write('Welcome to app2')

st.set_page_config(
    # Can be "centered" or "wide". In the future also "dashboard", etc.
    layout="wide",
    initial_sidebar_state="expanded",  # Can be "auto", "expanded", "collapsed"
    # String or None. Strings get appended with "• Streamlit".
    page_title="SHAPING_AI",
    page_icon=None,  # String, anything supported by st.image, or None.
)

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

#------------------------Module 1--------------------------

DATA1 = ('dist_month.csv')
DATE_COLUMN1 = 'date'
df1 = pd.read_csv(DATA1, parse_dates=[DATE_COLUMN1])

def draw_dist():
    fig = px.histogram(df1, x='date', y='count', template='plotly_white', range_x=['2011','2020'],width = 700, height = 400)
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='Articles Count')
    fig.update_traces(xbins_size="M1")
    return fig

st.title('Articles distribution over time')
st.plotly_chart(draw_dist())

dist_media_df = pd.read_csv('dist_media50.csv')

def draw_media(data):
    fig = px.histogram(data, x='count', y='index', template='plotly_white', width = 700, height = 500)
    fig.update_xaxes(title_text='Number of articles published from 2011 to 2021')
    fig.update_yaxes(title_text='Media')
    fig.update_traces(xbins_size="M1")
    return fig

st.title('Main Media actors')
st.subheader("Number of results")
num = st.slider("",5,20)
data= dist_media_df[:num]
st.plotly_chart(draw_media(data))

