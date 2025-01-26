import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from mlsynth.mlsynth import dataprep
import os

# Set up theme for Matplotlib
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
    data = group.copy()
    reference_value = data.loc[data['Date'] == pd.Timestamp(reference_date), column_name]
    if not reference_value.empty:
        data[column_name] = data[column_name] / reference_value.values[0] * 100
    return data


# Function to preprocess data
def preprocess_data(url, date_range, column_name, treat_artist, reference_date):
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]
    df['Water'] = df.apply(
        lambda row: 1 if row['Artist'] == treat_artist and row['Date'] > pd.to_datetime(reference_date) else 0,
        axis=1,
    )
    tyla_observations = df[df['Artist'] == treat_artist].shape[0]
    artist_counts = df['Artist'].value_counts()
    artists_to_keep = artist_counts[artist_counts >= tyla_observations].index
    df = df[df['Artist'].isin(artists_to_keep)]
    df = df[df['Artist'] != 'Lisa Oduor-Noah']
    grouped = df.groupby('Artist')
    normalized_groups = [
        normalize(group.copy(), column_name=column_name, reference_date=reference_date)
        for artist, group in grouped
    ]
    return pd.concat(normalized_groups, ignore_index=True)


# Plot treated unit and donors with average controls
def plot_donors_and_treated(donor_matrix, treated_vector, pre_periods, title, ax):
    for i in range(donor_matrix.shape[1]):
        ax.plot(donor_matrix[:, i], color='gray', linewidth=0.5, alpha=0.8, label='_nolegend_')
    ax.plot(treated_vector, color='black', linewidth=2, label='Treated Unit')
    average_controls = donor_matrix.mean(axis=1)
    ax.plot(average_controls, color='red', linewidth=2, label='Normalized Average of Controls')
    ax.axvline(x=pre_periods, color='blue', linestyle='--', linewidth=1.5, label='Water')
    ax.set_title(title)
    ax.set_xlabel('Time Periods')


# Main plotting routine
def main():
    set_theme()

    # Spotify Data
    spotify_url = "https://raw.githubusercontent.com/jgreathouse9/jgreathouse9.github.io/refs/heads/master/Spotify/Merged_Spotify_Data.csv"
    spotify_date_range = ['2023-01-01', '2024-06-01']
    outcome = 'Playlist Reach'
    spotify_df = preprocess_data(
        url=spotify_url,
        date_range=spotify_date_range,
        column_name=outcome,
        treat_artist='Tyla',
        reference_date='2023-08-17'
    )
    spotify_prepped = dataprep(spotify_df, 'Artist', 'Date', outcome, 'Water')

    # Apple Music Data
    apple_url = "https://raw.githubusercontent.com/jgreathouse9/jgreathouse9.github.io/refs/heads/master/Apple%20Music/AppleMusic.csv"
    apple_date_range = ['2022-01-01', '2024-06-01']
    apple_outcome = 'Playlists'
    apple_df = preprocess_data(
        url=apple_url,
        date_range=apple_date_range,
        column_name=apple_outcome,
        treat_artist='Tyla',
        reference_date='2023-08-17'
    )
    apple_prepped = dataprep(apple_df, 'Artist', 'Date', apple_outcome, 'Water')

    # Ensure the directory exists
    output_dir = '/blogcontent/scdense/'
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Create two-plot figure
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)
    plot_donors_and_treated(
        spotify_prepped["donor_matrix"], spotify_prepped["y"], spotify_prepped["pre_periods"],
        "Spotify: Tyla's Playlist Reach vs Controls", axes[0]
    )
    axes[0].set_ylabel('Outcome')
    plot_donors_and_treated(
        apple_prepped["donor_matrix"], apple_prepped["y"], apple_prepped["pre_periods"],
        "Apple Music: Tyla's Playlist Count vs Controls", axes[1]
    )

    axes[1].legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'spotapp.png'))
    plt.close()


if __name__ == "__main__":
    main()
