import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
import joblib


##################################### PAGE CONFIGURATION AND TITLE #################################################
st.set_page_config(
    # Can be "centered" or "wide". In the future also "dashboard", etc.
    layout="wide",
    initial_sidebar_state="expanded",  # Can be "auto", "expanded", "collapsed"
    # String or None. Strings get appended with "• Streamlit".
    page_title="SHAPING_AI",
    page_icon=None,  # String, anything supported by st.image, or None.
)

################################################### SIDEBAR ###################################################
image = Image.open('images/logo_medialab.png')
st.sidebar.image(image)
st.sidebar.title('Navigate')
choice = st.sidebar.radio("",('Home', 'Articles', 'Analysis', 'Topics', 'Terms Network'))
st.sidebar.title("About")
st.sidebar.info(
    """
    This app is Open Source dashboard.
    """
)
st.sidebar.info("Feel free to collaborate and comment on the work. The github link can be found "
                "[here](https://github.com/yuliianikolaenko/SHAPING_AI_dashboard).")

################################################### MODULE ARTICLES ###################################################
dist_articles_df = pd.read_csv('data/dist_articles.csv', parse_dates=['date'])
def draw_dist():
    fig = px.histogram(dist_articles_df, x='date', y='count', template='plotly_white', range_x=['2011','2021'],width = 800, height = 500)
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='Articles Count')
    fig.update_traces(xbins_size="M1")
    return fig

################################################### MODULE BIGRAMS ###################################################
dist_bigram_df = pd.read_csv('data/dist_bigram.csv')
def draw_bigram(data):
    fig = px.bar(data, x='count', y='bigram', orientation='h', width = 500, height = 400)
    fig.update_yaxes(title_text='')
    fig.update_xaxes(title_text='Count')
    fig.update_yaxes(autorange="reversed")
    return fig

################################################### MODULE MEDIA ###################################################
dist_media_df = pd.read_csv('data/dist_media.csv')
def draw_media(data):
    fig = px.histogram(data, x='count', y='index', orientation='h', width = 500, height = 400)
    fig.update_xaxes(title_text='Count of articles published')
    fig.update_yaxes(title_text='')
    fig.update_yaxes(autorange="reversed")
    fig.update_traces(xbins_size="M1")
    return fig

################################################### MODULE TOPICS ###################################################
lda_model = joblib.load('lda/lda_model.jl')
vocab = joblib.load('lda/vocab.jl')
topics_data = pd.read_csv('data/dist_topic.csv')

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
    fig = px.histogram(df, x='weight', y='words', template='plotly_white', width = 500, height = 400)
    fig.update_xaxes(title_text='Term frequency')
    fig.update_yaxes(title_text='Topic Keywords')
    fig.update_yaxes(autorange="reversed")
    return fig

def draw_dist_topic(data):
    fig = px.line(data, x="year", y="norm", color='topic', range_x=['2011', '2020'], width = 500, height = 400)
    fig.update_traces(mode='markers+lines')
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='Topic count (normalized)')
    fig.update_layout(showlegend=False)
    return fig

################################################### MODULE CHOICE ###################################################
if choice == 'Home':
    st.title("SHAPING AI MEDIA DASHBOARD")
    st.info("""The international project 'Shaping 21st Century AI. Controversies and Closure in Media, Policy, and Research' investigates the development of Artificial Intelligence (AI) as a socio-technical phenomenon. The project’s task aims at detecting criticism and promises around AI in the French media. """)
    st.info('This dashboard will present the exploratory analysis of the Freanch media discourse aroud AI from 2011 to 2021.')
elif choice == 'Articles':
    st.title('Data')
    col1, col2 = st.columns(2)
    col1.markdown('### Europresse Database')
    col1.markdown('Corpus was extracted using search by keywords in title and lead paragraph of articles. National and regional French media publishing in French language. Time period of 10 years from 1 January 2011 to 1 January 2021. Metadata included such variables as _content_ (text of the article), _author_ (name of the author), _title_ (title of the article), _journal_ (name of the media), _date_ (date of the article publishing).')
    col1.info(' Search queries'
            ': "*intelligence artificielle*" OR "*IA*" OR "*algorithme*" OR "*apprentissage profond*" OR "*apprentissage machine*" OR "*réseau de neurone*" OR "*machine learning*" OR "*deep learning*" OR "*neural network*"')
    col2.markdown('### Text Corpus')
    col2.markdown('Data wrangling included removal of missing values, dublicates, text pre-processing: unicode, lower casing, links, special characters, punctuation, stopwords removal. Total number of articles in the final corpus is 48411'
                '.')
    st.title('Articles distribution over time')
    st.info('The plot represents the distribution of the articles published by all media sources for 10 years period: from January 2011 to December 2020.')
    st.plotly_chart(draw_dist())
