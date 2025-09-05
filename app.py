from flask import Flask, request, render_template
from textblob import TextBlob
import wikipedia
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import os
import json

app = Flask(__name__)

# -----------------------------
# File where chats are saved
# -----------------------------
DATA_FILE = "data.json"

# -----------------------------
# Load previous chats
# -----------------------------
def load_chats():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

# -----------------------------
# Save new chat to file
# -----------------------------
def save_chat(user_text, bot_text):
    data = load_chats()
    data.append({"user": user_text, "bot": bot_text})
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# -----------------------------
# Train model on saved chats
# -----------------------------
def train_model():
    data = load_chats()
    if not data:
        return None, None
    # Make sure each entry has "user" and "bot"
    X = [chat.get("user", "") for chat in data]
    y = [chat.get("bot", "") for chat in data]
    vectorizer = CountVectorizer()
    X_vect = vectorizer.fit_transform(X)
    model = MultinomialNB()
    model.fit(X_vect, y)
    return model, vectorizer

# -----------------------------
# Pre-filled knowledge base
# -----------------------------
PRE_FILLED_KNOWLEDGE = {
    "who is babar azam": "Babar Azam is a Pakistani cricketer and former captain of the national team.",
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

    # --- GREETING HANDLER ---
    greetings = ["hi", "hello", "hey", "salam", "assalamualaikum"]
    if user_lower in greetings:
        return "Hello! I'm Fusion AI. How can I help you today?"

    # --- Check pre-filled knowledge ---
    if user_lower in PRE_FILLED_KNOWLEDGE:
        return PRE_FILLED_KNOWLEDGE[user_lower]

    # --- "What is ..." Handler ---
    if user_lower.startswith("what is"):
        try:
            topic = user_lower.replace("what is", "").strip()
            if topic:
                result = wikipedia.summary(topic, sentences=3)  # <-- fetch 3 sentences
                save_chat(user_text, result)
                return result
        except:
            return "Sorry, I couldn’t find information about that."

    # --- "Who is ..." Handler ---
    if user_lower.startswith("who is"):
        try:
            topic = user_lower.replace("who is", "").strip()
            if topic:
                result = wikipedia.summary(topic, sentences=3)  # <-- fetch 3 sentences
                save_chat(user_text, result)
                return result
        except:
            return "Sorry, I couldn’t find information about that."

    # --- Wikipedia Lookup (for single words or unknown phrases) ---
    try:
        result = wikipedia.summary(user_text, sentences=3)
        save_chat(user_text, result)
        return result
    except:
        pass

    # --- Sentiment Analysis ---
    blob = TextBlob(user_text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        bot_response = "That sounds positive!"
    elif sentiment < 0:
        bot_response = "That sounds negative!"
    else:
        bot_response = "Good question. Can you explain more?"

    # --- Save chat & learn from previous chats ---
    save_chat(user_text, bot_response)
    model, vectorizer = train_model()
    if model and vectorizer:
        X_test = vectorizer.transform([user_text])
        bot_response = model.predict(X_test)[0]
        save_chat(user_text, bot_response)

    return bot_response

# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
