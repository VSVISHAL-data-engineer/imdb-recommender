from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome()
driver.get("https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31")
time.sleep(4)

for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

movie_items = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
print(f"Found {len(movie_items)} movies")

movies = []
storylines = []

for item in movie_items:
    try:
        title = item.find_element(By.CSS_SELECTOR, ".dli-title").text
        title = title.split(". ", 1)[-1] if ". " in title else title
    except:
        continue

    storyline = ""
    try:
        storyline = item.find_element(By.CSS_SELECTOR, "div.ipc-html-content-inner-div").text
    except:
        storyline = ""

    movies.append(title)
    storylines.append(storyline)

driver.quit()

df = pd.DataFrame({"Movie Name": movies, "Storyline": storylines})
df = df[df["Movie Name"].str.strip() != ""]
df.to_csv("imdb_2024_movies.csv", index=False)
print(f"Saved {len(df)} movies to imdb_2024_movies.csv")
print(df.head(10))