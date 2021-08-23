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
from PIL import Image

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

image = Image.open('logo_medialab.png')
#Titles and Mode selections
st.sidebar.image(image)
st.sidebar.title("About")
st.sidebar.info(
    """
    This app is Open Source dashboard.
    """
)
st.sidebar.info("Feel free to collaborate and comment on the work. The github link can be found "
                "[here](https://github.com/yuliianikolaenko/SHAPING_AI_dashboard).")
st.sidebar.title("Navigate")
st.sidebar.radio("", ["Articles and media", "Topics", "Network"])

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

#------------------------Module 2--------------------------
DATA2 = ('topics.csv')
DATE_COLUMN2 = 'date_year'
df2 = pd.read_csv(DATA2, parse_dates=[DATE_COLUMN2])
st.title("Top words discussed in each topic")
st.subheader('Choose Year')


def get_text_of_topic(topic):
    data = df2.groupby(['Topic'])['date_year'].apply(lambda x: ' '.join(x)).reset_index()
    txt = temp_data.dialogue[0]
    return txt

def show_word_cloud(data,year,topic):
        txt = get_text_of_topic(topic)
        wc = WordCloud(background_color="white",
                       contour_width=3, contour_color="white")
        wc.generate(txt)
        return wc

def swc(df,v1,v2):
    return show_word_cloud(df,v1,v2)

option_1_s = st.selectbox('',[2011,2012,2013,2014,2015,2016,2017,2018,2019,2020])
st.subheader('Choose Topic')
option_2_s = st.selectbox('',['Topic 1','Topic 2','Topic 3','Topic 4','Topic 5','Topic 6','Topic 7','Topic 8','Topic 9','Topic 10'])
st.subheader("Number of results")
option_3_s = st.slider("",5,50)
st.subheader('Wordcloud')
wc = swc(df2, option_1_s.value, option_2_s.value)
fig = plt.figure(figsize=(8, 8))
plt.imshow(wc, interpolation="bilinear")
plt.axis('off')
plt.title(select_box2.value, fontsize=18)
plt.tight_layout()
st.pyplot(fig)



#------------------------Module 3--------------------------

st.subheader('Topic proportion over time')
st.write('Click on the topics to compare:')
def draw_map_topics():
    fig = px.area(df2, x="date_year", y="count", color="Topic", line_group="Topic", hover_name="Topic",width = 1200, height = 500, groupnorm='fraction')
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='Topic Count')
    return fig
st.plotly_chart(draw_map_topics())

st.set_option('deprecation.showPyplotGlobalUse', False)