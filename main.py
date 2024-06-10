import requests
from datetime import datetime, timedelta
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
Api_key = "NLKW7ZOMDO6X884T"
Api_key_news = "f718b7d85219498bbcb51e14069d6b05"

todays_date = datetime.now()
yesterday = todays_date - timedelta(1)

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": Api_key

}
stock_price = requests.get(url="https://www.alphavantage.co/query", params=stock_parameters)
stock_price.raise_for_status()
price_data = stock_price.json()

key_list = list(price_data["Time Series (Daily)"].keys())
first_day_data = price_data["Time Series (Daily)"][key_list[0]]
next_day_data = price_data["Time Series (Daily)"][key_list[1]]
print(first_day_data)
print(next_day_data)

diff_of_price = round(float(first_day_data["4. close"]) - float(next_day_data["4. close"]), 2)
print(diff_of_price)


def persentage(diff_of_data):
    pers = (diff_of_data / float(first_day_data["4. close"]) * 100)
    return round(pers, 2)


print(persentage(diff_of_price))

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
stock_news_parameters = {
    "q": COMPANY_NAME,
    "from": yesterday.date(),
    "sortBy": "publishedAt",
    "apikey": Api_key_news
}
stock_price_news = requests.get(url="https://newsapi.org/v2/everything", params=stock_news_parameters)
stock_price_news.raise_for_status()
price_data_news = stock_price_news.json()
print(price_data_news["articles"][0])
news_data = price_data_news["articles"][0]

if diff_of_price > 0 :
    value = persentage(diff_of_price)
    message_to_send = f"TSLA: 🔺{value}% \nHeadline: {news_data['title']}.\nBrief: {news_data['description']}"

else:
    value = persentage(diff_of_price * -1)
    message_to_send = f"TSLA: 🔻{value}% \nHeadline: {news_data['title']}.\nBrief: {news_data['description']}"




## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

account_sid = "AC14ef306a1dc024239c0ed5cb51dc64e3"
auth_token = "92d61dae586903a0d96d8e4fae167b02"

client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         from_='+14697122002',
         body=message_to_send,
         to='+918329069224'
     )
print(message_to_send)



# Optional: Format the SMS message like this:
"""TSLA: 🔺2% 
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have 
gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings 
show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash. 
or 
"TSLA: 🔻5% 
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F 
filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus 
market crash."""
