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
from multiapp import MultiApp
def foo():
    st.title("Hello Foo")
def bar():
    st.title("Hello Bar")

app = MultiApp()
app.add_app("Foo", foo)
app.add_app("Bar", bar)
app.run()

PAGES = {
    "Topics": app2,
    "Networks": app3
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()

