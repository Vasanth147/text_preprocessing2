import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter

data = [
    {"headline": "MI Women Crush UP Warriorz!", "entities": {'ORG': 'MI Women'}, "vader": -0.2244, "textblob": 0.0, "source": "Cricket Times", "likes": 66, "comments": 12, "reposts": 0, "time": "4d"},
    {"headline": "Mumbai Indians Women Outclass UP Warriorz Women with an 8-Wicket Victory!", "entities": {'ORG': 'Mumbai Indians Women'}, "vader": 0.0, "textblob": 0.0, "source": "Cricket Buzz", "likes": 50, "comments": 15, "reposts": 2, "time": "3d"},
    {"headline": "Harmanpreet Kaur Leads India to Victory in T20 Series Against Australia!", "entities": {'PERSON': 'Harmanpreet Kaur', 'EVENT': 'T20 Series', 'GPE': 'Australia'}, "vader": 0.0, "textblob": 0.0, "source": "Sports India", "likes": 120, "comments": 30, "reposts": 5, "time": "2d"},
    {"headline": "Smriti Mandhana’s Century Powers India to a Record-Breaking Win!", "entities": {'ORG': 'Century Powers India'}, "vader": 0.6239, "textblob": 1.0, "source": "Cricket Times", "likes": 200, "comments": 40, "reposts": 10, "time": "1d"},
    {"headline": "BCCI Announces Central Contracts for Women's Team: Who Made the Cut?", "entities": {'ORG': "BCCI Central Contracts"}, "vader": -0.2732, "textblob": 0.0, "source": "Cricket Buzz", "likes": 80, "comments": 25, "reposts": 3, "time": "5d"}
]

df = pd.DataFrame(data)


def categorize_sentiment(vader_score):
    if vader_score > 0.2:
        return "Positive"
    elif vader_score < -0.2:
        return "Negative"
    else:
        return "Neutral"

df["sentiment_category"] = df["vader"].apply(categorize_sentiment)


df["days_ago"] = df["time"].apply(lambda x: int(x.replace("d", "")))

entity_list = []
for row in df["entities"]:
    entity_list.extend(row.values())


entity_counts = Counter(entity_list)
top_entities = entity_counts.most_common(10)


st.set_page_config(page_title="Women’s Cricket Insights", layout="wide")

st.title("Women’s Cricket News Dashboard")

st.subheader("Trending News (Top Headlines by Engagement)")
top_news = df.sort_values(by=["likes", "comments", "reposts"], ascending=False)
st.table(top_news[["headline", "likes", "comments", "reposts"]].head(5))


st.subheader("Sentiment Trends Over Time")

fig = px.line(df.sort_values("days_ago"), x="days_ago", y="vader", markers=True, title="Sentiment Shifts Over Time")
fig.update_xaxes(title_text="Days Ago")
fig.update_yaxes(title_text="VADER Sentiment Score")
st.plotly_chart(fig)


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


st.subheader("Platform-Wise Audience Engagement")

engagement_metrics = df.groupby("source")[["likes", "comments", "reposts"]].sum()
fig = px.bar(engagement_metrics, barmode="group", title="Engagement by Platform", labels={"value": "Count", "variable": "Metric"})
st.plotly_chart(fig)


st.subheader("Key Inferences & Conclusions")
st.markdown("""
- **Most Engagement:** "Smriti Mandhana’s Century Powers India" had the highest engagement.
- **Sentiment Trends:** Mixed emotions; Smriti Mandhana’s century had the most **positive** sentiment.
- **Top Players & Teams:** Mumbai Indians Women & Harmanpreet Kaur were frequently mentioned.
- **Audience Engagement:** "Cricket Times" and "Cricket Buzz" had the most audience interaction.
- **News Cycle Impact:** Engagement spikes for big events (matches, contracts, rankings).
""")
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import matplotlib.pyplot as plt
# import seaborn as sns
# from wordcloud import WordCloud
# from collections import Counter

