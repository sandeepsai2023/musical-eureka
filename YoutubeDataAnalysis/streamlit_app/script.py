# nohup streamlit run '/Users/saisandeep/GitRepo/musical-eureka/YoutubeDataAnalysis/streamlit_app/script.py' &
# ps aux | grep streamlit


"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import calplot
import plotly.graph_objects as go
import ast



df_video_metadata_new = pd.read_csv('/Users/saisandeep/GitRepo/musical-eureka/YoutubeDataAnalysis/Data/video_metadata_new.csv',header=0)
df_watch_history = pd.read_csv('/Users/saisandeep/GitRepo/musical-eureka/YoutubeDataAnalysis/Data/watch_history.csv',header=0)
df_final = df_watch_history.merge(df_video_metadata_new,left_on='video_id',right_on='id',how='left',suffixes=('_watch_history','_video_metadata'))
df_final = df_final.dropna(subset=['video_id'])
df_final = df_final.drop_duplicates(subset=['time','video_id'])

st.dataframe(df_final)

temp = df_final.groupby('channelTitle').agg(num_of_videos=('video_id',pd.Series.nunique)).reset_index().sort_values(by='num_of_videos',ascending=False)
st.dataframe(temp)

st.text(df_final.columns)

st.sidebar.header("Filter Options")
tag_input = st.sidebar.text_input("Enter a tag to filter:", "")
temp = df_final[df_final['tags'].notna()]
temp = temp[~temp['tags'].str.contains(r'\[\]', regex=True)]
temp['tags'] = temp['tags'].apply(lambda x: x.replace('[','').replace(']',''))
temp['tags'] = temp['tags'].apply(ast.literal_eval)
temp = temp.explode('tags')
if tag_input:
    temp = temp[temp['tags'].str.contains(tag_input)]
temp_agg = temp.groupby('watch_date').agg(num_of_videos=('video_id',pd.Series.nunique)).reset_index().sort_values(by='num_of_videos',ascending=False)
st.dataframe(temp_agg)

# Convert 'watch_date' to datetime, handle errors by setting invalid parsing as NaT
temp['watch_date'] = pd.to_datetime(temp['watch_date'], errors='coerce')

# Drop rows where 'watch_date' couldn't be parsed
temp = temp.dropna(subset=['watch_date'])

# Date range selector
min_date = temp['watch_date'].min()
max_date = temp['watch_date'].max()

