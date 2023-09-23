import requests
from bs4 import BeautifulSoup
import re
import random
import pandas as pd
from twilio.rest import Client
import sys
import csv
import os
import schedule


# Initializing urls and headers - To mask bot like activities

useragents=['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4894.117 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4855.118 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4892.86 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4854.191 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4859.153 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36/null',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36,gzip(gfe)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4895.86 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4860.89 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4885.173 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4864.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4877.207 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4872.118 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4876.128 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36']

# Add your sharable Amazon wishlist link here

target_url='https://www.amazon.in/hz/wishlist/ls/3NYBKPPBJ3XBL?ref_=wl_share'

headers={"User-Agent":useragents[random.randint(0,31)],"accept-language": "en-US,en;q=0.9","accept-encoding": "gzip, deflate, br","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}


def get_prod_info(soup):
    product_list = soup.find_all('h2',{'class':'a-size-base'})
    price_list = soup.find_all('span',{'class':'a-price'})
    return product_list, price_list

def fetch_latest_data(target_url, headers):
    resp = requests.get(target_url,headers=headers)
    soup = BeautifulSoup(resp.text,'html.parser')
    products, prices = get_prod_info(soup)
    return products, prices


# initialize price_tracker file

def write_init_data():
    products, prices = fetch_latest_data(target_url, headers)
    with open('price_tracker.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['id','product_name', 'initial_price', 'current_low', 'current', 'offer', 'url'])

        for x in range(len(products)):
            id = int(x+1)
            product_name = products[x].find('a').text.lstrip().rstrip()
            initial_price = int(prices[x].find('span').text.replace(',', '').replace('₹', '').replace('.00', ''))
            current_low = int(prices[x].find('span').text.replace(',', '').replace('₹', '').replace('.00', ''))
            current = int(prices[x].find('span').text.replace(',', '').replace('₹', '').replace('.00', ''))
            offer = (((int(initial_price))-(int(current)))/int(initial_price))*100
            url = 'https://amazon.in'+products[x].find('a')['href'].split('?')[0]
            writer.writerow([id, product_name, initial_price, current_low, current, offer, url])
            print(id, product_name, initial_price, current_low, current, offer, url)


# check for price drop and update csv

def fetch_current_price():
    id = []
    price_parsed = []
    products, prices = fetch_latest_data(target_url, headers)
    for x in range(len(products)):
        id.append(x+1)
        price_parsed.append(int(prices[x].find('span').text.replace(',', '').replace('₹', '').replace('.00', '')))
    data = {'id': id, 'new_price': price_parsed}
    # print(data)
    df2 = pd.DataFrame(data)
    df = pd.read_csv('price_tracker.csv')
    
    #joining old data with new data
    df = df.merge(df2, on='id', how='left')
    
    # Updating current low
    df.loc[df['current_low'] > df['new_price'], 'current_low'] = df['new_price']
    
    # Updating current price
    df['current']=df['new_price']
    
    # Calculate 'offer' column
    df['offer'] = ((df['initial_price'] - df['current']) / df['initial_price']) * 100
    
    # Drop 'new_price' column
    df = df.drop(columns=['new_price'])
    df.to_csv('price_tracker.csv', index=False)
    print(df)


def generate_msg_content(offers):
    # Initialize an empty list to store the sentences
    sentences = ""

    # Loop through each row in the DataFrame
    for index, row in offers.iterrows():
        # Generate a sentence from the row
        sentence = f"'{row['product_name']}' is now selling for ₹{row['current']}. The price is {row['offer']}% off and the lowest price recorded is ₹{row['current_low']}. {row['url']}.\n\n"
        
        # Add the sentence to the list
        sentences+=sentence

    print(sentences)
    return sentences


def send_msg(content):
    account_sid = ['TWILIO_ACCOUNT_SID']
    auth_token = ['TWILIO_AUTH_TOKEN']

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=content,
        to=['YOUR_WHATSAPP_NUMBER']
    )

    return message.sid


def check_file_exists(file_path):
    return os.path.isfile(file_path)


# Send notification if any of the items has more than 8% drop in price

def send_offer_notifications():
    df = pd.read_csv('master_data.csv')
    discounts = df[df['offer'] > 8]
    if discounts.empty:
        print("No offers yet")
    else:
        content = generate_msg_content(discounts)
        response = send_msg(content)
        print(response)


def main():
    if check_file_exists("master_data.csv"):
        print("Updating prices...")
        fetch_current_price()
        send_offer_notifications()
    else:
        write_init_data()
        print('File initialized!')
    

schedule.every().hour.do(main)

while True:
    schedule.run_pending()
