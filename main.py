##################################### IMPORT #####################################################################
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
from PIL import Image
import joblib
##################################### PAGE CONFIGURATION AND TITLE #################################################
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="SHAPING AI",
    page_icon=None,
)
################################################### SIDEBAR ###################################################
image = Image.open('images/logo_medialab.png')
st.sidebar.image(image)
st.sidebar.title('Navigate')
choice = st.sidebar.radio("",('Home', 'Data', 'Analysis', 'Topics', 'Terms Network'))
st.sidebar.title("About this app")
st.sidebar.info("This dashboard presents the exploratory analysis of the French media discourse around AI from 2011 to 2021. Feel free to collaborate and comment on the work. The Github link can be found "
                "[here](https://github.com/yuliianikolaenko/shaping-ai-dashboard).")
################################################### DATA ###################################################
dist_articles_df = pd.read_csv('data/dist_articles.csv', parse_dates=['date'])
#dist_bigram_df = pd.read_csv('data/dist_bigram.csv')
lda_model = joblib.load('lda/lda_model.jl')
vocab = joblib.load('lda/vocab.jl')
topics_data = pd.read_csv('data/dist_topic.csv')
################################################### FUNCTIONS ###################################################
def draw_dist(data):
    fig = px.histogram(data, x='date', y='count', template='plotly_white', width = 800, height = 500)
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='Articles Count')
    fig.update_traces(xbins_size="M1")
    return fig

def draw_bigram(data):
    fig = px.bar(data, x='count', y='bigram', orientation='h', width = 500, height = 400)
    fig.update_yaxes(title_text='')
    fig.update_xaxes(title_text='Count')
    fig.update_yaxes(autorange="reversed")
    return fig

def load_bigram(min, max):
    df_bigram = pd.read_csv('data/df_bigrams.csv', parse_dates=['year'])
    df_bigram = df_bigram[(df_bigram["year"] >= min) & (df_bigram["year"] <= max)]
    data = df_bigram.sort_values(["count"], ascending=False)
    return data

def load_media(min, max):
    df_journals = pd.read_csv('data/df_journals.csv', parse_dates=['date'])
    df_journals = df_journals[(df_journals["date"] >= min) & (df_journals["date"] <= max)]
    data = df_journals['journal_clean'].value_counts().to_frame('count').reset_index().rename(columns={'index': 'media'})
    data = data[:20]
    return data

def draw_media(data):
    fig = px.histogram(data, x='count', y='media', orientation='h', width = 500, height = 400)
    fig.update_xaxes(title_text='Count of articles published')
    fig.update_yaxes(title_text='')
    fig.update_yaxes(autorange="reversed")
    fig.update_traces(xbins_size="M1")
    return fig

def draw_topics(index):
    comp = lda_model.components_[index]
    vocab_comp = zip(vocab, comp)
    sorted_words = sorted(vocab_comp, key=lambda x: x[1], reverse=True)[:15]
    df = pd.DataFrame(sorted_words, columns=['words', 'weight'])
    fig = px.histogram(df, x='weight', y='words', template='plotly_white', width = 500, height = 400)
    fig.update_xaxes(title_text='Term frequency')
    fig.update_yaxes(title_text='Topic Keywords')
    fig.update_yaxes(autorange="reversed")
    return fig

def draw_dist_topic(data):
    fig = px.line(data, x="year", y="norm", color='topic', range_x=['2010', '2021'], width = 500, height = 400)
    fig.update_traces(mode='markers+lines')
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='Topic count (normalized)')
    fig.update_layout(showlegend=False)
    return fig
################################################### MODULE CHOICE ###################################################
if choice == 'Home':
    st.title("SHAPING AI MEDIA DASHBOARD")
    st.info("""The international project 'Shaping 21st Century AI. Controversies and Closure in Media, Policy, and Research' investigate the development of Artificial Intelligence (AI) as a socio-technical phenomenon. The project’s task aims at detecting criticism and promises around AI in the French media. """)
elif choice == 'Data':
    st.title("Data")
    st.markdown('### Europresse Database')
    st.markdown('Corpus was extracted using search by keywords in the title and lead paragraph of articles. National and regional French media publishing in French language. The time period of 10 years from 1 January 2011 to 1 January 2021. Metadata included such variables as _content_ (text of the article), _author_ (name of the author), _title_ (title of the article), _journal_ (name of the media), _date_ (date of the article publishing).')
    st.info(' Search queries'
            ': "*intelligence artificielle*" OR "*IA*" OR "*algorithme*" OR "*apprentissage profond*" OR "*apprentissage machine*" OR "*réseau de neurone*" OR "*machine learning*" OR "*deep learning*" OR "*neural network*"')
    st.markdown('### Text Corpus')
    st.markdown('Data wrangling included removal of missing values, duplicates, text pre-processing: unicode, lower casing, links, special characters, punctuation, stopwords removal. The total number of articles in the final corpus is 47572.')