# data = [
#     {"headline": "Top 5 Indian Women Cricketers Who Are Inspiring the Next Generation of Girls", "entities": {'CARDINAL': '5'}, "vader": 0.5574, "textblob": 0.3333, "source": "Cricket Insights", "likes": 120, "comments": 35, "reposts": 5, "time": "4d"},
#     {"headline": "The Daily Cricket Digest - Why do Indian stars need a 150 kg baggage allowance?!", "entities": {'ORG': 'The Daily Cricket Digest - Why', 'NORP': 'Indian', 'QUANTITY': 'a 150 kg'}, "vader": 0.0, "textblob": 0.0, "source": "Cricket Buzz", "likes": 90, "comments": 25, "reposts": 3, "time": "3d"},
#     {"headline": "Jay Shah's Role in Transforming Indian Cricket", "entities": {'PERSON': "Jay Shah's"}, "vader": 0.0, "textblob": 0.0, "source": "Sports Today", "likes": 80, "comments": 20, "reposts": 2, "time": "2d"},
#     {"headline": "Women’s T20 World Cup 2024: 6 Indian Women Players to Watch For", "entities": {'ORG': 'Women’s T20 World Cup 2024', 'CARDINAL': '6', 'NORP': 'Indian'}, "vader": 0.0, "textblob": 0.0, "source": "Cricket Times", "likes": 200, "comments": 50, "reposts": 8, "time": "1d"},
#     {"headline": "Beyond Cricket: Yuvraj Singh’s Inspiring Story of Hope and Strength", "entities": {'PERSON': 'Yuvraj Singh’s'}, "vader": 0.836, "textblob": 0.5, "source": "Sports India", "likes": 220, "comments": 60, "reposts": 15, "time": "5d"}
# ]

# df = pd.DataFrame(data)

# def categorize_sentiment(vader_score):
#     if vader_score > 0.2:
#         return "Positive"
#     elif vader_score < -0.2:
#         return "Negative"
#     else:
#         return "Neutral"

# df["sentiment_category"] = df["vader"].apply(categorize_sentiment)

# df["days_ago"] = df["time"].apply(lambda x: int(x.replace("d", "")))

# entity_list = []
# for row in df["entities"]:
#     entity_list.extend(row.values())

# entity_counts = Counter(entity_list)
# top_entities = entity_counts.most_common(10)

# st.set_page_config(page_title="Women’s Cricket Insights", layout="wide")

# st.title("Women’s Cricket News Dashboard")

# st.subheader("Trending News (Top Headlines by Engagement)")
# top_news = df.sort_values(by=["likes", "comments", "reposts"], ascending=False)
# st.table(top_news[["headline", "likes", "comments", "reposts"]].head(5))

# st.subheader("Sentiment Trends Over Time")

# fig = px.line(df.sort_values("days_ago"), x="days_ago", y="vader", markers=True, title="Sentiment Shifts Over Time")
# fig.update_xaxes(title_text="Days Ago")
# fig.update_yaxes(title_text="VADER Sentiment Score")
# st.plotly_chart(fig)

# st.subheader("Most Mentioned Players & Teams")

# wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(entity_counts)
# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# st.pyplot(plt)

# fig = px.bar(x=[e[0] for e in top_entities], y=[e[1] for e in top_entities], 
#              title="Top Mentioned Players & Teams", labels={"x": "Name", "y": "Mentions"}, color=[e[1] for e in top_entities])
# fig.update_xaxes(title_text="Players/Teams")
# fig.update_yaxes(title_text="Mentions")
# st.plotly_chart(fig)

# st.subheader("Platform-Wise Audience Engagement")

# engagement_metrics = df.groupby("source")[["likes", "comments", "reposts"]].sum()
# fig = px.bar(engagement_metrics, barmode="group", title="Engagement by Platform", labels={"value": "Count", "variable": "Metric"})
# st.plotly_chart(fig)

# st.subheader("Key Inferences & Conclusions")
# st.markdown("""
# - **Most Engagement:** "Beyond Cricket: Yuvraj Singh’s Inspiring Story of Hope and Strength" had the highest engagement.
# - **Sentiment Trends:** Mixed emotions; Yuvraj Singh’s story had the most **positive** sentiment.
# - **Top Players & Teams:** Women’s T20 World Cup 2024 & Jay Shah were frequently mentioned.
# - **Audience Engagement:** "Cricket Times" and "Cricket Buzz" had the most audience interaction.
# - **News Cycle Impact:** Engagement spikes for big events (player stories, tournaments, off-field discussions).
# """)
