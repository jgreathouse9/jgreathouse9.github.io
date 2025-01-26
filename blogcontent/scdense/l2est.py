import pandas as pd
from mlsynth.mlsynth import PDA
import matplotlib
import os
import matplotlib.pyplot as plt

def set_theme():
    theme = {
        "axes.grid": True,
        "grid.linestyle": "-",
        "grid.color": "black",
        "legend.framealpha": 1,
        "legend.facecolor": "white",
        "legend.shadow": True,
        "legend.fontsize": 14,
        "legend.title_fontsize": 16,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        "axes.labelsize": 16,
        "axes.titlesize": 20,
        "figure.dpi": 100,
        "axes.facecolor": "white",
        "figure.figsize": (10, 5.5),
    }
    matplotlib.rcParams.update(theme)


# Function to normalize data
def normalize(group, column_name, reference_date):
    # Work only with the relevant columns
    data = group.copy()
    reference_value = data.loc[data['Date'] == pd.Timestamp(reference_date), column_name]
    if not reference_value.empty:
        data[column_name] = data[column_name] / reference_value.values[0] * 100
    return data


def preprocess_data(url, date_range, column_name, treat_artist, reference_date):
    # Load the data
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Filter by date range
    df = df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]

    # Add treatment column
    df['Water'] = df.apply(
        lambda row: 1 if row['Artist'] == treat_artist and row['Date'] > pd.to_datetime(reference_date) else 0,
        axis=1,
    )

    # Get the number of observations for the treated artist
    tyla_observations = df[df['Artist'] == treat_artist].shape[0]

    # Filter artists with at least as many observations as the treated artist
    artist_counts = df['Artist'].value_counts()
    artists_to_keep = artist_counts[artist_counts >= tyla_observations].index
    df = df[df['Artist'].isin(artists_to_keep)]
    df = df[df['Artist'] != 'Lisa Oduor-Noah']
    # Group by Artist, normalize each group, and combine into a single DataFrame
    grouped = df.groupby('Artist')
    normalized_groups = [
        normalize(group.copy(), column_name=column_name, reference_date=reference_date)
        for artist, group in grouped
    ]
    df = pd.concat(normalized_groups, ignore_index=True)

    return df





# Set theme
set_theme()

# Define the save directory (blogcontent/scdense/figures/)
save_directory = os.path.join(os.getcwd(), "blogcontent", "scdense", "figures")

# Create the directory if it doesn't exist
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Define the filename and extension
save_1 = {
    "filename": "SpotifyTyla",  # New filename
    "extension": "png",  # Desired extension
    "directory": save_directory,  # Save in the specified directory
}

outcome = 'Playlist Reach'

# Spotify Data
spotify_url = "https://raw.githubusercontent.com/jgreathouse9/jgreathouse9.github.io/refs/heads/master/Spotify/Merged_Spotify_Data.csv"
spotify_date_range = ['2023-01-01', '2024-06-01']
spotify_df = preprocess_data(
    url=spotify_url,
    date_range=spotify_date_range,
    column_name=outcome,
    treat_artist='Tyla',
    reference_date='2023-08-17'
)

spotify_config = {
    "df": spotify_df,
    "treat": "Water",
    "time": "Date",
    "outcome": outcome,
    "unitid": "Artist",
    "counterfactual_color": "red",
    "treated_color": "black",
    "display_graphs": True,
    "method": "l2",
    "save": save_1
}

spotify_model = PDA(spotify_config)
ARCO_results = spotify_model.fit()

# Define the filename and extension
save_2 = {
    "filename": "AppleTyla",  # New filename
    "extension": "png",  # Desired extension
    "directory": save_directory,  # Save in the specified directory
}


# Apple Music Data
apple_url = "https://raw.githubusercontent.com/jgreathouse9/jgreathouse9.github.io/refs/heads/master/Apple%20Music/AppleMusic.csv"
apple_date_range = ['2022-01-01', '2024-12-31']
apple_df = preprocess_data(
    url=apple_url,
    date_range=apple_date_range,
    column_name='Playlists',
    treat_artist='Tyla',
    reference_date='2023-08-17'
)
appleoutcome = 'Playlists'

apple_config = {
    "df": apple_df,
    "treat": "Water",
    "time": "Date",
    "outcome": "Playlists",
    "unitid": "Artist",
    "counterfactual_color": "red",
    "treated_color": "black",
    "display_graphs": True,
    "method": "l2",
    "save": save_2
}

apple_model = PDA(apple_config)
apple_results = apple_model.fit()
