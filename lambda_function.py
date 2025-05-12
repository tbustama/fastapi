import os
import boto3
import yfinance as yf
import google.generativeai as genai

# ENV VARS (Set in Lambda Environment Variables)
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']
# NEWS_API_KEY = os.environ['NEWS_API_KEY']
SES_EMAIL_FROM = os.environ['SES_EMAIL_FROM']
SES_EMAIL_TO = os.environ['SES_EMAIL_TO']

# Set OpenAI key
# --- Configuration ---
# Option 1: Configure API key directly in the script (NOT RECOMMENDED for production)
# Replace "YOUR_API_KEY" with your actual API key.
# genai.configure(api_key="YOUR_API_KEY")

# Option 2: Load API key from an environment variable (RECOMMENDED)
# Make sure you have an environment variable named GOOGLE_API_KEY set with your API key.
try:
    api_key = GEMINI_API_KEY
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
except ValueError as e:
    print(f"Error: {e}")
    print("Please set the GOOGLE_API_KEY environment variable or configure the API key directly in the script.")
    exit()
    
# --- Select a Model ---
# List available models (optional, for informational purposes)
# print("Available models:")
# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

# Choose a model. For text generation, 'gemini-pro' or 'gemini-1.5-flash' are common choices.
# 'gemini-1.5-flash' is often faster and more cost-effective for simpler tasks.
model_name = "gemini-2.0-flash" # Or "gemini-pro"

try:
    model = genai.GenerativeModel(model_name)
except Exception as e:
    print(f"Error creating model: {e}")
    exit()


def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    current_price = stock.info.get('regularMarketPrice')
    pe_ratio = stock.info.get('trailingPE', 'N/A')
    ma_200 = hist['Close'].rolling(window=200).mean().iloc[-1]
    return {
        "ticker": ticker,
        "current_price": current_price,
        "pe_ratio": pe_ratio,
        "ma_200": ma_200
    }

# def get_news(ticker):
#     url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
#     response = requests.get(url)
#     if response.status_code != 200:
#         return ["Failed to retrieve news."]
#     articles = response.json().get("articles", [])
#     return [a['title'] for a in articles]

def analyze_stock_with_llm(data, news):
    prompt = f"""
Analyze {data['ticker']} with the following info:
- Current Price: {data['current_price']}
- PE Ratio: {data['pe_ratio']}
- 200-day Moving Average: {data['ma_200']}
- Recent News: {', '.join(news)}

Would you recommend buying this stock today? Keep your answer concise and informative.
"""
    response = model.generate_content(prompt)
    return response

def send_email(subject, body):
    client = boto3.client('ses', region_name='us-east-1')  # or your region
    response = client.send_email(
        Source=SES_EMAIL_FROM,
        Destination={'ToAddresses': [SES_EMAIL_TO]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )
    return response

def lambda_handler(event, context):
    tickers = ['AMZN', 'TSLA', 'SQ']
    summaries = []

    for ticker in tickers:
        data = get_stock_data(ticker)
    #     # news = get_news(ticker)
        advice = analyze_stock_with_llm(data, '')
        summaries.append(f"📈 {ticker}:\n{advice}\n")
    final_summary = "\n\n".join(summaries)
    send_email("📊 Morning Stock Report", final_summary)
    return {"statusCode": 200,  "headers": {
        "Access-Control-Allow-Origin": "*",  # or a specific domain
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    },"body": "Email sent successfully"}
