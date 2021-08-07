# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import joblib
import spacy
import en_core_web_sm
import functions as preproc


def get_UN_data():
    try:
        dataSO = pd.read_csv("StackOverflow_cleaned.csv",
                       sep=";")
        dataSO['CreationDate'] = pd.to_datetime(dataSO['CreationDate']).dt.year
        dataSO['CreationDate']= dataSO['CreationDate'].astype(str)
        return dataSO
    except:
        st.write("ERROR Exception get_UN_data")
        return []

def main():
    try:

        df = get_UN_data()
        
        page = st.sidebar.selectbox("Choisir votre page", ['Homepage', 'Exploration', 'Prediction'])

        if page == 'Homepage':
            st.text("Page d'acceuil.")
        elif page == 'Exploration':
            years = st.multiselect("Select a year",list(df['CreationDate'].unique()),'2020')
            if not years:
                st.text("Please select at least one year.")
            else:
                data = df[df['CreationDate'].isin(years)]
                st.write("### Title and Body cleaning", data.sort_index())
            dWC = data['Tags'].value_counts().to_dict()
            wc = WordCloud().fit_words(dWC)
            st.image(wc.to_array())
        else:
            model = joblib.load("logit_nlp_model.pkl", 'r')
            vectorizer = joblib.load("tfidf_vectorizer.pkl", 'r')
            multilabel_binarizer = joblib.load("multilabel_binarizer.pkl", 'r')

            title = st.text_input('Input your title here: ') 
            body = st.text_input('Input your body here: ') 

            if st.button('Propose tags'):
                if(title!="" and body!=""):
                    # Clean the title sent
                    nlp = spacy.load('en_core_web_sm')
                    pos_list = ["NOUN","PROPN"]
                    rawtext = title
                    cleaned_title = preproc.text_cleaner(rawtext, nlp, pos_list, "english")

                    # Clean the body sent
                    nlp = spacy.load('en_core_web_sm')
                    pos_list = ["NOUN","PROPN"]
                    rawtext = body
                    cleaned_body = preproc.text_cleaner(rawtext, nlp, pos_list, "english")

                    clean = cleaned_title+cleaned_body

                    # Apply saved trained TfidfVectorizer
                    X_tfidf = vectorizer.transform([clean])

                    # Perform prediction
                    predict = model.predict(X_tfidf)
                    # Inverse multilabel binarizer
                    tags_predict = multilabel_binarizer.inverse_transform(predict)

                    st.write(tags_predict)
    except:
        st.write("ERROR Exception")
        
if __name__ == '__main__':
    main()
          