import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide", page_title="Artist Trends")

# Display a general message at the top

st.markdown(
    "## I'm a music nerd. Especially for (neo)soul and alt-R/B music. I'm also a fan of the [COLORS](https://www.youtube.com/@COLORSxSTUDIOS) show on YouTube. In this spirit, I scraped some data from Spotify and Apple Music. The data are for lots of my favorite neo-soul artists, or other artists from generes I like. I made an app of it."
)

# Function to get the latest commit SHA for versioning


def get_csv_version(platform):
    if platform == "Spotify":
        url = (
            r"https://api.github.com/repos/jgreathouse9/jgreathouse9.github.io/commits"
            r"?path=Spotify/Merged_Spotify_Data.csv&page=1&per_page=1"
        )
    else:  # Apple Music
        url = (
            r"https://api.github.com/repos/jgreathouse9/jgreathouse9.github.io/commits"
            r"?path=Apple%20Music/AppleMusic.csv&page=1&per_page=1"
        )
    response = requests.get(url)
    if response.status_code == 200:
        commit_data = response.json()
        return commit_data[0]["sha"]  # Use the latest commit SHA as the version key
    else:
        st.error("Unable to fetch file version. Using default cache key.")
        return "default_version"


# Function to load the appropriate data based on the selected platform


@st.cache_data
def load_data(platform, version):
    if platform == "Spotify":
        file_path = r"https://raw.githubusercontent.com/jgreathouse9/jgreathouse9.github.io/refs/heads/master/Spotify/Merged_Spotify_Data.csv"
    else:  # Apple Music
        file_path = r"https://raw.githubusercontent.com/jgreathouse9/jgreathouse9.github.io/refs/heads/master/Apple%20Music/AppleMusic.csv"
    data = pd.read_csv(file_path)
    data["Date"] = pd.to_datetime(
        data["Date"].str.split(" ").str[0], format="%Y-%m-%d", errors="coerce"
    )
    return data


# Platform selection

platform = st.sidebar.radio(
    "Choose streaming platform",
    options=["Spotify", "Apple Music"],
    index=0,  # Default to Spotify
)

# Fetch CSV version key based on platform

csv_version = get_csv_version(platform)

# Load the appropriate data based on the selected platform

data = load_data(platform=platform, version=csv_version)

# Artist Selection in the sidebar

artist_list = sorted(data["Artist"].unique())
default_artist = "Tyla" if "Tyla" in artist_list else artist_list[0]
selected_artists = st.sidebar.multiselect(
    "Choose artists", artist_list, default=[default_artist]
)

# Metric Selection in the sidebar

metric = st.sidebar.radio(
    "Choose a metric to plot:",
    options=[col for col in data.columns if col not in ["Artist", "Date"]],
)

# Date Range Selector in the sidebar

st.sidebar.header("Date Range Selection")
date_slider = st.sidebar.slider(
    "Select date range:",
    min_value=data["Date"].min().date(),
    max_value=data["Date"].max().date(),
    value=(data["Date"].min().date(), data["Date"].max().date()),
    format="YYYY-MM-DD",
)
start_date, end_date = date_slider

# Filter the data based on the selected artist and date range

filtered_data = data[
    (data["Artist"].isin(selected_artists))
    & (data["Date"] >= pd.to_datetime(start_date))
    & (data["Date"] <= pd.to_datetime(end_date))
].sort_values(by="Date")

# X-axis Reference line for the date (added option to show or hide)

show_vertical_line = st.sidebar.checkbox("Show vertical reference line?", value=False)
vertical_line_date = None
if show_vertical_line:
    vertical_line_date = st.sidebar.slider(
        "Select date for vertical reference line",
        min_value=data["Date"].min().date(),
        max_value=data["Date"].max().date(),
        value=data["Date"].min().date(),
        format="YYYY-MM-DD",
    )
# Check if any data is available after filtering

if filtered_data.empty:
    st.write("No data available for the selected date range.")
else:
    # Create the plot

    fig = go.Figure()

    for artist in selected_artists:
        artist_data = filtered_data[filtered_data["Artist"] == artist]
        dates = artist_data["Date"]
        metric_values = artist_data[metric]

        # Add a line for each artist

        fig.add_trace(
            go.Scatter(
                x=dates,
                y=metric_values,
                mode="lines",
                name=artist,
                line=dict(
                    color=st.sidebar.color_picker(
                        f"Pick a color for {artist}", "#1DB954"
                    ),
                    dash=st.sidebar.radio(
                        f"Pick a line style for {artist}",
                        ["solid", "dot", "dash", "longdash"],
                    ),
                ),
                hovertemplate="<b>%{text}</b><br>Date: %{x|%Y-%m-%d}<br>"
                + f"{metric}: %{{y:.2f}}<extra></extra>",
                text=[artist] * len(dates),  # Set custom text for each hover event
            )
        )
    # Add vertical reference line if selected

    if show_vertical_line and vertical_line_date:
        fig.add_shape(
            type="line",
            x0=vertical_line_date,
            x1=vertical_line_date,
            y0=filtered_data[metric].min(),
            y1=filtered_data[metric].max(),
            line=dict(color="blue", dash="dot"),
        )
    # Set title and labels

    if len(selected_artists) == 1:
        fig.update_layout(
            title=f"{selected_artists[0]} - {metric}",
            xaxis_title="Date",
            yaxis_title=metric,
        )
    else:
        fig.update_layout(
            title="Multiple Artists - " + metric, xaxis_title="Date", yaxis_title=metric
        )
    # Show the plot in Streamlit

    st.plotly_chart(fig)
# Use st.empty() to refresh periodically

if "counter" not in st.session_state:
    st.session_state.counter = 0  # Initialize counter if it doesn't exist
# Increment counter every time the script reruns

st.session_state.counter += 1

# Wait 10 seconds before rerunning the app (without blocking the main process)

if st.session_state.counter % 2 == 0:
    time.sleep(10)  # Simulate wait before rerun
    st.rerun()  # Trigger a rerun of the app
