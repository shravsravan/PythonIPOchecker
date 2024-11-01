import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import re
from docx import Document
from bs4 import BeautifulSoup
import moneycontrol

# Function to extract text from PDF document
def extract_text_from_pdf(pdf_path):
    from PyPDF2 import PdfReader

    text = ""
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to search for financial keywords in document
def search_keywords(text, keywords):
    keyword_counts = {}
    for keyword in keywords:
        keyword_counts[keyword] = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE))
    return keyword_counts

# Function to get news sentiment using NewsAPI
def get_news_sentiment(query):
    api_key = "YOUR_NEWSAPI_KEY"  # Replace with your NewsAPI key
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url)
    articles = response.json().get('articles', [])
    sentiment_score = 0

    for article in articles:
        analysis = TextBlob(article['title'])
        sentiment_score += analysis.sentiment.polarity

    return sentiment_score / len(articles) if articles else 0

# Function to fetch data from Screener.in
def fetch_screener_data(stock_name):
    url = f"https://www.screener.in/company/{stock_name}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = {}

    try:
        price = soup.find('div', class_='value').text  # Adjust class name based on actual HTML
        market_cap = soup.find('div', class_='market-cap').text  # Adjust class name based on actual HTML
        data['Price'] = price
        data['Market Cap'] = market_cap
    except AttributeError:
        print(f"Error fetching data from Screener.in for {stock_name}")

    return data

# Function to fetch data from Moneycontrol API
class Moneycontrol:
    pass


def fetch_moneycontrol_data(stock_name):
    mc = Moneycontrol()
    try:
        stock_data = mc.get_quote(stock_name)
        data = {
            'Price': stock_data['lastPrice'],
            'P/E Ratio': stock_data['pe'],
            'Market Cap': stock_data['marketCap']
        }
        return data
    except Exception as e:
        print(f"Error fetching data from Moneycontrol: {e}")
        return {}

# Function to fetch company info using Alpha Vantage
def fetch_company_info(ipo_name):
    search_url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ipo_name}&apikey=YOUR_ALPHA_VANTAGE_API_KEY"
    response = requests.get(search_url)
    data = response.json()

    if 'bestMatches' in data and len(data['bestMatches']) > 0:
        best_match = data['bestMatches'][0]
        ticker = best_match['1. symbol']
        sector = best_match['3. sector']
        return ticker, sector
    else:
        print("No ticker found for the specified company.")
        return None, None

# Function to fetch nearest competitor (basic implementation)
def fetch_nearest_competitor(ticker, sector):
    # Placeholder for actual implementation
    # This should return a list of competitors based on the sector
    return ["Competitor A", "Competitor B"]

# Main analysis function
def analyze_profitability(document_path, ipo_name):
    # Step 1: Extract and analyze document
    keywords = ['revenue', 'growth', 'debt', 'profit', 'competitive', 'cash flow', 'risk']
    document_text = extract_text_from_pdf(document_path)
    keyword_counts = search_keywords(document_text, keywords)

    # Step 2: Get sentiment score for recent news
    news_sentiment = get_news_sentiment(ipo_name)

    # Step 3: Fetch stock data
    ticker, sector = fetch_company_info(ipo_name)
    if ticker is None:
        print("Unable to proceed as no ticker was found.")
        return

    screener_data = fetch_screener_data(ticker)
    moneycontrol_data = fetch_moneycontrol_data(ticker)

    # Display fetched data
    print(f"Screener.in Data: {screener_data}")
    print(f"Moneycontrol Data: {moneycontrol_data}")

    # Step 4: Analyze competitors and fetch nearest competitor data
    competitors = fetch_nearest_competitor(ticker, sector)
    print(f"Nearest Competitors: {competitors}")

    # Additional analysis can be performed here
    # You can visualize data, create reports, etc.

# Example usage
document_path = "C:\\Users\\shrav\\Downloads\\Swiggy Limited Prospectus.pdf"  # Replace with your PDF document path
ipo_name = "Swiggy Limited"  # Replace with the IPO name you are analyzing
analyze_profitability(document_path, ipo_name)
