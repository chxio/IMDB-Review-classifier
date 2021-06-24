from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np

#movie_name = "Source code (2011)"
print("Enter the name of the movie : ")
print("example : The Tree of Life (2011)")
print("\n \n")
movie_name = input()


driver = webdriver.Chrome(r"--chromedriver path--")
time.sleep(3)
driver.maximize_window()
time.sleep(3)


driver.get("https://www.imdb.com/")
time.sleep(3)


driver.find_element(By.XPATH, "//*[@id='suggestion-search']").click()
time.sleep(3)
driver.find_element(By.XPATH, "//*[@id='suggestion-search']").send_keys(movie_name)
time.sleep(3)


driver.find_element(By.XPATH, "//*[@id='suggestion-search-button']").click()
time.sleep(3)

driver.find_element(By.XPATH, "//*[@id='findSubHeader']/a[1]").click()
time.sleep(3)

driver.find_element(By.XPATH, "//*[@id='main']/div/div[2]/table/tbody/tr[1]/td[2]/a").click()
time.sleep(3)


from selenium.common.exceptions import NoSuchElementException
try:
    driver.find_element(By.XPATH, "//*[@id='quicklinksMainSection']/a[3]").click()
except NoSuchElementException:
    driver.find_element(By.XPATH, "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[2]/div/div[2]/ul/li[2]/a").click()
#//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div/div[2]/ul/li[2]/a
time.sleep(3)

for i in range(10):
    driver.find_element(By.XPATH, "//*[@id='load-more-trigger']").click()
    time.sleep(3)
#time.sleep(3)

#Scrap IMBD review
ans = driver.current_url
page = requests.get(ans,verify=False)
soup = BeautifulSoup(page.content, "html.parser")
all = soup.find(id="main")

#Get the title of the movie
all = soup.find(id="main")
parent = all.find(class_ ="parent")
name = parent.find(itemprop = "name")
url = name.find(itemprop = 'url')
film_title = url.get_text()

#Get the title of the review
title_rev = all.select(".title")
title = [t.get_text().replace("\n", "") for t in title_rev]

#Get the review
review_rev = all.select(".content .text")
review = [r.get_text() for r in review_rev]

#Make it into dataframe
table_review = pd.DataFrame({
    "Title" : title,
    "Review" : review
})



table_review

#Sentiment Analysis

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import time

#Vadersentiment
analyser = SentimentIntensityAnalyzer()
sentiment1 = []
sentiment2 = []

for rev in review:
    score1 = analyser.polarity_scores(rev)
    com_score = score1.get('compound')
    if com_score  >= 0.05:
        sentiment1.append('positive')
    elif com_score > -0.05 and com_score < 0.05:
        sentiment1.append('neutral')
    elif com_score <= -0.05:
        sentiment1.append('negative')

table_review['Sentiment Vader'] = sentiment1

#TextBlob
for rev in review:
    score2 = TextBlob(rev).sentiment.polarity
    if score2 >= 0:
        sentiment2.append('positive')
    else:
        sentiment2.append('negative')
print(f"The movie title is {film_title}")
print("We analyzed 25 top reviews from IMDB")
print("")
print("According to vadersentiemnt, you should :")
if sentiment1.count('positive') > sentiment1.count('negative'):
    print('WATCH IT!')
else:
    print("NOT WATCH IT...")
print('Positive : ', sentiment1.count('positive'))
print('Negative : ', sentiment1.count('negative'))
print("")
print("According to TextBlob, you should :")
if sentiment2.count('positive') > sentiment2.count('negative'):
    print('WATCH IT!')
else:
    print("NOT WATCH IT...")
print('Positive : ', sentiment2.count('positive'))
print('Negative : ', sentiment2.count('negative'))

#Close the browser
driver.close()