elif choice == 'Analysis':
    st.title('Analysis')
    st.info('Analysis')
    st.subheader('Choose the time period you want to analyse:')
    min_ts = min(dist_articles_df['date']).to_pydatetime()
    max_ts = max(dist_articles_df['date']).to_pydatetime()
    min_selection, max_selection = pd.to_datetime(st.slider("", min_value=min_ts, max_value=max_ts, value=[min_ts, max_ts]))
    dist_articles_df = dist_articles_df[(dist_articles_df["date"] >= min_selection) & (dist_articles_df["date"] <= max_selection)]
    my_expander = st.expander()
    my_expander.write('Hello there!')
    clicked = my_expander.button('Click me!')
    my_expander.subheader('Articles distribution over time')
    my_expander.plotly_chart(draw_dist(dist_articles_df))
    col1, col2 = st.columns(2)
    col1.subheader('Most frequent words')
    data = load_bigram(min_selection, max_selection)
    data = data[:20]
    col1.plotly_chart(draw_bigram(data))
    col2.subheader('Main Media actors')
    data = load_media(min_selection, max_selection)
    col2.plotly_chart(draw_media(data))
elif choice == 'Topics':
    st.title("Topic Modeling")
    st.info('Topics were extracted from the text corpus using the Latent Dirichlet Allocation (LDA) model with Scikit-learn open-source Python machine learning library. The number of topics was selected manually through the comparison and selection of the highest Topic Coherence score.')
    st.subheader('Choose the topic you want to analyse:')
    option_2_s = st.selectbox('', ['History', 'Investments', 'Healthcare', 'Robotics', 'Companies', 'Market&Clients', 'Research', 'Education', 'Enterprises', 'Legality'])
    col1, col2 = st.columns(2)
    col1.subheader('Topic keywords')
    if option_2_s == 'History':
        col1.plotly_chart(draw_topics(0))
    elif option_2_s == 'Investments':
        col1.plotly_chart(draw_topics(1))
    elif option_2_s == 'Healthcare':
        col1.plotly_chart(draw_topics(2))
    elif option_2_s == 'Robotics':
        col1.plotly_chart(draw_topics(3))
    elif option_2_s == 'Companies':
        col1.plotly_chart(draw_topics(4))
    elif option_2_s == 'Market&Clients':
         col1.plotly_chart(draw_topics(5))
    elif option_2_s == 'Research':
         col1.plotly_chart(draw_topics(6))
    elif option_2_s == 'Education':
         col1.plotly_chart(draw_topics(7))
    elif option_2_s == 'Enterprises':
         col1.plotly_chart(draw_topics(8))
    elif option_2_s == 'Legality':
         col1.plotly_chart(draw_topics(9))
    col2.subheader('Topic distribution over time')
    if option_2_s == 'History':
        topics = topics_data[topics_data['topic'] == 0]
        col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == 'Investments':
        topics = topics_data[topics_data['topic'] == 1]
        col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == 'Healthcare':
        topics = topics_data[topics_data['topic'] == 2]
        col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == 'Robotics':
        topics = topics_data[topics_data['topic'] == 3]
        col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == 'Companies':
        topics = topics_data[topics_data['topic'] == 4]
        col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == 'Market&Clients':
         topics = topics_data[topics_data['topic'] == 5]
         col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == 'Research':
         topics = topics_data[topics_data['topic'] == 6]
         col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == 'Education':
         topics = topics_data[topics_data['topic'] == 7]
         col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == 'Enterprises':
         topics = topics_data[topics_data['topic'] == 8]
         col2.plotly_chart(draw_dist_topic(topics))
    elif option_2_s == 'Legality':
         topics = topics_data[topics_data['topic'] == 9]
         col2.plotly_chart(draw_dist_topic(topics))
elif choice == 'Terms Network':
    st.title("Terms Network")
    st.info(
        """The network represents the links (co-occurrence in the text) between the terms extracted from all corpora. The node's colors are allocated by the Louvain Method of community detection.""")
    components.iframe(
        'https://medialab.github.io/minivan/#/embeded-network?bundle=https:%2F%2Fraw.githubusercontent.com%2Fyuliianikolaenko%2Fshaping-ai-dashboard%2Fmain%2Fnetwork%2FSHAPING-AI-NETWORK-BUNDLE.json&color=cluster_label&lockNavigation=true&name=&ratio=1.3436928&showLink=true&size=weight&x=0.5308020842190102&y=0.3783239544591892',
        width=800, height=500)
