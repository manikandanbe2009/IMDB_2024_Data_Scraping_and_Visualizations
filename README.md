# 🎬 IMDB 2024 Data Scraping and Visualizations

An interactive Streamlit dashboard that analyzes IMDB 2024 movie data, including ratings, genres, durations, and voting counts. Data is stored and managed with a MySQL database.

---
**1. Data Scraping and Storage**
    - Data Source: IMDb 2024 Movies page (link).
        Scraping Method: Use Selenium to extract the following fields:
        Movie Name
        Genre
        Ratings
        Voting Counts
        Duration
    - Genre-wise Storage: Save extracted data as individual CSV files for each genre.
    - Combine Data: Merge all genre-wise CSVs into a single DataFrame.
    - SQL Storage: Store the merged dataset into an SQL database for querying and future analysis.

## 📌 Features
**1. Top 10 Movies by Rating and Voting Counts:** Identify movies with the highest ratings and significant voting engagement.
**2.Genre Distribution:** Plot the count of movies for each genre in a bar chart.
**3.Average Duration by Genre:** Show the average movie duration per genre in a horizontal bar chart.
**4.Voting Trends by Genre:** Visualize average voting counts across different genres.
**5.Rating Distribution:** Display a histogram or boxplot of movie ratings.
**6.Genre-Based Rating Leaders:** Highlight the top-rated movie for each genre in a table.
**7.Most Popular Genres by Voting:**  Identify genres with the highest total voting counts in a pie chart.
**8.Duration Extremes:** Use a table or card display to show the shortest and longest movies.
**9.Ratings by Genre:** Use a heatmap to compare average ratings across genres.
**10.Correlation Analysis**: Analyze the relationship between ratings and voting counts using a scatter plot.
**Interactive Filtering Functionality**
  1.Allow users to filter the dataset based on the following criteria:
    Duration (Hrs): Filter movies based on their runtime (e.g., < 2 hrs, 2–3 hrs, > 3 hrs).
    Ratings: Filter movies based on IMDb ratings (e.g., > 8.0).
    Voting Counts: Filter based on the number of votes received (e.g., > 10,000 votes).
   Genre: Filter movies within specific genres (e.g., Action, Drama).
  2.Display the filtered results in a dynamic DataFrame within the Streamlit app.
  3.Combine filtering options so users can apply multiple filters simultaneously for customized insights

---

## 📂 Project Structure

```bash
IMDB_2024_Data_Scraping_and_Visualizations\env\Scripts
│
├── index.py                # Main Dashboard Page and other functionaliy
├── data_scraping.ipynb     # Data Scraping and Storage
├── action_genres.csv       # Action Geners csv file
├── adventure_genres.csv    # Adventure Genres csv file
├── comedy_genres.csv       # Comedy Genres csv file
├── crime_genres.csv        # Crime Genres csv file
├── thriller_genres.csv     # Thriller Genres csv file
├── imdb_db.sql             # Database table schema
README.md                # This file


**Requirement Details**
    Python 3.8+    
    MySQL     
    Streamlit    
    SQLAlchemy    
    Pandas    
    Seaborn / Matplotlib

**Installation**
1.git clone git@github.com:manikandanbe2009/IMDB-2024-Data-Scraping-and-Visualizations.git
2.Data Scraping and Storage
  use ipynb for data scraping and storage
  1.pip install selenium pandas
  2.Get Geners data and storage seperate name geners csv file
  3.combined the all csv into single Dataframe using Padas
  4. All Dataframe data storage to DB
  5. use imdb_db.sql create database and table  schema
3.Create and Activate a Virtual Environment
  python -m venv env
  Activate :  env-> scripts-> Activate.ps1 right click and  copy path and activate to terimal example (D:\AI-ML\Projects\IMDB_2024_Data_Scraping_and_Visualizations\env\Scripts\Activate.ps1)
4.Install Required Libraries
    pip install streamlit streamlit_option_menu sqlalchemy seaborn matplotlib pandas
5.Run Streamlit
  streamlit run index.py