elif choice == 'Analysis':
    st.title('Analysis')
    st.info('Choose the year you want to analyse.')
    year = st.selectbox('Year', ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'])
    col1, col2 = st.columns(2)
    st.info('Choose the number of results you would like to display.')
    num = st.slider("", 5, 20)
    col1.subheader('Most frequent words')
    data = dist_bigram_df[:num]
    col1.plotly_chart(draw_bigram(data))
    col2.subheader('Main Media actors')
    data = dist_media_df[:num]
    col2.plotly_chart(draw_media(data))
elif choice == 'Topics':
    st.title("Topic Modeling")
    st.info('Topics were extracted from the text corpus using the Latent Dirichlet Allocation (LDA) model with Scikit-learn open-source Python machine learning library. The number of topics was selected manually through the comparison and selection of the highest Topic Coherence score.')
    st.title("Top words discussed in each topic")
    st.subheader('Choose Topic')
    option_2_s = st.selectbox('Topic', ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    st.subheader("Number of results")
    option_3_s = st.slider("", 5, 10)
    col1, col2 = st.columns(2)
    col1.subheader('Topic keywords')
    if option_2_s == '1':
        col1.plotly_chart(draw_topics(0, option_3_s))
    elif option_2_s == '2':
        col1.plotly_chart(draw_topics(1, option_3_s))
    elif option_2_s == '3':
        col1.plotly_chart(draw_topics(2, option_3_s))
    elif option_2_s == '4':
        col1.plotly_chart(draw_topics(3, option_3_s))
    elif option_2_s == '5':
        col1.plotly_chart(draw_topics(4, option_3_s))
    elif option_2_s == '6':
         col1.plotly_chart(draw_topics(5, option_3_s))
    elif option_2_s == '7':
         col1.plotly_chart(draw_topics(6, option_3_s))
    elif option_2_s == '8':
         col1.plotly_chart(draw_topics(8, option_3_s))
    elif option_2_s == '9':
         col1.plotly_chart(draw_topics(8, option_3_s))
    elif option_2_s == '10':
         col1.plotly_chart(draw_topics(9, option_3_s))
    col2.subheader('Topic distribution over time')
    if option_2_s == '1':
        topics = topics_data[topics_data['topic'] == 0]
        col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == '2':
        topics = topics_data[topics_data['topic'] == 1]
        col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == '3':
        topics = topics_data[topics_data['topic'] == 2]
        col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == '4':
        topics = topics_data[topics_data['topic'] == 3]
        col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == '5':
        topics = topics_data[topics_data['topic'] == 4]
        col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == '6':
         topics = topics_data[topics_data['topic'] == 5]
         col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == '7':
         topics = topics_data[topics_data['topic'] == 6]
         col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == '8':
         topics = topics_data[topics_data['topic'] == 8]
         col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == '9':
         topics = topics_data[topics_data['topic'] == 8]
         col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == '10':
         topics = topics_data[topics_data['topic'] == 9]
         col2.plotly_chart(draw_dist_topic(topics))
elif choice == 'Terms Network':
    st.title("Terms Network")
    st.info(
        """The network represents the links (co-occurrence in the text) between the terms extracted from all corpora. The node's colors are allocated by the Louvain Method of community detection.""")
    components.iframe(
        'https://medialab.github.io/minivan/#/embeded-network?bundle=https:%2F%2Fraw.githubusercontent.com%2Fyuliianikolaenko%2Fshaping-ai-dashboard%2Fmain%2Fnetwork%2FBUNDLE%2520-%2520Shaping%2520AI%2520Network.json&color=cluster_label&lockNavigation=true&name=&ratio=1.3436928&showLink=true&size=weight&x=0.5308020842190102&y=0.3783239544591892',
        width=800, height=500)
