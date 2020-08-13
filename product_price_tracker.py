import smtplib
import requests
from bs4 import BeautifulSoup
import time

sender = 'your_email@gmail.com'
receiver = '''Receiver email address'''

password = input('Enter your password: ')  # sender's email password

# url of the product page which is to be tracked
url = 'https://www.flipkart.com/acer-aspire-7-core-i5-9th-gen-8-gb-512-gb-ssd-windows-10-home-4-graphics-nvidia-geforce-gtx-1650-a715-75g-50sa-gaming-laptop/p/itmff1cbf710ce62?pid=COMFR6AANWZVZM8Y&lid=LSTCOMFR6AANWZVZM8YICAJ6Z&marketplace=FLIPKART&srno=s_1_1&otracker=search&otracker1=search&fm=SEARCH&iid=c34f11d5-4272-498b-9bbb-eed8fe8f6aea.COMFR6AANWZVZM8Y.SEARCH&ppt=sp&ppn=sp&ssid=wbcdwsvznk0000001597055865745&qH=312f91285e048e09'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}


def check_price():

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find('span', class_='_35KyD6').get_text()
    price = soup.find('div', class_='_1vC4OE _3qQ9m1').get_text()[1:].replace(',', '')
    final_price = float(price)

    if final_price <= 57000:
        send_mail()

    print(title)
    print(final_price)


def send_mail():

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(sender, password)

    print('Login Success')

    subject = 'Prices dropped!! Last Day of SALE!'
    body = 'Please check the link below ' \
           'https://www.flipkart.com/acer-aspire-7-core-i5-9th-gen-8-gb-512-gb-ssd-windows-10-home-4-graphics-nvidia-geforce-gtx-1650-a715-75g-50sa-gaming-laptop/p/itmff1cbf710ce62?pid=COMFR6AANWZVZM8Y&lid=LSTCOMFR6AANWZVZM8YICAJ6Z&marketplace=FLIPKART&srno=s_1_1&otracker=search&otracker1=search&fm=SEARCH&iid=c34f11d5-4272-498b-9bbb-eed8fe8f6aea.COMFR6AANWZVZM8Y.SEARCH&ppt=sp&ppn=sp&ssid=wbcdwsvznk0000001597055865745&qH=312f91285e048e09'
    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(sender, receiver, msg)
    print('Email has been sent to ', receiver)

    server.quit()


check_price()

'''If you want to send mail timely... then use the below loop
while (True):
    check_price()
    time.sleep(3600) # since sleep is 3600 seconds... a mail will be send after every hour.
'''