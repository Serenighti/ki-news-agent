import anthropic, requests, os
from datetime import datetime

def fetch_news():
    api_key = os.environ.get("NEWS_API_KEY")
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "artificial intelligence OR AI",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": api_key
    }
    response = requests.get(url, params=params)
    articles = response.json().get("articles", [])
    result = []
    for a in articles:
        result.append(f"- {a['title']}: {a.get('description', '')} | LINK: {a.get('url', '')}")
    return "\n".join(result)

def summarize(news_text):
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""
Heute ist der {datetime.now().strftime('%d.%m.%Y')}.
Hier sind aktuelle KI-News-Schlagzeilen:

{news_text}

Bitte:
- Wähle die 5 interessantesten aus
- Erkläre jede in 2-3 einfachen Sätzen auf Deutsch
- Schreibe einen kurzen, freundlichen Intro-Satz
- Schreibe am Ende jeder Zusammenfassung den Link zum Artikel
"""
        }]
    )
    return response.content[0].text

def send_telegram(text):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text}
    )

print("1. News sammeln...")
news = fetch_news()

print("2. Claude fasst zusammen...")
summary = summarize(news)

print("3. Telegram-Nachricht senden...")
send_telegram(summary)

print("Fertig!")
