import streamlit as st
import pandas as pd
import numpy as np
from gensim.corpora import Dictionary
from gensim.models import LdaModel
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
from io import BytesIO
import base64
import ast


# Load your data
def load_data():
    return pd.read_csv('data/topic_data.csv')


roberta_df = load_data()

venue_names = ['Lost Weekend', 'Gans Woanders', 'Milla', 'SODA', 'Fox Bar', 'Cadu, Cafe an der Uni']

threshold = 0.5
conditions = [
    (roberta_df['positive'] > threshold),
    (roberta_df['negative'] > threshold)
]
choices = ['positive', 'negative']
roberta_df['ovr_sentiment'] = np.select(conditions, choices, default='negative')


# My LDA functions
@st.cache_data
def run_lda_for_sentiment_overall(df, sentiment_description):
    df['trigrams_lemmatized'] = df['trigrams_lemmatized'].apply(
        lambda x: eval(x) if isinstance(x, str) else x)
    dictionary = Dictionary(df['trigrams_lemmatized'].tolist())
    corpus = [dictionary.doc2bow(text) for text in df['trigrams_lemmatized']]

    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, random_state=42,
                         update_every=1, chunksize=100, passes=30, alpha='auto', per_word_topics=True)

    vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
    return vis_data


@st.cache_data
def run_lda_for_sentiment(df, sentiment_description):
    df['trigrams_lemmatized'] = df['trigrams_lemmatized'].apply(
        lambda x: eval(x) if isinstance(x, str) else x)
    dictionary = Dictionary(df['trigrams_lemmatized'].tolist())
    corpus = [dictionary.doc2bow(text) for text in df['trigrams_lemmatized']]

    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, random_state=42,
                         update_every=1, chunksize=100, passes=30, alpha='auto', per_word_topics=True)
    vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
    return vis_data


# Main Streamlit app
def main():
    st.set_page_config(layout="wide")

    st.title("Topic Modelling with LDA ('Latent Dirichlet Allocation') model")

    st.write("LDA (Latent Dirichlet Allocation) is a machine learning technique to discover hidden topics in large"
             " sets of text. Each document contains a mix of topics, and each topic is a mix of words. LDA allocates "
             "words to topics based on probabilities."
             " It's like determining the main subjects of many conversations without knowing them beforehand.")

    st.write(""" Having analyzed the general sentiment and the prevalent words associated with Lost Weekend and its competitors,
    we can delve deeper into the specific themes or topics that dominate these sentiments. By employing topic modeling,
    we'll gain insights into the specific subjects that drive positive or negative reviews. Again we will look at the
    overall topics and by venue topics""")

    st.title("LDA Analysis for Reviews")

    analysis_type = st.radio("Choose Analysis Type:", ("Overall", "By Venue"))

    if analysis_type == "Overall":
        sentiment = st.radio("Choose Sentiment:", ("Positive", "Negative"))
        if sentiment == "Positive":
            vis_data = run_lda_for_sentiment_overall(roberta_df[roberta_df['ovr_sentiment'] == 'positive'],
                                                     "Positive Overall")
        elif sentiment == "Negative":
            vis_data = run_lda_for_sentiment_overall(roberta_df[roberta_df['ovr_sentiment'] == 'negative'],
                                                     "Negative Overall")
    elif analysis_type == "By Venue":
        venue = st.selectbox("Choose a Venue:", venue_names)
        venue_reviews = roberta_df[roberta_df['name'] == venue]
        sentiment = st.radio("Choose Sentiment:", ("Positive", "Negative"))
        if sentiment == "Positive" and not venue_reviews.empty:
            vis_data = run_lda_for_sentiment(venue_reviews, "Positive")
        elif sentiment == "Negative" and not venue_reviews.empty:
            vis_data = run_lda_for_sentiment(venue_reviews, "Negative")
        else:
            st.write(f"No {sentiment.lower()} reviews found for {venue}.")
            return

    html_string = pyLDAvis.prepared_data_to_html(vis_data)
    b64 = base64.b64encode(html_string.encode('utf-8')).decode('utf-8')
    st.markdown(f'<iframe src="data:text/html;base64,{b64}" width="100%" height="800"></iframe>',
                unsafe_allow_html=True)


if __name__ == "__main__":
    main()


