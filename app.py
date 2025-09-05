from flask import Flask, request, render_template
from textblob import TextBlob
import wikipedia

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def get_bot_response():
    user_text = request.args.get('msg')

    if not user_text:
        return "Please type something."

    # --- GREETING HANDLER ---
    greetings = ["hi", "hello", "hey", "salam", "assalamualaikum"]
    if user_text.lower().strip() in greetings:
        return "Hello! I'm Fusion AI. How can I help you today?"

    # --- "What is ..." Handler ---
    if user_text.lower().startswith("what is"):
        try:
            topic = user_text.lower().replace("what is", "").strip()
            if topic:
                result = wikipedia.summary(topic, sentences=1)
                return result
        except:
            return "Sorry, I couldn’t find information about that."

    # --- "Who is ..." Handler ---
    if user_text.lower().startswith("who is"):
        try:
            topic = user_text.lower().replace("who is", "").strip()
            if topic:
                result = wikipedia.summary(topic, sentences=1)
                return result
        except:
            return "Sorry, I couldn’t find information about that."

    # --- Wikipedia Lookup (for single words like 'lion') ---
    try:
        result = wikipedia.summary(user_text, sentences=1)
        return result
    except:
        pass

    # --- Sentiment Analysis (for opinions) ---
    blob = TextBlob(user_text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "That sounds positive!"
    elif sentiment < 0:
        return "That sounds negative!"
    else:
        return "Good question. Can you explain more?"

if __name__ == "__main__":
    app.run(debug=True)
