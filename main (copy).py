# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from flask import Flask
from wordcloud import WordCloud

from urllib.error import URLError

app = Flask(__name__)


def get_UN_data():
    dataSO = pd.read_csv("StackOverflow_cleaned.csv",
                   sep=";")
    dataSO['CreationDate'] = pd.to_datetime(dataSO['CreationDate']).dt.year
    dataSO['CreationDate']= dataSO['CreationDate'].astype(str)
    return dataSO

@app.route("/")
def test():
    st.write("Test")

@app.route("/StackOverflow_question/")
def wordCloudAnnee():
    df = get_UN_data()
    years = st.multiselect("Select a year",list(df['CreationDate'].unique()),'2020')
    
    if not years:
        st.error("Please select at least one year.")
    else:
        data = df[df['CreationDate'].isin(years)]
        st.write("### Title and Body cleaning", data.sort_index())

        dWC = data['Tags'].value_counts().to_dict()
        wc = WordCloud().fit_words(dWC)
        st.image(wc.to_array())
        
@app.route("/StackOverflow_question/")
def stachOver():       
    title = st.text_input('Input your title here: ') 
    body = st.text_input('Input your body here: ') 
        
    if st.button('Propose tags'):
        st.write('Tags')


if __name__ == "__main__":
    app.run()
