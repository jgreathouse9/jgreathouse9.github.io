import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# Define a custom theme for Matplotlib

jared_theme = {
    "axes.grid": True,
    "grid.linestyle": "-",
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
}
matplotlib.rcParams.update(jared_theme)


def load_data(url):
    """
    Load and process the Excel file into a DataFrame.

    Args:
        url (str): URL of the Excel file.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    # Load the Excel file

    df = pd.read_excel(url, header=[0, 1])

    # Drop the first column

    df = df.iloc[:, 2:]

    # Flatten the multi-index column names and clean up any unwanted characters like newline characters

    df.columns = [" ".join(col).strip().replace("\n", " ") for col in df.columns.values]

    # Drop the last row

    df = df.iloc[:-1, :]

    # Parse the 'Headline Date' column into datetime format

    df["Headline Date"] = pd.to_datetime(df["Headline Date"])

    # Create a new column for formatted labels (e.g., "Jan 2014")

    df["Month-Year"] = df["Headline Date"].dt.strftime("%b %Y")

    # Keep only the columns whose titles contain "Seasonally adjusted" and exclude columns containing "Non-Seas"

    seasonally_adjusted_columns = [
        col for col in df.columns if "Seasonally adjusted" in col
    ]
    non_seasonally_adjusted_columns = [col for col in df.columns if "Non-Seas" in col]

    # Drop the non-seasonally adjusted columns

    df = df.drop(columns=non_seasonally_adjusted_columns)

    # Make sure all selected columns are in the DataFrame

    selected_columns = ["Headline Date", "Month-Year"] + seasonally_adjusted_columns
    existing_columns = [col for col in selected_columns if col in df.columns]

    # Keep only the existing columns in the final DataFrame

    df = df[existing_columns]

    return df


def plot_data(df):
    """
    Plot the Visa consumer spending data.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
    """
    # Reduce the number of ticks to 12 evenly spaced

    tick_indices = list(range(0, len(df), max(len(df) // 8, 1)))

    # Plot the first column as x-axis and the last two columns as y-axis

    plt.figure(figsize=(12, 6))

    plt.plot(
        df["Month-Year"],
        df[df.columns[-2]],
        marker="o",
        markersize=4.5,
        linestyle="-",
        label="Discretionary",
        color="#1434CB",
    )
    plt.plot(
        df["Month-Year"],
        df[df.columns[-1]],
        marker="s",
        markersize=4.5,
        linestyle="-",
        label="Non-Discretionary",
        color="#EB001B",
    )

    # Customize the x-axis labels to show only 12 ticks

    plt.xticks(
        ticks=tick_indices,
        labels=df["Month-Year"].iloc[tick_indices],
        rotation=45,
        ha="right",
    )

    # Add labels, title, and grid

    plt.xlabel("Date")
    plt.ylabel("Seasonally Adjusted SMI")
    plt.title("Consumer Spending, Visa Data")
    plt.legend(title="SMI Data")

    # Show the plot

    plt.tight_layout()
    plt.show()
