import streamlit as st
from streamlit_option_menu import option_menu
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
engine = create_engine("mysql+pymysql://root:Password@localhost/imdbdatadb")

st.set_page_config(
    page_title="IMDB 2024 Movie List", 
    page_icon="🎬", 
    layout="wide")

def convert_duration(duration_str):
    try:
        parts = duration_str.lower().replace(" ", "").replace("h", ":").replace("m", "").split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 1:
            return int(parts[0])
    except:
        return None
    
def convert_to_number(value):
    if isinstance(value, str):
        value = value.strip().upper().replace(",", "")
        if value.endswith('K'):
            return float(value[:-1]) * 1_000
        elif value.endswith('M'):
            return float(value[:-1]) * 1_000_000
        elif value.replace('.', '', 1).isdigit():
            return float(value)
    elif isinstance(value, (int, float)):
        return value
    return 0
with st.sidebar : 
    selected = option_menu(
        menu_title="IMDB Dashboard", 
        options=["Top-Rated Movies", "Correlation Analysis", "Genre Analysis", "Duration Insights","Voting Patterns","Rating Distribution", "Genre-Based Rating Leader","Most Popular Genres by Voting","Duration Extremes","Ratings by Genre","Filter Data"],
        menu_icon="film",
        default_index=0,
    )


# Page: Top-Rated Movies
if selected == "Top-Rated Movies":
    st.title("Top 10 Movies by Rating and Voting Counts")
    @st.cache_data
    def get_data():
        query = "SELECT * FROM imdbmovielist2024 ORDER BY Ratings DESC, `Voting_Counts` DESC LIMIT 10"
        return pd.read_sql(query, engine)
    df = get_data()
    st.dataframe(df)
    
elif selected == "Genre Analysis":
    st.title("Genre Distribution")
    st.write("Plot the count of movies for each genre in a bar chart.")
    @st.cache_data
    def get_data():
        query = "SELECT Genre FROM imdbmovielist2024"
        return pd.read_sql(query, engine)

    df = get_data()
    genre_counts = df['Genre'].value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Movie Count']
    fig, ax = plt.subplots(figsize=(5, 5))
    sns.barplot(data=genre_counts, x='Genre', y='Movie Count', ax=ax, palette='bright')
    ax.set_title("Number of Movies by Genre")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Movie Count")

    st.pyplot(fig)

elif selected == "Duration Insights":
    st.title("Genre Distribution")
    st.write("Analyze the average duration of movies across genres.")
    @st.cache_data
    def get_data():
        query = "SELECT Genre, Duration FROM imdbmovielist2024"
        return pd.read_sql(query, engine)

    df = get_data()
    df["Duration_Min"] = df["Duration"].apply(convert_duration)
    avg_duration = df.groupby("Genre")["Duration_Min"].mean().sort_values()

    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_duration.values, y=avg_duration.index, palette="coolwarm")
    for i, (genre, avg) in enumerate(avg_duration.items()):
        plt.text(avg - 5, i, f"{int(avg)} min", color='white', va='center', ha='right', fontweight='bold')

    plt.title("Average Movie Duration by Genre (2024)", fontsize=14)
    plt.xlabel("Average Duration (minutes)")
    plt.ylabel("Genre")
    plt.tight_layout()
    st.pyplot(plt)

elif selected == "Voting Patterns":
    st.title("Voting Trends by Genre")
    st.write("Discover genres with the highest average voting counts.")
    @st.cache_data
    def get_data():
        query = "SELECT Genre, Voting_Counts FROM imdbmovielist2024"
        return pd.read_sql(query, engine)
    df = get_data()
    df['Voting_Counts'] = df['Voting_Counts'].apply(convert_to_number).astype(int)
    avg_votes = df.groupby("Genre")["Voting_Counts"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 5))  
    sns.barplot(x=avg_votes.values, y=avg_votes.index, ax=ax, palette='bright')
    for i, (genre, vote) in enumerate(avg_votes.items()):
        ax.text(vote - max(avg_votes) * 0.05, i, f"{int(vote):,}", 
                color='white', va='center', ha='right', fontweight='bold')

    ax.set_title("Average Voting Counts by Genre", fontsize=14)
    ax.set_xlabel("Average Voting Counts")
    ax.set_ylabel("Genre")
    plt.tight_layout()
    st.pyplot(fig)


