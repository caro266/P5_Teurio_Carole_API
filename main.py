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
        
        page = st.sidebar.selectbox("Select a page", ['Homepage', 'Exploration', 'Prediction'])

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

            st.text("Exemple 1 :\n Titre: Git push existing repo to a new and different remote repo server? \n Body: <p>Say I have a repository and I want to clone this into my account at github to have my own playground aside from the more \"official\" repo on fedorahosted. What would be the steps to initially copy that over? Within github there is this nice \"fork\" button, but I can't use this for obvious reasons.</p> <p>And how would I track changes in the fedorahosted repo into the github one? </p>.")
            st.text("Exemple 2 :\n Titre: How to convert int to string in java?\n Body: I'd like to convert integer into string on java")
            st.text("Exemple 3 :\n Titre: Performing a Stress Test on Web Application?\n Body: <p>In the past, I used Microsoft Web Application Stress Tool and Pylot to stress test web applications. I'd written a simple home page, login script, and site walkthrough (in an ecommerce site adding a few items to a cart and checkout).</p>  <p>Just hitting the homepage hard with a handful of developers would almost always locate a major problem. More scalability problems would surface at the second stage, and even more - after the launch.</p>  <p>The URL of the tools I used were Microsoft Homer (aka <a href=\"http://www.microsoft.com/downloads/details.aspx?familyid=e2c0585a-062a-439e-a67d-75a89aa36495&amp;displaylang=en\" rel=\"noreferrer\">Microsoft Web Application Stress Tool</a>) and <a href=\"https://code.google.com/archive/p/pylt/\" rel=\"noreferrer\">Pylot</a>.</p>  <p>The reports generated by these tools never made much sense to me, and I would spend many hours trying to figure out what kind of concurrent load the site would be able to support. It was always worth it because the stupidest bugs and bottlenecks would always come up (for instance, web server misconfigurations).</p>  <p>What have you done, what tools have you used, and what success have you had with your approach? The part that is most interesting to me is coming up with some kind of a meaningful formula for calculating the number of concurrent users an app can support from the numbers reported by the stress test application.</p>")
	    
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
    except Exception as err:
        st.write("ERROR Exception : ",err)
        
if __name__ == '__main__':
    main()
          
