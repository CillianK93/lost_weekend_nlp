import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

import ast  # Import the Abstract Syntax Trees module

# Convert the string representation of a list back to an actual list
def str_to_list(s):
    try:
        return ast.literal_eval(s)
    except ValueError:
        return []


roberta_df = pd.read_csv('data/en_de_rsl.csv')


def plot_sentiment_for_venue(df, venue_name):
    # Filter data for the selected venue
    filtered_data = df[df['name'] == venue_name]

    # Grouping and aggregating for the mean.
    results = filtered_data.groupby('name').agg({
        'positive': 'mean',
        'neutral': 'mean',
        'negative': 'mean'
    }).reset_index()

    # Rename the columns for clarity
    results.columns = ['Venue',
                       'Average Positive',
                       'Average Neutral',
                       'Average Negative']

    # Convert the results DataFrame to a "long" format suitable for Seaborn
    long_format = results.melt(id_vars='Venue', value_vars=[
        'Average Positive', 'Average Neutral', 'Average Negative'
    ])

    fig, ax = plt.subplots(figsize=(6, 3))

    # Plot using Seaborn on the given axes
    sns.barplot(data=long_format, x="variable", y="value", ax=ax)  # Note the 'ax' argument
    ax.set_title(f"Average Sentiment Scores for {venue_name}")
    ax.set_ylabel("Average Sentiment Score")
    ax.set_xlabel("Sentiment Type")
    ax.set_ylim(0, 1)  # Assuming sentiment scores are between 0 and 1

    # Show the plot in Streamlit
    st.pyplot(fig)


threshold = 0.6

# Apply the conversion to all reviews
roberta_df['review_text'] = roberta_df['review_text'].apply(str_to_list)

# Separate the reviews based on sentiment score
positive_reviews = roberta_df[roberta_df['positive'] > threshold]['review_text']
neutral_reviews = roberta_df[roberta_df['neutral'] > threshold]['review_text']
negative_reviews = roberta_df[roberta_df['negative'] > threshold]['review_text']

# Join tokens to form single strings and then join all the reviews
positive_text = ' '.join([' '.join(review) for review in positive_reviews])
neutral_text = ' '.join([' '.join(review) for review in neutral_reviews])
negative_text = ' '.join([' '.join(review) for review in negative_reviews])


def generate_venue_wordclouds(df, threshold=0.6):
    # Group by venue
    grouped = df.groupby('name')

    # For storing combined texts for each sentiment for each venue
    venue_positive_texts = {}
    venue_neutral_texts = {}
    venue_negative_texts = {}

    # Loop over each venue group
    for venue_name, group in grouped:
        # Filter reviews based on sentiment thresholds for the current venue group
        positive_reviews = group[group['positive'] > threshold]['review_text']
        neutral_reviews = group[group['neutral'] > threshold]['review_text']
        negative_reviews = group[group['negative'] > threshold]['review_text']

        # Generate the combined text for each sentiment category for the current venue
        venue_positive_texts[venue_name] = ' '.join([' '.join(review) for review in positive_reviews])
        venue_neutral_texts[venue_name] = ' '.join([' '.join(review) for review in neutral_reviews])
        venue_negative_texts[venue_name] = ' '.join([' '.join(review) for review in negative_reviews])

    return venue_positive_texts, venue_neutral_texts, venue_negative_texts

def generate_wordcloud(text, title):
    wordcloud = WordCloud(max_font_size=80,
                          max_words=20,
                          background_color="white",
                          colormap='viridis',
                          prefer_horizontal=0.9,
                          margin=10).generate(text)

    fig, ax = plt.subplots(figsize=(3, 2))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(title)

    st.pyplot(fig)


def main():
    # Layout settings
    # st.set_page_config(layout="wide")

    st.title("Analysis Walkthrough")
    st.write("""
    On this page, I will walk you through our data and how we truly begin to understand
     the sentiment behind our reviews .""")
    st.write(""" 
    After Data cleaning and preprocessing I ran two pre-trained Sentiment models on my dataset.
    Two BERT models from Hugging Face""")

    images = [
        ("Bert Soda", "images/bert_soda.png"),
        ("Bert Lost Weekend", "images/bert_lost.png"),
        ("Roberta Soda", "images/ro_soda.png"),
        ("Roberta Lost Weekend", "images/ro_lost.png"),
    ]

    # Sidebar enhancements
    st.sidebar.header("Time series analysis of both Sentiment models")

    # Extract image descriptions for the radio selector
    image_descriptions = [img[0] for img in images]
    selected_description = st.sidebar.radio("", image_descriptions)

    # Fetch the corresponding image path for the selected description
    selected_image_path = next((img[1] for img in images if img[0] == selected_description), None)

    if selected_image_path:
        # Display the selected image with caption and adjusted width
        st.image(selected_image_path, caption=selected_description, width=1200)
    else:
        st.warning("The selected image is missing. Please check the image path.")

    st.subheader("Average Sentiment Score Distribution by Venue")

    # Dropdown to select venue
    available_venues = roberta_df['name'].unique()
    selected_venue = st.selectbox("Choose a Venue:", available_venues)

    # Plot sentiment scores for the selected venue
    plot_sentiment_for_venue(roberta_df, selected_venue)

    st.write("""After analysing the results and outputs of both models the 2nd Roberta model seemed
             like the right fit for further analysis""")

    st.subheader("So what are the people talking about?")
    # st.write(positive_text)

    # Add word cloud generation option
    wordcloud_options = {"Positive": positive_text, "Neutral": neutral_text, "Negative": negative_text}
    chosen_sentiment = st.selectbox("Select a sentiment to view its word cloud:", list(wordcloud_options.keys()))
    generate_wordcloud(wordcloud_options[chosen_sentiment], f" Most common words in {chosen_sentiment} Reviews")

    st.subheader("Further insights into the word clouds by venue")

    # Using the function to get the combined texts
    venue_positive_texts, venue_neutral_texts, venue_negative_texts = generate_venue_wordclouds(roberta_df)

    # Let users select the venue
    selected_venue = st.selectbox("Select a venue:", list(venue_positive_texts.keys()))

    # Let users select sentiment for the word cloud
    sentiment_options = {"Positive": venue_positive_texts, "Neutral": venue_neutral_texts,
                             "Negative": venue_negative_texts}
    chosen_sentiment = st.selectbox("Select a sentiment:", list(sentiment_options.keys()))

     # Generate the word cloud for the selected venue and sentiment
    if sentiment_options[chosen_sentiment][selected_venue]:
        generate_wordcloud(sentiment_options[chosen_sentiment][selected_venue],
                               f"Words in {selected_venue} {chosen_sentiment} Reviews")
    else:
        st.write(f"No {chosen_sentiment.lower()} reviews found for {selected_venue}.")


if __name__ == "__main__":
    main()
