from flask import Flask, render_template, request, Response
import requests, wikipedia, os, json, re, string
from responses import CONVERSATION_KEYWORDS
from deep_translator import GoogleTranslator
from geometry_solver import *

try:
    import sympy as sp
except:
    sp = None

app = Flask(__name__)

user_language = "en"
DATA_FILE = "data.json"
api_key = "7d1051d0b33f47899aeccedcc6c98b39"

# ---------------- Utility Functions ----------------
def save_chat(user_text, bot_text):
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try: data = json.load(f)
            except: data = []
    data.append({"user": user_text, "bot": bot_text})
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def respond(keyword):
    global user_language
    keyword_norm = keyword.lower().translate(str.maketrans('', '', string.punctuation))
    if keyword_norm in CONVERSATION_KEYWORDS:
        return CONVERSATION_KEYWORDS[keyword_norm][user_language]
    else:
        return "Sorry, I didn't understand that." if user_language=="en" else "معاف کریں، میں نے یہ نہیں سمجھا۔"

def translate_to_urdu(text):
    if user_language == "ur":
        try: return GoogleTranslator(source='auto', target='ur').translate(text)
        except: return "معاف کریں، اس موضوع کے بارے میں معلومات حاصل نہیں ہو سکیں۔"
    return text

def get_news(category=None, country="us"):
    try:
        url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"
        if category: url += f"&category={category}"
        response = requests.get(url)
        data = response.json()
        if data['status'] != 'ok': return translate_to_urdu("Sorry, I couldn't fetch news.")
        articles = data.get('articles', [])
        if not articles: return translate_to_urdu("No news found.")
        headlines = ""
        for i, article in enumerate(articles[:5], 1):
            headlines += f"{i}. {article['title']} ({article['source']['name']})\n"
        return translate_to_urdu(headlines)
    except:
        return translate_to_urdu("Sorry, could not fetch news.")

def try_solve_math(expr: str):
    s = expr.strip().replace('^', '**')
    if not re.match(r'^[0-9\.\s\+\-\*\/\^\(\)]+$', s): raise ValueError("Not a safe math expression")
    if sp: return str(sp.sympify(s))
    return str(eval(s, {"__builtins__": None}, {}))

PRE_FILLED_KNOWLEDGE = {
    "who is the founder of fusion ai": {
        "en": "Ayan Zafar (born 14 August 2010) is the principal developer and creator of Fusion AI.",
        "ur": "آیان ظفر (پیدائش 14 اگست 2010) فیوژن اے آئی کے پرنسپل ڈویلپر اور تخلیق کار ہیں۔"
    },
    "what is ai": {
        "en": "AI stands for Artificial Intelligence, which allows machines to perform tasks that normally require human intelligence.",
        "ur": "AI کا مطلب مصنوعی ذہانت ہے، جو مشینوں کو وہ کام کرنے کی اجازت دیتی ہے جو عام طور پر انسانی ذہانت کی ضرورت ہوتی ہے۔"
    },
    "capital of pakistan": {
        "en": "Islamabad is the capital of Pakistan.",
        "ur": "اسلام آباد پاکستان کا دارالحکومت ہے۔"
    }
}

# ---------------- Routes ----------------
@app.route("/")
def home():
    default_message = {
        "en": "Hello! Please choose a language: English (en) or Urdu (ur).",
        "ur": "ہیلو! زبان منتخب کریں: انگریزی (en) یا اردو (ur)۔"
    }
    return render_template("index.html", default_message=default_message[user_language])

@app.route("/get", methods=["GET"])
def get_bot_response():
    global user_language
    user_text = request.args.get('msg', '').strip()
    if not user_text: return Response(translate_to_urdu("Please type something."), mimetype='text/plain; charset=utf-8')
    user_normalized = user_text.lower().translate(str.maketrans('', '', string.punctuation))

    # Language switching
    if user_normalized in ["urdu","ur"]:
        user_language = "ur"; response="زبان اردو میں تبدیل کر دی گئی ہے۔"
        save_chat(user_text,response); return Response(response,mimetype='text/plain; charset=utf-8')
    elif user_normalized in ["english","en"]:
        user_language = "en"; response="Language switched to English."
        save_chat(user_text,response); return Response(response,mimetype='text/plain; charset=utf-8')

    # Greetings
    if user_normalized in ["hi","hello","hey","salam","assalamualaikum"]:
        response = "ہیلو! میں آپ کا فیوژن اے آئی ہوں۔ کس طرح مدد کر سکتا ہوں؟" if user_language=="ur" else "Hello! I'm Fusion AI. How can I help you today?"
        save_chat(user_text,response); return Response(response,mimetype='text/plain; charset=utf-8')

    # Pre-filled knowledge
    for key,value in PRE_FILLED_KNOWLEDGE.items():
        if key in user_normalized: response=value[user_language]; save_chat(user_text,response); return Response(response,mimetype='text/plain; charset=utf-8')

    # News
    if "news" in user_normalized:
        category = None
        if "sports" in user_normalized: category="sports"
        elif "technology" in user_normalized: category="technology"
        response = get_news(category); save_chat(user_text,response); return Response(response,mimetype='text/plain; charset=utf-8')

    # Math
    try:
        math_result = try_solve_math(user_text)
        save_chat(user_text,math_result); return Response(math_result,mimetype='text/plain; charset=utf-8')
    except: pass

    # Wikipedia
    if user_normalized.startswith("who is") or user_normalized.startswith("what is"):
        topic = user_normalized.replace("who is","").replace("what is","").strip()
        if topic:
            try: summary=wikipedia.summary(topic,sentences=4)
            except wikipedia.exceptions.DisambiguationError as e: summary=wikipedia.summary(e.options[0],sentences=4)
            except wikipedia.exceptions.PageError: summary=f"معاف کریں، '{topic}' کے بارے میں معلومات حاصل نہیں ہو سکیں۔"
            summary=translate_to_urdu(summary); save_chat(user_text,summary); return Response(summary)


    # --- High-Level Geometry ---
    geo_patterns = {
        "triangle area heron": lambda args: triangle_area_heron(*map(float,args)),
        "triangle area": lambda args: triangle_area_base_height(float(args[0]),float(args[1])),
        "circle area": lambda args: circle_area(float(args[0])),
        "circle circumference": lambda args: circle_circumference(float(args[0])),
        "distance": lambda args: distance_between_points(float(args[0]),float(args[1]),float(args[2]),float(args[3])),
        "midpoint": lambda args: midpoint(float(args[0]),float(args[1]),float(args[2]),float(args[3]))
    }

    for pattern, func in geo_patterns.items():
        if user_normalized.startswith(pattern):
            try:
                args = user_normalized.replace(pattern,"").strip().split()
                result, steps = func(args)

                # Professional formatting
                formatted_steps = "\n".join([f"Step {i+1}: {s}" for i, s in enumerate(steps)])
                response = f"✅ Calculation Complete:\n{formatted_steps}\n\n🎯 Result: {result}"
            
            except Exception as e:
                response = f"⚠️ Error: {str(e)}"
            
            save_chat(user_text, response)
            return Response(response, mimetype='text/plain; charset=utf-8')

    # Fallback (if nothing matched)
    response = respond(user_text)
    save_chat(user_text,response)
    return Response(response,mimetype='text/plain; charset=utf-8')


if __name__ == "__main__":
    app.run(debug=True),
