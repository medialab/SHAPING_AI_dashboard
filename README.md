# SHAPING_AI_dashboard 📈
This Streamlit app is [deployed on Streamlit Sharing](https://share.streamlit.io/). You can also click on this [link](https://share.streamlit.io/yuliianikolaenko/shaping-ai-dashboard/main/main.py) to visualize the dashboard.

This dashboard will present the exploratory analysis of the Freanch media discourse aroud AI from 2011 to 2021.

 ## Set Up 
 
Create a python virtual environnemnt and install the requirement.txt package using pip :

```
pip install -r requirements.txt
```

## Text preprocessing
<code>data_wrangling.ipynb</code>: Python code with data preprocessing, features engineering, text cleaning and visualisations


## Data 
<code>dist_articles.csv</code>: distribution of the articles over 10 years period

<code>dist_media</code>: distribution of the media and published articles

<code>dist_bigram</code>: distribution of the bigrams count

<code>dist_topic.csv</code>: distribution of the topics over time

## Topic Modeling

<code>lda_model.jl</code>: LDA model

<code>vocab.jl</code>: corpus vocabulary 


## Launching the App

Run the following line in the terminal, it will launch the Dashboard locally in the default browser.

```
streamlit run main.py
```

