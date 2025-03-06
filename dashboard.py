import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter

# Set page configuration
st.set_page_config(page_title="Women’s Cricket Insights", layout="wide")

# Custom CSS to change background color to white
st.markdown(
    """
    <style>
        body {
            background-color: white !important;
        }
        .stApp {
            background-color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sample data
data = [
    {"headline": "MI Women Crush UP Warriorz!", "entities": {'ORG': 'MI Women'}, "vader": -0.2244, "textblob": 0.0, "source": "Cricket Times", "likes": 66, "comments": 12, "reposts": 0, "time": "4d"},
    {"headline": "Mumbai Indians Women Outclass UP Warriorz Women with an 8-Wicket Victory!", "entities": {'ORG': 'Mumbai Indians Women'}, "vader": 0.0, "textblob": 0.0, "source": "Cricket Buzz", "likes": 50, "comments": 15, "reposts": 2, "time": "3d"},
    {"headline": "Harmanpreet Kaur Leads India to Victory in T20 Series Against Australia!", "entities": {'PERSON': 'Harmanpreet Kaur', 'EVENT': 'T20 Series', 'GPE': 'Australia'}, "vader": 0.0, "textblob": 0.0, "source": "Sports India", "likes": 120, "comments": 30, "reposts": 5, "time": "2d"},
    {"headline": "Smriti Mandhana’s Century Powers India to a Record-Breaking Win!", "entities": {'ORG': 'Century Powers India'}, "vader": 0.6239, "textblob": 1.0, "source": "Cricket Times", "likes": 200, "comments": 40, "reposts": 10, "time": "1d"},
    {"headline": "BCCI Announces Central Contracts for Women's Team: Who Made the Cut?", "entities": {'ORG': "BCCI Central Contracts"}, "vader": -0.2732, "textblob": 0.0, "source": "Cricket Buzz", "likes": 80, "comments": 25, "reposts": 3, "time": "5d"}
]

df = pd.DataFrame(data)

# Function to categorize sentiment
def categorize_sentiment(vader_score):
    if vader_score > 0.2:
        return "Positive"
    elif vader_score < -0.2:
        return "Negative"
    else:
        return "Neutral"

df["sentiment_category"] = df["vader"].apply(categorize_sentiment)
df["days_ago"] = df["time"].apply(lambda x: int(x.replace("d", "")))

# Extracting entity mentions
entity_list = []
for row in df["entities"]:
    entity_list.extend(row.values())

entity_counts = Counter(entity_list)
top_entities = entity_counts.most_common(10)

# Dashboard Title
st.title("Women’s Cricket News Dashboard")

# Trending News Table
st.subheader("Trending News (Top Headlines by Engagement)")
top_news = df.sort_values(by=["likes", "comments", "reposts"], ascending=False)
st.table(top_news[["headline", "likes", "comments", "reposts"]].head(5))

# Sentiment Trends Over Time
st.subheader("Sentiment Trends Over Time")
fig = px.line(df.sort_values("days_ago"), x="days_ago", y="vader", markers=True, title="Sentiment Shifts Over Time")
fig.update_xaxes(title_text="Days Ago")
fig.update_yaxes(title_text="VADER Sentiment Score")
st.plotly_chart(fig)

# Most Mentioned Players & Teams
st.subheader("Most Mentioned Players & Teams")

wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(entity_counts)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(plt)

fig = px.bar(x=[e[0] for e in top_entities], y=[e[1] for e in top_entities], 
             title="Top Mentioned Players & Teams", labels={"x": "Name", "y": "Mentions"}, color=[e[1] for e in top_entities])
fig.update_xaxes(title_text="Players/Teams")
fig.update_yaxes(title_text="Mentions")
st.plotly_chart(fig)

# Platform-Wise Audience Engagement
st.subheader("Platform-Wise Audience Engagement")
engagement_metrics = df.groupby("source")[["likes", "comments", "reposts"]].sum()
fig = px.bar(engagement_metrics, barmode="group", title="Engagement by Platform", labels={"value": "Count", "variable": "Metric"})
st.plotly_chart(fig)

# Key Inferences & Conclusions
st.subheader("Key Inferences & Conclusions")
st.markdown("""
- **Most Engagement:** "Smriti Mandhana’s Century Powers India" had the highest engagement.
- **Sentiment Trends:** Mixed emotions; Smriti Mandhana’s century had the most **positive** sentiment.
- **Top Players & Teams:** Mumbai Indians Women & Harmanpreet Kaur were frequently mentioned.
- **Audience Engagement:** "Cricket Times" and "Cricket Buzz" had the most audience interaction.
- **News Cycle Impact:** Engagement spikes for big events (matches, contracts, rankings).
""")
