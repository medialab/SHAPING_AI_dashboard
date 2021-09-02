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
import sklearn
import joblib


## PAGE CONFIGURATION AND TITLE ##
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

## SIDEBAR ##
image = Image.open('logo_medialab.png')
st.sidebar.image(image)
st.sidebar.title("About")
st.sidebar.info(
    """
    This app is Open Source dashboard.
    """
)
st.sidebar.info("Feel free to collaborate and comment on the work. The github link can be found "
                "[here](https://github.com/yuliianikolaenko/SHAPING_AI_dashboard).")

## MODULE ARTICLES ##
DATA1 = ('dist_articles.csv')
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

## MODULE MEDIA ##
dist_media_df = pd.read_csv('dist_media.csv')
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

## MODULE TOPICS
lda_model = joblib.load('lda_model.jl')
vocab = joblib.load('vocab.jl')
def draw_word_cloud(index, maxwords):
  imp_words_topic=""
  comp=lda_model.components_[index]
  vocab_comp = zip(vocab, comp)
  sorted_words = sorted(vocab_comp, key= lambda x:x[1], reverse=True)[:50]
  for word in sorted_words:
    imp_words_topic=imp_words_topic+" "+word[0]
  wordcloud = WordCloud(width = 1000, height = 500, background_color="white",
                       contour_width=3, contour_color="white", max_words=maxwords).generate(imp_words_topic)
  fig = plt.figure(figsize=(10,10))
  plt.imshow(wordcloud)
  plt.axis("off")
  plt.tight_layout()
  plt.show()
  return fig


st.title("Top words discussed in each topic")
st.subheader('Choose Topic')
option_2_s = st.selectbox('Topic', [0,1,2,3,4,5,6,7,8,9])
st.subheader("Number of results")
option_3_s = st.slider("",5,50)
#st.plotly_chart(draw_topics(option_3_s))
st.subheader('Wordcloud')
fig = draw_word_cloud(option_2_s, option_3_s)
st.pyplot(fig)

## MODULE NETWORK ##
st.title("Terms Network")

components.iframe('https://medialab.github.io/minivan/#/embeded-network?bundle=https:%2F%2Fraw.githubusercontent.com%2Fyuliianikolaenko%2Fshaping-ai-dashboard%2Fmain%2FBUNDLE%2520-%2520Network.json&color=cluster_label&lockNavigation=false&name=&ratio=0.7904075294117647&showLink=true&size=weight&x=0.5596849487946193&y=0.3357065808546196', width=800, height=500)
