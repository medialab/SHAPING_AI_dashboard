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
                "[here](https://github.com/yuliianikolaenko/SHAPINGAI_dashboard).")


HtmlFile = open("lda.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
print(source_code)
components.html(source_code, height = 1000, width = 2000)

DATA = ('topics.csv')
DATE_COLUMN = 'date_year'
df = pd.read_csv(DATA, parse_dates=[DATE_COLUMN])

def draw_map_topics():
    fig = px.line(df, x="date_year", y="count", color="Topic", line_group="Topic", hover_name="Topic",
                  title='Topics distribution over time', width = 1500, height = 800)
    return fig

##### SIDEBAR
#slider to chose date
show_timerange = st.sidebar.checkbox("Show date range")
if show_timerange == True:
    # Calculate the timerange for the slider
    min_ts = min(df[DATE_COLUMN]).to_pydatetime()
    max_ts = max(df[DATE_COLUMN]).to_pydatetime()
    day_date = pd.to_datetime(st.sidebar.slider("Date to chose", min_value=min_ts, max_value=max_ts, value=max_ts))
    st.write(f"Data for {day_date.date()}")
    df = df[(df['date_year'] == day_date)]

st.plotly_chart(draw_map_topics())
