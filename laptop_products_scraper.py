import smtplib
import requests
from bs4 import BeautifulSoup
import time
import getpass
import pandas as pd
import getpass


# Email id of the sender
sender = 'your_email@gmail.com'

# Email id of receiver (user to be notified)
receiver = '''Receiver email address'''

password = getpass.getpass('Enter your account password: ')  # sender's email password

budget = float(input('Your budget? '))

# Products page url
url = 'https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.dedicated_graphics_memory%255B%255D%3D4%2BGB&p%5B%5D=facets.processor%255B%255D%3DCore%2Bi5&p%5B%5D=facets.storage_type%255B%255D%3DSSD'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

product_titles = soup.find_all('div', class_='_3wU53n')
product_prices = soup.find_all('div', class_='_1vC4OE _2rQ-NK')
product_links = soup.find_all('a', class_='_31qSD5')

# To check price and title for single product
# print(product_titles[1])
# print(product_prices[1])
# print(url+product_links[1]['href'])

# lists to store prices and product info
titles = []
prices = []
links = []


for i in range(len(product_prices)):

    title = product_titles[i].get_text()
    titles.append(title)
    price = float(product_prices[i].get_text()[1:].replace(',', ''))
    prices.append(price)
    link = product_links[i]['href']
    links.append(link)

# list of prices and titles
# print(titles)
# print(prices)
# print(links)

selected_products = []

for x in range(len(prices)):

    if prices[x] <= budget:
        selected_products.append(x)


print('These are the laptops in your budget ')

# body of email to be written
body = ''

selected_titles = []
selected_prices = []
selected_links = []

for selected in selected_products:

     info1 = titles[selected]
     selected_titles.append(info1)
     info2 = str(prices[selected])
     selected_prices.append(info2)
     info3 = url+links[selected]
     selected_links.append(info3)
     body = body + '\n' + info1 + '\n' + 'Price: ' + info2 + '\n' + info3


print(selected_titles)
print(selected_prices)
print(selected_links)
# print(body)

# Storing data into a file
df = pd.DataFrame({'Product Info': selected_titles, 'Price': selected_prices})
df.to_csv('products.csv', index=False, encoding='utf-8')


def send_mail(body):

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(sender, password)

    print('Login Success')

    subject = 'Prices dropped!! Last Day of SALE!'
    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(sender, receiver, msg)
    print('Email has been sent to ', receiver)

    server.quit()


send_mail(body)

'''If you want to send mail timely... then use the below loop
while (True):
    send_mail(body)
    time.sleep(3600) # since sleep is 3600 seconds... a mail will be send after every hour.
'''
