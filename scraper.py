import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url = 'https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page='

pages = [i for i in range(1, 11)]

urls = []

for page in pages:
    final_link = url+str(page)
    urls.append(final_link)

# print(urls)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}

# lists to store prices and product info
titles = []
prices = []
ratings = []

for url in urls:
    page = requests.get(url, headers=headers)
    time.sleep(3)
    soup = BeautifulSoup(page.content, 'html.parser')

    product_titles = soup.find_all('div', class_='_3wU53n')
    product_prices = soup.find_all('div', class_='_1vC4OE _2rQ-NK')
    product_ratings = soup.find_all('div', class_='hGSR34')

    for i in range(len(product_prices)):
        title = product_titles[i].get_text()
        titles.append(title)
        price = float(product_prices[i].get_text()[1:].replace(',', ''))
        prices.append(price)
        rating = float(product_ratings[i].get_text())
        ratings.append(rating)


# list of prices, titles and ratings
# print(titles)
# print(prices)
# print(ratings)

# Storing data into a file
df = pd.DataFrame({'Laptop Name': titles, 'Price': prices, 'Ratings': ratings})
df.to_csv('laptops.csv', index=False, encoding='utf-8')