# Page: Correlation Analysis
elif selected == "Correlation Analysis":
    st.title("Correlation Analysis")
    st.write("This scatter plot analyzes the relationship between **Ratings** and **Voting Counts** for 2024 action movies.")
    df = pd.read_sql("SELECT Ratings, `Voting_Counts`, Duration FROM imdbmovielist2024", engine)
    df["Voting_Counts"] = df["Voting_Counts"].astype(float) 
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x="Ratings", y="Voting_Counts", ax=ax)
    ax.set_title("Ratings vs Voting Counts", fontsize=14)
    ax.set_xlabel("IMDB Ratings")
    ax.set_ylabel("Voting Counts")
    correlation = df["Ratings"].corr(df["Voting_Counts"])
    st.write(f"**Correlation Coefficient:** {correlation:.2f}")
    st.pyplot(fig)

# Page: Rating Distribution:
elif selected == "Rating Distribution":
    st.title("Rating Distribution")
    st.write("Analyze the distribution of ratings across all movies")
    df = pd.read_sql("SELECT Ratings FROM imdbmovielist2024", engine)
    df = df.dropna(subset=['Ratings'])
    st.subheader("Distribution of Movie Ratings")
    plot_type = st.radio("Choose a plot type:", ["Histogram", "Boxplot"])

    fig, ax = plt.subplots(figsize=(6, 4))

    if plot_type == "Histogram":
        sns.histplot(df['Ratings'], bins=15, kde=True, ax=ax, color='skyblue')
        ax.set_title("Histogram of Movie Ratings")
        ax.set_xlabel("Ratings")
        ax.set_ylabel("Count")
    else:
        sns.boxplot(x=df['Ratings'], ax=ax, color='lightcoral')
        ax.set_title("Boxplot of Movie Ratings")
        ax.set_xlabel("Ratings")

    st.pyplot(fig)
# Page: Genre-Based Rating Leader
elif selected == "Genre-Based Rating Leader":
    st.title("Genre-Based Rating Leaders")
    st.write("Highlight the top-rated movie for each genre in a table.")
    @st.cache_data
    def get_data():
        query = """ SELECT *
        FROM imdbmovielist2024 AS a
        WHERE Ratings = (
            SELECT MAX(Ratings)
            FROM imdbmovielist2024 AS b
            WHERE a.Genre = b.Genre
        )
        ORDER BY Genre, Ratings DESC"""
        return pd.read_sql(query, engine)
    df = get_data()
    st.dataframe(df)
# Page: Most Popular Genres by Voting
elif selected == "Most Popular Genres by Voting":
    st.title("Genre-Based Rating Leaders")
    st.write(" Identify genres with the highest total voting counts in a pie chart.")
    @st.cache_data
    def get_data():
        query = """SELECT Genre, Voting_Counts FROM imdbmovielist2024"""
        return pd.read_sql(query, engine)
    df = get_data()
    df["Voting_Counts"] = df["Voting_Counts"].astype(float) 
    voting_by_genre = df.groupby("Genre")["Voting_Counts"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(5, 5))
    colors = plt.cm.tab20.colors
    ax.pie(
        voting_by_genre,
        labels=voting_by_genre.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors
    )
    ax.set_title("Genres with Highest Total Voting Counts")
    ax.axis("equal") 
    st.pyplot(fig)
