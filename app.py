from flask import Flask, render_template, request
import requests
import wikipedia
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import os
import json
import re

# Optional: sympy for safer math evaluation
try:
    import sympy as sp
except Exception:
    sp = None

app = Flask(__name__)

# -----------------------------
# NewsAPI setup
# -----------------------------
api_key = "7d1051d0b33f47899aeccedcc6c98b39"
def get_news(category=None, country="us"):
    try:
        url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"
        if category:
            url += f"&category={category}"

        response = requests.get(url)
        data = response.json()

        if data['status'] != 'ok':
            return "Sorry, I couldn't fetch news at the moment."

        articles = data.get('articles', [])
        if not articles:
            return "No news found for this category."

        headlines = ""
        for i, article in enumerate(articles[:5], 1):
            headlines += f"{i}. {article['title']} ({article['source']['name']})\n"

        return headlines

    except Exception as e:
        return f"Error fetching news: {e}"

# -----------------------------
# Math solver
# -----------------------------
def try_solve_math(expr: str):
    s = expr.strip().replace('^', '**')
    # allow digits, operators, parentheses, decimals, and spaces
    if not re.match(r'^[0-9\.\s\+\-\*\/\^\(\)]+$', s):
        raise ValueError("Not a safe math expression")
    if sp:
        try:
            r = sp.sympify(s)
            if getattr(r, "is_number", False):
                return str(r)
        except:
            raise
    else:
        try:
            return str(eval(s, {"__builtins__": None}, {}))
        except:
            raise

# -----------------------------
# Chat data & model
# -----------------------------
DATA_FILE = "data.json"

def load_chats():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_chat(user_text, bot_text):
    data = load_chats()
    data.append({"user": user_text, "bot": bot_text})
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def train_model():
    data = load_chats()
    if not data:
        return None, None
    X = [chat.get("user", "") for chat in data]
    y = [chat.get("bot", "") for chat in data]
    vectorizer = CountVectorizer()
    X_vect = vectorizer.fit_transform(X)
    model = MultinomialNB()
    model.fit(X_vect, y)
    return model, vectorizer

PRE_FILLED_KNOWLEDGE = {
    "who is babar azam": "Babar Azam is a Pakistani cricketer and captain of the national team.",
    "what is ai": "AI stands for Artificial Intelligence, which allows machines to perform tasks that normally require human intelligence.",
    "who is elon musk": "Elon Musk is the CEO of Tesla and SpaceX.",
    "capital of pakistan": "Islamabad is the capital of Pakistan."
}

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def get_bot_response():
    user_text = request.args.get('msg')
    if not user_text:
        return "Please type something."

    user_lower = user_text.lower().strip()

    # --- NEWS HANDLER ---
    if "news" in user_lower:
        if "sports" in user_lower:
            return get_news("sports")
        elif "technology" in user_lower:
            return get_news("technology")
        else:
            return get_news()

    # --- ARITHMETIC HANDLER ---
    try:
        result = try_solve_math(user_text)
        return result
    except ValueError:
        pass

    # --- GREETINGS ---
    greetings = ["hi", "hello", "hey", "salam", "assalamualaikum"]
    if user_lower in greetings:
        return "Hello! I'm Fusion AI. How can I help you today?"

    # --- Pre-filled knowledge ---
    if user_lower in PRE_FILLED_KNOWLEDGE:
        return PRE_FILLED_KNOWLEDGE[user_lower]

    # --- Wikipedia Queries ---
    if user_lower.startswith("who is") or user_lower.startswith("what is") or len(user_lower.split()) <= 4:
        try:
            topic = user_lower.replace("who is", "").replace("what is", "").strip()
            if topic:
                result = wikipedia.summary(topic, sentences=4)
                save_chat(user_text, result)
                return result
        except wikipedia.exceptions.DisambiguationError as e:
            return f"This topic is ambiguous. Did you mean: {e.options[:5]}?"
        except:
            return "Sorry, I couldn’t find information about that."

    # --- Sentiment-based fallback ---
    blob = TextBlob(user_text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        bot_response = "That sounds positive!"
    elif sentiment < 0:
        bot_response = "That sounds negative!"
    else:
        bot_response = "Good question. Can you explain more?"

    # --- Save chat & train model ---
    save_chat(user_text, bot_response)
    model, vectorizer = train_model()
    if model and vectorizer:
        X_test = vectorizer.transform([user_text])
        bot_response = model.predict(X_test)[0]
        save_chat(user_text, bot_response)

    return bot_response

# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
