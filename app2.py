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
    st.title('APP1')
    st.write('Welcome to app1')

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
