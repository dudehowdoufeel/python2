import pandas as pd
import matplotlib.pyplot as plt

a = r"C:/Users/ASUS/Desktop/python2/hw9/netflix_titles.csv"
df = pd.read_csv(a)

#vse  
total_movies = df[df['type'] == 'Movie'].shape[0]
total_shows = df[df['type'] == 'TV Show'].shape[0]

#zhanry
genres = df['listed_in'].str.split(',', expand=True).stack().str.strip()
most_common_genres = genres.value_counts()

print(f"total number of movies: {total_movies}")
print(f"total number of TV shows: {total_shows}")
print("\nmost common genres:")
print(most_common_genres.head())

# klining
missing_values = df.isnull().sum()
print("\nMissing values in each column:")
print(missing_values)

#cast pustymi strokami
df['cast'].fillna('', inplace=True)

# udalit stranu i god vypuska
df.dropna(subset=['release_year', 'country'], inplace=True)

#proverka
missing_values_after = df.isnull().sum()
print("\nMissing values after cleaning:")
print(missing_values_after)

release_year_count = df['release_year'].value_counts().sort_index()

#graphik
plt.figure(figsize=(14, 8))
release_year_count.plot(kind='bar', color='skyblue')
plt.title('num of movies and TV shows released each year')
plt.xlabel('year')
plt.ylabel('count')
plt.xticks(rotation=90)
plt.tight_layout()

#soxr
chart_path = r'C:\Users\ASUS\Desktop\python2\hw9\graphik.png'
plt.savefig(chart_path)
plt.show()
print(f"\nChart saved to {chart_path}")

#samyi popularnyi zhar
most_common_genre = most_common_genres.idxmax()
print(f"\nThe most frequent genre in the dataset is: {most_common_genre}")

recent_years = release_year_count.tail(10)
print("\nRecent years and the number of shows released:")
print(recent_years)

#soxr
cleaned_data_path = r"C:\Users\ASUS\Desktop\python2\hw9\cleanedNetflix_data.csv"
df.to_csv(cleaned_data_path, index=False)
print(f"\nCleaned data saved to {cleaned_data_path}")

summary = f"""
The most popular genre on Netflix is **'{most_common_genre}'**, which shows how much people love this type of content.

In the last 10 years, Netflix has been making more and more movies and TV shows. Here's how many were released each year recently:
{recent_years.to_string()}

It's cool to see how Netflix is growing and giving us so much new content to enjoy!
"""


summary_path = r"C:\Users\ASUS\Desktop\python2\hw9\summary2.txt"
with open(summary_path, "w", encoding="utf-8") as file:
    file.write(summary)
print(f"\nSummary saved to {summary_path}")
