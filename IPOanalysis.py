import requests
import fitz  # PyMuPDF for PDF extraction
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import re


# Function to extract text from PDF document
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


# Function to search for financial keywords in document
def search_keywords(text, keywords):
    found = {}
    for keyword in keywords:
        matches = re.findall(rf"\b{keyword}\b", text, re.IGNORECASE)
        found[keyword] = len(matches)
    return found


# Function to get news sentiment using NewsAPI
def get_news_sentiment(query):
    api_key = "6f83f736660a419bb76d73249e58b264"  # Replace with your NewsAPI key
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url)
    articles = response.json().get("articles", [])

    headlines = [article["title"] for article in articles]
    sentiments = [TextBlob(headline).sentiment.polarity for headline in headlines]

    avg_sentiment = np.mean(sentiments) if sentiments else 0
    return avg_sentiment


# Analyze probability of profitability based on document data and sentiment
def analyze_profitability(document_path, ipo_name):
    # Step 1: Extract and analyze document
    keywords = ['revenue', 'growth', 'debt', 'profit', 'competitive']
    document_text = extract_text_from_pdf(document_path)
    keyword_counts = search_keywords(document_text, keywords)

    # Step 2: Get sentiment score for recent news
    news_sentiment = get_news_sentiment(ipo_name)

    # Step 3: Compile data into a DataFrame
    data = pd.DataFrame(list(keyword_counts.items()), columns=['Keyword', 'Count'])
    data['Sentiment'] = news_sentiment
    data['Impact'] = data['Count'] * (1 + data['Sentiment'])

    # Step 4: Visualization
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Keyword', y='Impact', data=data, palette='viridis')
    plt.title(f"Impact Score Analysis for IPO: {ipo_name}")
    plt.xlabel('Financial Factor')
    plt.ylabel('Impact Score')
    plt.show()

    # Simple conclusion (based on arbitrary thresholds)
    avg_impact = data['Impact'].mean()
    if avg_impact > 10:
        print("IPO has a high potential for profitability.")
    else:
        print("IPO might be risky or less profitable.")

# Example usage:
document_path = 'C:\\Users\\shrav\\Downloads\\Sagility India Limited Prospectus.pdf'
ipo_name = 'Sagility India Limited'
analyze_profitability(document_path, ipo_name)
