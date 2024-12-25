import pandas as pd
import streamlit as st
import plotly.graph_objects as go  # Import Plotly
#
st.set_page_config(layout="wide", page_title="Artist Trends")

# Display a general message at the top
st.markdown("## I'm a music nerd, but especially for (neo)soul. I'm also a fan of the [COLORS](https://www.youtube.com/@COLORSxSTUDIOS) show on YouTube. In this spirit, I scraped some Spotify data of lots of artist who I like/are in genres I like and made an app of it.")



# Load the dataset


@st.cache_data
def load_data():
    file_path = r"https://raw.githubusercontent.com/jgreathouse9/jgreathouse9.github.io/refs/heads/master/Spotify/Merged_Spotify_Data.csv"
    data = pd.read_csv(file_path)

    # Strip time portion and convert to datetime

    data["Date"] = pd.to_datetime(
        data["Date"].str.split(" ").str[0], format="%Y-%m-%d", errors="coerce"
    )

    return data


data = load_data()

# Artist Selection in the sidebar

artist_list = sorted(data["Artist"].unique())  # Sort the artist list alphabetically
default_artist = "Tyla" if "Tyla" in artist_list else artist_list[0]
selected_artists = st.sidebar.multiselect(
    "Choose artists", artist_list, default=[default_artist]
)

# Metric Selection in the sidebar

metric = st.sidebar.radio(
    "Choose a metric to plot:",
    options=["Playlist Reach", "Playlists", "Popularity", "Monthly Listeners"],
)

# Date Range Selector in the sidebar

start_date, end_date = st.sidebar.date_input(
    "Select date range",
    [data["Date"].min().date(), data["Date"].max().date()],
    min_value=data["Date"].min().date(),
    max_value=data["Date"].max().date(),
)

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
    vertical_line_date = st.sidebar.date_input(
        "Select date for vertical reference line",
        min_value=data["Date"].min().date(),
        max_value=data["Date"].max().date(),
        value=data["Date"].min().date(),
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