# Page: Most Popular Genres by Voting
elif selected == "Duration Extremes":
    st.title("Duration Extremes")
    st.write("Use a table or card display to show the shortest and longest movies.")
    @st.cache_data
    def get_data():
        query = """SELECT Movie_Name, Genre, Duration FROM imdbmovielist2024"""
        return pd.read_sql(query, engine)
        
    df = get_data()
    # df['Duration_Min'] = df['Duration'].str.extract(r'(\d+)').astype(float)
    df["Duration_Min"] = df["Duration"].apply(convert_duration)
    shortest_movie = df.sort_values("Duration_Min").head(1)
    longest_movie = df.sort_values("Duration_Min", ascending=False).head(1)
    st.write("**Shortest Movie:**")
    st.dataframe(shortest_movie[["Movie_Name", "Genre", "Duration"]], use_container_width=True)
    st.write("**Longest Movie:**")
    st.dataframe(longest_movie[["Movie_Name", "Genre", "Duration"]], use_container_width=True)

# Page: Ratings by Genre
elif selected == "Ratings by Genre":
    st.title("Ratings by Genre")
    st.write("Use a heatmap to compare average ratings across genres")
    @st.cache_data
    def get_data():
        query = """SELECT  Genre, Ratings FROM imdbmovielist2024"""
        return pd.read_sql(query, engine)
        
    df = get_data()
    # df['Duration_Min'] = df['Duration'].str.extract(r'(\d+)').astype(float)
    avg_ratings = df.groupby("Genre")["Ratings"].mean().reset_index()
    avg_ratings["dummy"] = "Genre"
    pivot_table = avg_ratings.pivot(index="Genre", columns="dummy", values="Ratings")

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(6, len(pivot_table) * 0.5))
    sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5, cbar=False, ax=ax)

    plt.title("Average Ratings by Genre", fontsize=14)
    plt.xlabel("")
    plt.ylabel("")
    plt.xticks([])
    plt.tight_layout()
    st.pyplot(fig)

elif selected == "Filter Data" :
    st.title("Interactive Filtering")
    @st.cache_data
    def get_data():
        query = "SELECT * FROM imdbmovielist2024"
        df = pd.read_sql(query, engine)
        duration_parts = df['Duration'].str.extract(r'(?:(\d+)h)?\s*(?:(\d+)m)?')
        duration_parts = duration_parts.fillna(0).astype(int)
        df['Duration_minutes'] = duration_parts[0] * 60 + duration_parts[1]
        return df        
    df = get_data()
    col1, col2 = st.columns(2)
    
    with col1:
        duration_filter = st.selectbox("Duration (Hours)", ["All","< 1 hrs", "1-2 hrs", "2–3 hrs", "> 3 hrs"])
        rating_filter = st.slider("Minimum Rating", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
    with col2:
        vote_filter = st.number_input("Minimum Voting Counts", min_value=0, value=0, step=100)
        genre_filter = st.multiselect("Select Genre(s)", options=df["Genre"].unique(), default=df["Genre"].unique())
    filtered_df = df.copy()
    filtered_df['Voting_Counts'] = filtered_df['Voting_Counts'].apply(convert_to_number).astype(int)
    if duration_filter == "< 1 hrs":
        filtered_df = filtered_df[(filtered_df['Duration_minutes'] < 60)]
    elif duration_filter == "1-2 hrs":
        filtered_df = filtered_df[(filtered_df['Duration_minutes'] >= 60) & (filtered_df['Duration_minutes'] <= 120)]
    elif duration_filter == "2–3 hrs":
        filtered_df = filtered_df[(filtered_df['Duration_minutes'] >= 120) & (filtered_df['Duration_minutes'] <= 180)]
    elif duration_filter == "> 3 hrs":
        filtered_df = filtered_df[filtered_df['Duration_minutes'] > 180]

    filtered_df = filtered_df[
        (filtered_df['Ratings'] >= rating_filter) &
        (filtered_df['Voting_Counts'] >= vote_filter) &
        (filtered_df['Genre'].isin(genre_filter))
    ]

    st.subheader(" Filtered Movie List")
    st.dataframe(filtered_df.reset_index(drop=True))