start_date, end_date = st.sidebar.date_input(
    "Select date range:",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Convert date inputs to datetime
if isinstance(start_date, (tuple, list)):
    start_date = pd.to_datetime(start_date[0])
    end_date = pd.to_datetime(end_date[1])
else:
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

# Filter the DataFrame based on the input tag and date range
if tag_input:
    # Filter rows where 'tags' match the input (case-insensitive)
    filtered_df = temp[temp['tags'].str.lower() == tag_input.lower()]
else:
    # If no tag is input, use the entire DataFrame
    filtered_df = temp.copy()

# Further filter by date range
filtered_df = filtered_df[
    (filtered_df['watch_date'] >= start_date) &
    (filtered_df['watch_date'] <= end_date)
]

# Check if the filtered DataFrame is not empty
if not filtered_df.empty:
    # Aggregate data by date to get daily counts
    daily_trend = filtered_df.groupby('watch_date').size().reset_index(name='count')
    daily_trend = daily_trend.sort_values('watch_date')

    # Display the filtered data (optional)
    st.write(f"### Showing results for tag: `{tag_input}`")
    st.write(daily_trend)

    # Plot the trend using Plotly
    fig = px.line(
        daily_trend,
        x='watch_date',
        y='count',
        title=f"Daily Trend for Tag: `{tag_input}`",
        labels={'watch_date': 'Date', 'count': 'Number of Videos'},
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No data found for the specified tag and date range.")




# Convert 'time' to datetime format with mixed inference
df_final['time'] = pd.to_datetime(df_final['time'], format='mixed', errors='coerce')


# Sidebar filter for aggregation level
aggregation_level = st.sidebar.selectbox(
    "Select Aggregation Level",
    ["Daily", "Monthly", "Weekly"]
)

# Aggregate data based on the selected level
if aggregation_level == "Daily":
    df_final['date'] = df_final['time'].dt.date
    aggregated_data = df_final.groupby('date').size().reset_index(name='count')
elif aggregation_level == "Weekly":
    df_final['week'] = df_final['time'].dt.to_period('W').apply(lambda r: r.start_time)
    aggregated_data = df_final.groupby('week').size().reset_index(name='count')
elif aggregation_level == "Monthly":
    df_final['month'] = df_final['time'].dt.to_period('M').apply(lambda r: r.start_time)
    aggregated_data = df_final.groupby('month').size().reset_index(name='count')

# Create the heatmap-like visualization
# Adding some randomness to 'count' for visualization purposes
aggregated_data['count'] = aggregated_data['count'] + np.random.randint(1, 10, size=len(aggregated_data))

fig = px.density_heatmap(
    aggregated_data,
    x=aggregated_data.columns[0],  # 'date', 'week', or 'month' depending on aggregation
    y='count',
    nbinsx=30,
    title="Activity Heatmap",
    labels={'x': 'Date', 'y': 'Activity Count'}
)

# Display the heatmap in Streamlit
st.title("YouTube Activity Contribution Heatmap")
st.plotly_chart(fig)

# Display data
st.write("Aggregated Data Used for the Heatmap:")
st.dataframe(aggregated_data)

youtube_product = st.sidebar.selectbox(
    "Select Youtueb Product",
    ["YouTube Music", "YouTube","All"]
)

if youtube_product == "YouTube Music":
    df_product = df_final[df_final['header'].str.contains("YouTube Music")]
elif youtube_product == "YouTube":
    df_product = df_final[df_final['header'].str.contains("YouTube")]
elif youtube_product == "All":
    df_product = df_final.copy()

# Aggregate data by date to count number of videos watched per day
df_product['date'] = df_product['time'].dt.date
aggregated_data = df_product.groupby('date').size().reset_index(name='count')

# Convert to a Series with the dates as index, required for calplot
heatmap_data = pd.Series(aggregated_data['count'].values, index=pd.to_datetime(aggregated_data['date']))

# Create a Calendar Heatmap using calplot
fig, ax = calplot.calplot(heatmap_data, cmap='Greens', colorbar=True, suptitle='YouTube Activity Heatmap')

# Display the heatmap in Streamlit
st.title("YouTube Activity Contribution Heatmap")
st.pyplot(fig)

# Display data
st.write("Aggregated Data Used for the Heatmap:")
st.dataframe(aggregated_data)



# Convert 'time' to datetime format
df_final['time'] = pd.to_datetime(df_final['time'])

# Aggregate data by date to count number of videos watched per day
df_final['date'] = df_final['time'].dt.date
aggregated_data = df_final.groupby('date').size().reset_index(name='count')

# Prepare the data for the heatmap
aggregated_data['week'] = aggregated_data['date'].apply(lambda x: x.strftime('%U'))  # week number of the year
aggregated_data['day'] = aggregated_data['date'].apply(lambda x: x.weekday())  # day of the week (0=Monday)

# Creating a grid-like layout for the heatmap (similar to GitHub contributions)
weeks = aggregated_data['week'].unique()
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

heatmap_data = np.zeros((len(days), len(weeks)))  # Creating an empty array for the heatmap

for _, row in aggregated_data.iterrows():
    week_idx = list(weeks).index(row['week'])
    day_idx = row['day']
    heatmap_data[day_idx, week_idx] = row['count']

# Create the heatmap using Plotly
fig = go.Figure(data=go.Heatmap(
    z=heatmap_data,
    x=weeks,
    y=days,
    colorscale='Greens',
    hoverongaps=False,
    text=aggregated_data.apply(lambda row: f"Date: {row['date']}<br>Videos Watched: {row['count']}", axis=1),
    hoverinfo='text'
))

fig.update_layout(
    title='YouTube Activity Contribution Heatmap',
    xaxis_nticks=len(weeks) // 2,
    yaxis_nticks=len(days),
    xaxis_title="Week Number",
    yaxis_title="Day of Week",
    yaxis=dict(
        tickmode='array',
        tickvals=list(range(len(days))),
        ticktext=days,
    )
)

# Render in Streamlit
st.title("YouTube Activity Contribution Heatmap")
st.plotly_chart(fig)

# Display data
st.write("Aggregated Data Used for the Heatmap:")
st.dataframe(aggregated_data)