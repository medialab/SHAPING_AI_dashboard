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

## SIDEBAR ##
image = Image.open('images/logo_medialab.png')
st.sidebar.image(image)
st.sidebar.title('Navigate')
choice = st.sidebar.radio("",('Home', 'Articles', 'Words usage', 'Media', 'Topics', 'Terms Network'))
st.sidebar.title("About")
st.sidebar.info(
    """
    This app is Open Source dashboard.
    """
)
st.sidebar.info("Feel free to collaborate and comment on the work. The github link can be found "
                "[here](https://github.com/yuliianikolaenko/SHAPING_AI_dashboard).")

## MODULE ARTICLES ##
dist_articles_df = pd.read_csv('data/dist_articles.csv', parse_dates=['date'])
def draw_dist():
    fig = px.histogram(dist_articles_df, x='date', y='count', template='plotly_white', range_x=['2011','2021'],width = 800, height = 500)
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='Articles Count')
    fig.update_traces(xbins_size="M1")
    return fig

## MODULE BIGRAMS ##
dist_bigram_df = pd.read_csv('data/dist_bigram.csv')
def draw_bigram(data):
    fig = px.bar(data, x='count', y='bigram', title='Counts of top bigrams', template='plotly_white',width = 800, height = 500)
    fig.update_xaxes(title_text='Words count')
    fig.update_yaxes(title_text='Bigram')
    return fig

## MODULE MEDIA ##
dist_media_df = pd.read_csv('data/dist_media.csv')
def draw_media(data):
    fig = px.histogram(data, x='count', y='index', template='plotly_white', width = 700, height = 500)
    fig.update_xaxes(title_text='Number of articles published from 2011 to 2021')
    fig.update_yaxes(title_text='Media')
    fig.update_traces(xbins_size="M1")
    return fig

## MODULE TOPICS ##
@st.cache
lda_model = joblib.load('lda/lda_model.jl')
vocab = joblib.load('lda/vocab.jl')
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


def draw_topics(index, num):
    comp = lda_model.components_[index]
    vocab_comp = zip(vocab, comp)
    sorted_words = sorted(vocab_comp, key=lambda x: x[1], reverse=True)[:num]
    df = pd.DataFrame(sorted_words, columns=['words', 'weight'])
    fig1 = px.histogram(df, x='weight', y='words', template='plotly_white', width = 700, height = 500)
    fig1.update_xaxes(title_text='Term frequency')
    fig1.update_yaxes(title_text='Topic Keywords')
    return fig1

## MODULE CHOICE ##
if choice == 'Home':
    st.title("SHAPING AI MEDIA DASHBOARD")
    st.info("""The international project 'Shaping 21st Century AI. Controversies and Closure in Media, Policy, and Research' investigates the development of Artificial Intelligence (AI) as a socio-technical phenomenon. The project’s task aims at detecting criticism and promises around AI in the French media. """)
    st.info('This dashboard will present the exploratory analysis of the Freanch media discourse aroud AI from 2011 to 2021.')
elif choice == 'Articles':
    st.title('Articles distribution over time')
    st.info('The plot represents the distribution of the articles published by all media sources for 10 years period: from January 2011 to December 2020.')
    st.plotly_chart(draw_dist())
elif choice == 'Words usage':
    st.title('Most frequent words')
    st.info('Choose the number of bigrams you would like to display.')
    st.subheader("Number of results")
    num = st.slider("", 5, 20)
    data = dist_bigram_df[:num]
    st.plotly_chart(draw_bigram(data))
elif choice == 'Media':
    st.title('Main Media actors')
    st.info('Choose the number of media sources you would like to display.')
    st.subheader("Number of results")
    num = st.slider("", 5, 20)
    data = dist_media_df[:num]
    st.plotly_chart(draw_media(data))
elif choice == 'Topics':
    st.title("Top words discussed in each topic")
    st.info(
        'Topics were extracted from the text corpus using the Latent Dirichlet Allocation (LDA) model with Scikit-learn open-source Python machine learning library. The number of topics was selected manually through the comparison and selection of the highest Topic Coherence score.')
    st.subheader('Choose Topic')
    option_2_s = st.selectbox('Topic', ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    st.subheader("Number of results")
    option_3_s = st.slider("", 5, 50)
    st.subheader('Topic keywords')
    if option_2_s == '1':
        #st.pyplot(draw_word_cloud(0, option_3_s))
        st.plotly_chart(draw_topics(0, option_3_s))
    elif option_2_s == '2':
        #st.pyplot(draw_word_cloud(1, option_3_s))
        st.plotly_chart(draw_topics(1, option_3_s))
    elif option_2_s == '3':
        #st.pyplot(draw_word_cloud(2, option_3_s))
        st.plotly_chart(draw_topics(2, option_3_s))
    elif option_2_s == '4':
        #st.pyplot(draw_word_cloud(3, option_3_s))
        st.plotly_chart(draw_topics(3, option_3_s))
    elif option_2_s == '5':
        #st.pyplot(draw_word_cloud(4, option_3_s))
        st.plotly_chart(draw_topics(4, option_3_s))
    elif option_2_s == '6':
        #st.pyplot(draw_word_cloud(5, option_3_s))
        st.plotly_chart(draw_topics(5, option_3_s))
    elif option_2_s == '7':
        #st.pyplot(draw_word_cloud(6, option_3_s))
        st.plotly_chart(draw_topics(6, option_3_s))
    elif option_2_s == '8':
        #st.pyplot(draw_word_cloud(7, option_3_s))
        st.plotly_chart(draw_topics(7, option_3_s))
    elif option_2_s == '9':
        #st.pyplot(draw_word_cloud(8, option_3_s))
        st.plotly_chart(draw_topics(8, option_3_s))
    elif option_2_s == '10':
        #st.pyplot(draw_word_cloud(9, option_3_s))
        st.plotly_chart(draw_topics(9, option_3_s))
elif choice == 'Terms Network':
    st.title("Terms Network")
    st.info(
        """The network represents the links (co-occurrence in the text) between the terms extracted from all corpora. The node's colors are allocated by the Louvain Method of community detection.""")
    components.iframe(
        'https://medialab.github.io/minivan/#/embeded-network?bundle=https:%2F%2Fraw.githubusercontent.com%2Fyuliianikolaenko%2Fshaping-ai-dashboard%2Fmain%2Fnetwork%2FBUNDLE%2520-%2520Shaping%2520AI%2520Network.json&color=cluster_label&lockNavigation=true&name=&ratio=1.3436928&showLink=true&size=weight&x=0.5308020842190102&y=0.3783239544591892',
        width=800, height=500)
