# Simple AI chatbot with a 700-word dictionary, math solving, and conversation history.
from textblob import TextBlob
import wikipedia
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Training data: (example sentence, intent)
TRAINING_DATA = [
    ("hi", "greeting"),
    ("hello", "greeting"),
    ("hey", "greeting"),
    ("who are you", "about"),
    ("what is your name", "about"),
    ("2+2", "math"),
    ("lion", "animal"),
]

texts, labels = zip(*TRAINING_DATA)

# Turn text into numbers
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Train a classifier
model = MultinomialNB()
model.fit(X, labels)

def predict_intent(user_input):
    X_test = vectorizer.transform([user_input])
    return model.predict(X_test)[0]
GREETING_MSG = "Hello! I'm Fusion AI. How can I help you today?"

def get_response(user_input):
    user_input = user_input.lower()

    # Greeting responses
    if user_input in ["hi", "hello", "hey"]:
        return GREETING_MSG
# load KB from file
KB_FILE = "kb.json"
def load_kb():
    try:
        with open(KB_FILE, "r", encoding="utf-8") as f:
            pairs = json.load(f)
            return {item["user"].strip().lower(): item["bot"] for item in pairs if "user" in item and "bot" in item}
    except Exception:
        return {}
LOWER_KB = load_kb()

import os, json, re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DATA_FILE = "data.json"

def get_response(user_input):
    user_input = user_input.lower().strip()

    # ML intent detection
    intent = predict_intent(user_input)

    if intent == "greeting":
        return "Hello! I'm Fusion AI. How can I help you today?"
    elif intent == "about":
        return "I’m Fusion AI, your assistant."
    elif intent == "math":
        try:
            return f"Answer: {eval(user_input)}"
        except:
            return "I couldn’t solve that math problem."
    elif intent == "animal":
        if user_input in WORD_DICTIONARY:
            return WORD_DICTIONARY[user_input]
        else:
            return "That’s an interesting animal!"


# ---------- 1) PUT YOUR WORD_DICTIONARY HERE ----------
WORD_DICTIONARY = {
    "school": "A place where students learn from teachers.",
    "teacher": "A person who helps students learn new things.",
    "student": "A person who studies at a school or college.",
    "education": "The process of learning and gaining knowledge.",
    "friend": "Someone you know well and like.",
    "family": "A group of people related by blood or marriage.",
    "village": "A small community in a rural area.",
    "city": "A large town with many people and buildings.",
    "library": "A place with many books for reading or borrowing.",
    "laboratory": "A room for scientific experiments.",
    "principal": "The head of a school.",
    "holiday": "A day when you do not go to work or school.",
    "health": "The condition of your body and mind.",
    "illness": "A state of being sick or unhealthy.",
    "application": "A formal request for something.",
    "letter": "A written message sent to someone.",
    "essay": "A short piece of writing on a particular subject.",
    "respect": "A feeling of admiration for someone or something.",
    "unity": "Being together or at one with others.",
    "cooperation": "Working together for a common goal.",
    "abandon": "to leave something behind permanently.",
    "ability": "the skill to do something.",
    "absorb": "to soak up or take in.",
    "abstract": "existing in thought but not physical.",
    "abundant": "present in large amounts.",
    "accept": "to agree to receive or approve.",
    "access": "the right or way to enter or use.",
    "accident": "an unexpected event causing damage.",
    "accurate": "correct and free of error.",
    "achieve": "to succeed in doing something.",
    "adapt": "to change for a new situation.",
    "addict": "a person dependent on something.",
    "admire": "to respect and look up to.",
    "admit": "to accept the truth or allow entry.",
    "adopt": "to legally take as one’s own.",
    "advance": "to move forward.",
    "advice": "helpful guidance.",
    "affect": "to influence something.",
    "afford": "to have enough money or time for.",
    "afraid": "feeling fear.",
    "agree": "to share the same opinion.",
    "aid": "help or assistance.",
    "aim": "a goal or target.",
    "alert": "watchful and ready.",
    "alike": "similar or the same.",
    "alive": "living, not dead.",
    "allow": "to give permission.",
    "alone": "without others.",
    "amateur": "not professional.",
    "amazing": "causing great surprise.",
    "ambition": "a strong desire for success.",
    "amount": "quantity of something.",
    "amuse": "to make someone laugh or smile.",
    "analyze": "to study carefully.",
    "ancient": "very old.",
    "anger": "strong feeling of dislike.",
    "announce": "to make public information.",
    "annual": "happening once a year.",
    "answer": "a reply or solution.",
    "anxious": "worried or uneasy.",
    "apart": "separated by distance.",
    "appear": "to become visible.",
    "apply": "to make a request or put to use.",
    "appoint": "to assign a duty.",
    "appreciate": "to value highly.",
    "approach": "to come nearer.",
    "appropriate": "suitable or proper.",
    "approve": "to accept as good.",
    "argue": "to disagree with reasons.",
    "arise": "to come up or happen.",
    "arrange": "to put in order.",
    "arrest": "to take into police custody.",
    "arrive": "to reach a place.",
    "artistic": "creative or skilled in art.",
    "ashamed": "feeling guilt or embarrassment.",
    "ask": "to request information.",
    "asleep": "in a state of sleep.",
    "assist": "to help.",
    "assume": "to take for granted.",
    "assure": "to guarantee or promise.",
    "attach": "to join or connect.",
    "attempt": "to try.",
    "attend": "to be present.",
    "attract": "to draw attention.",
    "avoid": "to stay away from.",
    "aware": "having knowledge.",
    "awful": "very bad.",
    "balance": "state of being stable.",
    "bare": "not covered.",
    "bargain": "a good deal.",
    "base": "the bottom or foundation.",
    "basic": "simple and essential.",
    "battle": "a fight between groups.",
    "beautiful": "pleasing to the eye.",
    "become": "to turn into.",
    "beg": "to ask strongly.",
    "begin": "to start.",
    "behave": "to act in a certain way.",
    "believe": "to accept as true.",
    "belong": "to be part of something.",
    "benefit": "something good or helpful.",
    "best": "better than all others.",
    "better": "improved quality.",
    "between": "in the middle of two.",
    "beyond": "further than something.",
    "big": "large in size.",
    "bill": "a request for payment.",
    "bind": "to tie together.",
    "birth": "the beginning of life.",
    "bitter": "sharp or unpleasant taste.",
    "black": "the darkest color.",
    "blame": "to say someone caused a problem.",
    "blind": "unable to see.",
    "block": "to stop movement.",
    "blood": "red liquid in the body.",
    "blow": "to move air strongly.",
    "blue": "a color like the sky.",
    "board": "a flat surface or a committee.",
    "body": "the physical structure of a person.",
    "bold": "brave or confident.",
    "run": "to move quickly on foot.",
    "walk": "to move slowly on foot.",
    "eat": "to take in food.",
    "drink": "to swallow liquid.",
    "sit": "to rest on a chair or ground.",
    "stand": "to be upright on feet.",
    "jump": "to push off the ground into the air.",
    "sleep": "to rest with eyes closed.",
    "read": "to look at and understand written words.",
    "write": "to put words on paper.",
    "happy": "feeling good or pleased.",
    "sad": "feeling unhappy.",
    "angry": "feeling upset or mad.",
    "afraid": "feeling scared.",
    "excited": "feeling eager or thrilled.",
    "calm": "feeling peaceful and relaxed.",
    "lonely": "feeling alone.",
"proud": "feeling satisfied with yourself.",
    "jealous": "wanting what others have.",
    "sun": "the star that gives us light and heat.",
    "moon": "the natural satellite of Earth.",
    "star": "a glowing ball of gas in space.",
    "cloud": "water vapor seen in the sky.",
    "rain": "water falling from clouds.",
    "snow": "frozen water falling from clouds.",
    "river": "flowing water on land.",
    "lake": "still water surrounded by land.",
    "mountain": "very high land.",
    "forest": "a large area with many trees.",
    "morning": "time after sunrise.",
    "afternoon": "time after midday.",
        "evening": "time after sunset.",
    "night": "time when it is dark.",
    "day": "24 hours.",
    "week": "7 days.",
    "month": "about 30 days.",
    "year": "365 days.",
    "first": "coming before all others.",
    "last": "coming at the end.",
    "man": "adult male.",
    "woman": "adult female.",
    "child": "young person.",
    "friend": "someone you like.",
    "enemy": "someone against you.",
    "teacher": "person who teaches.",
    "student": "person who learns.",
    "doctor": "person who heals.",
    "farmer": "person who grows crops.",
    "worker": "person who works.",
    "book": "a set of written pages.",
    "pen": "tool for writing with ink.",
    "pencil": "tool for writing with lead.",
    "paper": "material to write on.",
    "bag": "container for carrying things.",
    "chair": "seat with a back.",
    "table": "flat surface with legs.",
    "bed": "furniture for sleeping.",
    "cup": "container for drinking.",
    "plate": "dish for food.",
    "dog": "pet animal that barks.",
    "cat": "pet animal that meows.",
    "cow": "farm animal giving milk.",
    "goat": "farm animal with horns.",
    "horse": "large animal used for riding.",
    "sheep": "wool-giving farm animal.",
    "lion": "wild animal, king of jungle.",
    "tiger": "striped wild cat.",
    "elephant": "large animal with trunk.",
    "monkey": "playful animal with tail.",
    "rice": "small white grain eaten as food.",
    "bread": "baked food from flour.",
    "milk": "white drink from animals.",
    "water": "clear liquid for drinking.",
    "juice": "liquid from fruits.",
    "meat": "food from animals.",
    "fish": "water animal eaten as food.",
    "egg": "oval food from birds.",
    "fruit": "sweet part of a plant.",
    "vegetable": "plant eaten as food.",
    "red": "color of blood.",
    "blue": "color of sky.",
    "green": "color of grass.",
    "yellow": "color of sun.",
    "black": "darkest color.",
    "white": "lightest color.",
    "brown": "color of wood.",
    "orange": "mix of red and yellow.",
    "purple": "mix of red and blue.",
    "pink": "light red color.",
    "head": "top part of body.",
    "eye": "organ of sight.",
    "ear": "organ of hearing.",
    "nose": "organ of smell.",
    "mouth": "part used to eat and talk.",
    "hand": "part for holding.",
    "leg": "part for walking.",
    "foot": "lower part of leg.",
    "finger": "small parts of hand.",
    "hair": "strands on the head.",
    "toe": "end of foot.",
    "arm": "limb for lifting.",
    "shoulder": "part joining arm to body.",
    "back": "rear side of body.",
    "chest": "front upper body.",
    "heart": "organ that pumps blood.",
    "brain": "organ of thinking.",
    "stomach": "organ that digests food.",
    "liver": "organ that cleans blood.",
    "skin": "outer covering of body.",
    "bone": "hard part inside body.",
    "blood": "red liquid in body.",
    "teeth": "hard parts in mouth.",
    "tongue": "part for tasting.",
    "neck": "joins head to body.",
    "knee": "joint in leg.",
    "elbow": "joint in arm.",
    "palm": "inside of hand.",
    "nail": "hard part at finger end.",
    "lung": "organ for breathing.",
    "sun": "star giving light.",
    "moon": "satellite of Earth.",
    "star": "shining body in sky.",
    "sky": "space above Earth.",
    "cloud": "water vapor in air.",
    "rain": "water falling from sky.",
    "snow": "frozen water from sky.",
    "wind": "moving air.",
    "storm": "violent weather.",
    "rainbow": "colored arc in sky.",
    "mountain": "high land.",
    "hill": "small mountain.",
    "river": "flowing water.",
    "lake": "still water.",
    "sea": "large salty water.",
    "ocean": "biggest body of water.",
    "desert": "dry sandy land.",
    "forest": "land with trees.",
    "island": "land in water.",
    "valley": "low land between hills.",
    "house": "place to live.",
    "room": "part of house.",
    "door": "entry in wall.",
    "window": "opening in wall.",
    "roof": "top of house.",
    "wall": "vertical divider.",
    "floor": "base of room.",
    "garden": "land with plants.",
    "kitchen": "place to cook.",
    "bathroom": "place to wash.",
    "school": "place to learn.",
    "teacher": "one who teaches.",
    "student": "one who studies.",
    "class": "group of learners.",
    "bookshop": "shop selling books.",
    "library": "place with books.",
    "hospital": "place for treatment.",
    "doctor": "medical professional.",
    "nurse": "helps doctor.",
    "patient": "sick person.",
    "shop": "place to buy things.",
    "market": "area with shops.",
    "bank": "place for money.",
    "office": "place for work.",
    "factory": "place making goods.",
    "farm": "land for growing crops.",
    "park": "land for recreation.",
    "road": "way for vehicles.",
    "street": "smaller road.",
    "bridge": "road over water.",
    "car": "four-wheeled vehicle.",
    "bus": "large vehicle for passengers.",
    "truck": "vehicle carrying goods.",
    "train": "railway transport.",
    "plane": "air transport.",
    "ship": "water transport.",
    "boat": "small watercraft.",
    "bicycle": "two-wheeled vehicle.",
    "motorcycle": "two-wheeled motor vehicle.",
    "taxi": "paid car transport.",
    "apple": "round red fruit.",
    "banana": "long yellow fruit.",
    "mango": "sweet tropical fruit.",
    "orange": "round citrus fruit.",
    "grapes": "small round fruit.",
    "pineapple": "tropical spiky fruit.",
    "strawberry": "red sweet fruit.",
    "pear": "green juicy fruit.",
    "peach": "soft juicy fruit.",
    "lemon": "sour yellow fruit.",
    "potato": "root vegetable.",
    "tomato": "red vegetable/fruit.",
    "onion": "strong-flavored vegetable.",
    "carrot": "orange root vegetable.",
    "cabbage": "leafy vegetable.",
    "spinach": "green leafy vegetable.",
    "beans": "seed vegetable.",
    "peas": "small green vegetable.",
    "chili": "spicy vegetable.",
    "corn": "yellow grain crop.",
    "happy": "feeling joy.",
    "sad": "feeling sorrow.",
    "angry": "feeling strong dislike.",
    "afraid": "feeling fear.",
    "surprised": "feeling sudden shock.",
    "excited": "feeling great joy.",
    "tired": "lacking energy.",
    "hungry": "needing food.",
    "thirsty": "needing drink.",
    "lonely": "feeling alone.",
    "love": "strong liking.",
    "hate": "strong dislike.",
    "friendship": "bond of friends.",
    "peace": "absence of war.",
    "war": "conflict between groups.",
    "fight": "physical struggle.",
    "help": "giving support.",
    "work": "activity to achieve something.",
    "play": "activity for fun.",
    "rest": "time to relax.",
    "sleep": "natural rest.",
    "run": "move quickly.",
    "walk": "move on feet.",
    "sit": "rest on seat.",
    "stand": "rise on feet.",
    "jump": "push body upward.",
    "sing": "make music with voice.",
    "dance": "move to music.",
    "write": "form words.",
    "read": "understand written words.",
    "eat": "take in food.",
    "drink": "take in liquid.",
    "cook": "prepare food.",
    "wash": "clean with water.",
    "clean": "remove dirt.",
    "build": "make something.",
    "draw": "make picture.",
    "paint": "apply color.",
    "open": "move to allow entry.",
    "close": "shut something.",
    "hot": "having high temperature.",
    "cold": "having low temperature.",
    "big": "of large size.",
    "small": "of little size.",
    "tall": "of great height.",
    "short": "of less height.",
    "long": "extended length.",
    "wide": "large breadth.",
    "narrow": "small width.",
    "heavy": "of great weight.",
    "light": "of little weight.",
    "fast": "moving quickly.",
    "slow": "not fast.",
    "near": "close in distance.",
    "far": "distant.",
    "early": "before time.",
    "late": "after time.",
    "new": "recently made.",
    "old": "existing long.",
    "good": "morally right.",
    "bad": "morally wrong.",
    "rich": "having wealth.",
    "poor": "lacking wealth.",
    "young": "not old.",
    "strong": "having power.",
    "weak": "lacking strength.",
    "dirty": "not clean.",
    "true": "not false.",
    "false": "not true.",
    "right": "correct.",
    "wrong": "incorrect.",
    "closed": "not open.",
    "day": "time with light.",
    "night": "time with darkness.",
    "morning": "early part of day.",
    "evening": "late part of day.",
    "week": "seven days.",
    "month": "about thirty days.",
    "year": "twelve months.",
    "today": "this day.",
    "tomorrow": "next day.",
    "yesterday": "previous day.",
    "time": "continuous progress of events.",
    "hour": "sixty minutes.",
    "minute": "sixty seconds.",
    "second": "smallest unit of time.",
    "clock": "device for time.",
    "watch": "small clock on hand.",
    "calendar": "shows days and months.",
    "past": "time before now.",
    "present": "time now.",
    "future": "time to come.",
    "first": "before all.",
    "last": "after all.",
    "middle": "between ends.",
    "start": "beginning.",
    "end": "finish.",
    "smile": "happy expression.",
    "cry": "shed tears.",
    "laugh": "show joy with sound.",
    "shout": "speak loudly.",
    "whisper": "speak softly.",
    "talk": "exchange words.",
    "listen": "pay attention to sound.",
    "hear": "perceive sound.",
    "see": "use eyes.",
    "look": "direct eyes.",
    "watch": "observe closely.",
    "touch": "feel by hand.",
    "smell": "sense with nose.",
    "taste": "sense with tongue.",
    "think": "use mind.",
    "know": "have knowledge.",
    "learn": "gain knowledge.",
    "understand": "grasp meaning.",
    "remember": "keep in mind.",
    "forget": "fail to recall.",
    "buy": "get by paying.",
    "sell": "give for money.",
    "give": "offer to someone.",
    "take": "receive something.",
    "send": "cause to go.",
    "bring": "carry to place.",
    "call": "name or summon.",
    "phone": "device for calling.",
    "message": "written communication.",
    "letter": "written words to someone.",
    "email": "digital message.",
    "post": "mail system.",
    "news": "new information.",
    "story": "account of events.",
    "poem": "form of verse writing.",
    "song": "musical composition.",
    "music": "art of sound.",
    "game": "activity for fun.",
    "sport": "physical activity for play.",
    "cricket": "bat-and-ball game.",
    "football": "kicking ball game.",
    "tennis": "racket sport.",
    "hockey": "stick-and-ball game.",
    "volleyball": "ball over net game.",
    "swimming": "moving in water.",
    "running": "fast movement.",
    "cycling": "riding bicycle.",
    "boxing": "sport of fighting.",
    "wrestling": "sport of grappling.",
    "clothes": "covering for body.",
    "shirt": "upper body clothing.",
    "pant": "lower body clothing.",
    "dress": "one-piece clothing.",
    "coat": "outer garment.",
    "jacket": "short coat.",
    "sweater": "warm knitted garment.",
    "socks": "clothing for feet.",
    "shoes": "covering for feet.",
    "hat": "head covering.",
    "cap": "simple headwear.",
    "scarf": "cloth for neck.",
    "gloves": "hand covering.",
    "belt": "waist strap.",
    "tie": "neckwear.",
    "skirt": "lower garment for women.",
    "shorts": "short pants.",
    "jeans": "denim pants.",
    "uniform": "same clothing for group.",
    "suit": "formal clothing set.",
    "ring": "circular jewelry.",
    "necklace": "jewelry for neck.",
    "bracelet": "jewelry for wrist.",
    "earring": "jewelry for ear.",
    "wallet": "pocket case for money.",
    "purse": "small bag for women.",
    "umbrella": "cover from rain.",
    "key": "tool to open locks.",
    "lock": "device to close.",
    "doorbell": "bell at door.",
    "light": "source of brightness.",
    "lamp": "device for light.",
    "fan": "device giving air.",
    "tv": "device showing video.",
    "radio": "device for sound.",
    "computer": "machine for tasks.",
    "laptop": "portable computer.",
    "tablet": "handheld computer.",
    "camera": "device taking photos.",
    "mic": "device for sound input.",
    "speaker": "device for sound output.",
    "printer": "device for printing.",
    "fridge": "machine to keep cool.",
    "oven": "device to bake food.",
    "stove": "device to cook food.",
    "washing machine": "machine to wash clothes.",
    "iron": "device to press clothes.",
    "engineer": "designs machines.",
    "chef": "professional cook.",
    "artist": "makes art.",
    "writer": "creates books.",
    "singer": "performs songs.",
    "actor": "performs in plays.",
    "dancer": "performs dances.",
    "athlete": "sports player.",
    "scientist": "studies science.",
    "king": "male ruler.",
    "queen": "female ruler.",
    "prince": "son of king.",
    "princess": "daughter of king.",
    "leader": "one who guides.",
    "boss": "head of workers.",
    "judge": "decides law cases.",
    "lawyer": "practices law.",
    "merchant": "sells goods.",
    "shopkeeper": "runs a shop.",
    "clerk": "office assistant.",
    "manager": "organizes workers.",
    "banker": "works in bank.",
    "pilot": "flies aircraft.",
    "guard": "protects places.",
    "fisherman": "catches fish.",
    "hunter": "kills animals.",
    "miner": "digs minerals.",
    "builder": "constructs houses.",
    "carpenter": "works with wood.",
    "mechanic": "repairs machines.",
    "plumber": "fixes water pipes.",
    "electrician": "fixes electricity.",
    "tailor": "makes clothes.",
    "conductor": "manages bus.",
    "captain": "leads ship.",
    "airport": "planes land there.",
    "station": "trains stop there.",
    "port": "ships dock there.",
    "algorithm": "A step-by-step procedure for solving a problem.",
    "artificial intelligence": "Machines simulating human intelligence.",
    "bandwidth": "Maximum data transfer capacity of a network.",
    "big data": "Extremely large datasets analyzed for patterns.",
    "blockchain": "Decentralized digital ledger technology.",
    "cache": "Temporary storage for quick access.",
    "cloud computing": "Internet-based computing and storage services.",
    "compiler": "Software that converts code into machine language.",
    "cybersecurity": "Protection of systems and data from attacks.",
    "database": "Organized collection of data.",
    "debugging": "Process of finding and fixing code errors.",
    "encryption": "Converting data into secure unreadable form.",
    "firmware": "Permanent software programmed into hardware.",
    "gpu": "Graphics Processing Unit for visual rendering.",
    "hardware": "Physical components of a computer.",
    "html": "Hypertext Markup Language for web pages.",
    "http": "Protocol for transferring web data.",
    "iot": "Internet of Things, network of smart devices.",
    "java": "Popular programming language.",
    "json": "Data format for transmitting information.",
    "kernel": "Core of an operating system.",
    "lan": "Local Area Network.",
    "machine learning": "AI technique where systems learn from data.",
    "malware": "Malicious software that harms computers.",
    "neural network": "Computer system modeled on human brain.",
    "open source": "Software with publicly available code.",
    "operating system": "Software managing hardware and resources.",
    "packet": "Small chunk of transmitted network data.",
    "phishing": "Online fraud to steal information.",
    "python": "High-level programming language.",
    "quantum computing": "Computers using quantum principles.",
    "ram": "Random Access Memory, temporary storage.",
    "saas": "Software as a Service, cloud-based apps.",
    "server": "Computer that provides services to others.",
    "source code": "Human-readable programming instructions.",
    "sql": "Structured Query Language for databases.",
    "tcp/ip": "Core Internet communication protocol.",
    "trojan": "Malware disguised as useful software.",
    "ui": "User Interface of an application.",
    "url": "Web address of a resource.",
    "ux": "User Experience design.",
    "virus": "Malicious code that spreads on systems.",
    "vpn": "Virtual Private Network for secure browsing.",
    "wi-fi": "Wireless internet connection.",
    "xml": "Markup language for structured data.",
    "api": "Application Programming Interface.",
    "cloud storage": "Online saving of files.",
    "dns": "Domain Name System, converts names to IP.",
    "firewall": "Security system that blocks threats.",
    "git": "Version control system.",
    "github": "Hosting service for code.",
    "ip address": "Unique number of a device on network.",
    "machine code": "Binary instructions for computers.",
    "mobile app": "Software designed for smartphones.",
    "node": "Device or point in a network.",
    "pixel": "Smallest unit of a digital image.",
    "saap": "Software as a Product (sold license).",
    "saac": "Security as a Code.",
    "session": "Temporary connection in networking.",
    "socket": "End-point for network communication.",
    "sql injection": "Database hacking technique.",
    "spyware": "Software that secretly gathers data.",
    "syntax": "Rules of programming language.",
    "token": "Digital unit used in authentication.",
    "trackpad": "Touch-sensitive input device.",
    "wearable tech": "Gadgets worn on body.",
    "web browser": "Software to access internet.",
    "wireless": "Communication without physical cables.",
    "zoom": "Video conferencing app.",
    "edge computing": "Processing data near source.",
    "emulator": "Software mimicking another system.",
    "gui": "Graphical User Interface.",
    "hotspot": "Internet access point.",
    "ipv6": "New internet addressing system.",
    "metadata": "Data about data.",
    "plugin": "Add-on feature for software.",
    "robotics": "Technology of designing robots.",
    "script": "Short program code.",
    "search engine": "Tool for finding information online.",
    "seo": "Search Engine Optimization.",
    "sms": "Short Message Service.",
    "stream": "Continuous flow of data.",
    "virtual reality": "Computer-generated immersive world.",
    "web server": "Computer hosting websites.",
    "zip file": "Compressed file format.",
    "asset": "Anything of value owned.",
    "balance sheet": "Financial statement showing assets and liabilities.",
    "brand": "Identity and image of a business.",
    "capital": "Money or resources for investment.",
    "ceo": "Chief Executive Officer.",
    "client": "Customer receiving services.",
    "commerce": "Buying and selling activities.",
    "competition": "Rivalry in business market.",
    "consumer": "End user of goods or services.",
    "contract": "Legal agreement between parties.",
    "corporation": "Legal entity separate from owners.",
    "credit": "Borrowed money to be repaid.",
    "debt": "Money owed.",
    "demand": "Desire for a product.",
    "dividend": "Profit share paid to shareholders.",
    "e-commerce": "Online business transactions.",
    "equity": "Ownership interest in a business.",
    "entrepreneur": "Person starting a business.",
    "expense": "Money spent by business.",
    "export": "Selling goods abroad.",
    "franchise": "Business under another company’s brand.",
    "gdp": "Gross Domestic Product, total output.",
    "import": "Bringing goods from abroad.",
    "industry": "Sector of economy.",
    "inflation": "Rise in prices.",
    "investment": "Putting money to earn profit.",
    "liability": "Legal or financial obligation.",
    "loan": "Borrowed money.",
    "market": "Place where goods are exchanged.",
    "marketing": "Promoting and selling products.",
    "merger": "Combining two businesses.",
    "monopoly": "Exclusive control of a market.",
    "net profit": "Earnings after expenses.",
    "negotiation": "Discussion to reach agreement.",
    "partnership": "Business owned by two or more.",
    "payroll": "List of employees’ wages.",
    "profit": "Money gained after costs.",
    "revenue": "Income earned.",
    "risk": "Chance of loss.",
    "shareholder": "Owner of company shares.",
    "startup": "New small business venture.",
    "strategy": "Long-term plan of action.",
    "subsidiary": "Company controlled by another.",
    "supply": "Availability of goods.",
    "supply chain": "Network from production to customer.",
    "tax": "Compulsory government charge.",
    "trademark": "Legal protection of brand.",
    "value": "Worth of something.",
    "vendor": "Supplier of goods.",
    "wholesale": "Selling in bulk.",
    "account": "Record of financial transactions.",
    "audit": "Examination of accounts.",
    "bankruptcy": "Legal state of insolvency.",
    "cash flow": "Money moving in and out.",
    "collateral": "Asset pledged for loan.",
    "consulting": "Giving expert advice.",
    "customer": "Person buying products.",
    "data analytics": "Studying data for business use.",
    "distribution": "Delivering goods to market.",
    "economy": "System of production and consumption.",
    "employer": "Person hiring workers.",
    "forecasting": "Predicting future trends.",
    "human resources": "Department for managing staff.",
    "invoice": "Bill for goods/services.",
    "outsourcing": "Hiring external service providers.",
    "productivity": "Efficiency of production.",
    "return on investment": "Profit earned on investment.",
    "stakeholder": "Anyone affected by business.",
    "stock market": "Place where shares are traded.",
    "sustainability": "Business with minimal negative impact.",
    "trade": "Exchange of goods/services.",
    "treasury": "Management of funds.",
    "turnover": "Sales within a time.",
    "venture capital": "Funding for startups.",
    "wage": "Payment for work.",
    "asexual reproduction": "Offspring from one parent.",
    "sexual reproduction": "Offspring from two parents.",
    "fertilization": "Fusion of sperm and egg.",
    "gamete": "Sex cell (sperm/egg).",
    "ovum": "Female reproductive cell.",
    "sperm": "Male reproductive cell.",
    "zygote": "Fertilized egg cell.",
    "embryo": "Early stage of development.",
    "fetus": "Later stage of development.",
    "ovary": "Female reproductive organ.",
    "testis": "Male reproductive organ.",
    "uterus": "Organ where fetus grows.",
    "placenta": "Organ supplying nutrients to fetus.",
    "menstruation": "Monthly shedding of uterus lining.",
    "ovulation": "Release of egg from ovary.",
    "hormone": "Chemical messenger.",
    "estrogen": "Female sex hormone.",
    "progesterone": "Hormone maintaining pregnancy.",
    "testosterone": "Male sex hormone.",
    "puberty": "Stage of sexual maturity.",
    "ejaculation": "Release of sperm.",
    "copulation": "Act of sexual intercourse.",
    "fertile period": "Days when conception is possible.",
    "contraception": "Preventing pregnancy.",
    "gestation": "Pregnancy period.",
    "cloning": "Producing identical organisms.",
    "pollination": "Transfer of pollen in plants.",
    "cross-pollination": "Pollen transfer between different plants.",
    "self-pollination": "Pollen transfer within same plant.",
    "seed": "Result of plant reproduction.",
    "fruit": "Mature ovary of plant.",
    "spore": "Asexual reproductive unit.",
    "vegetative propagation": "Plant reproduction without seeds.",
    "budding": "New organism from parent outgrowth.",
    "fragmentation": "Organism splits into parts.",
    "regeneration": "Growth of lost body parts.",
    "binary fission": "Splitting of one cell into two.",
    "mitosis": "Cell division for growth.",
    "meiosis": "Cell division for gametes.",
    "chromosome": "DNA carrying structure.",
    "gene": "Unit of heredity.",
    "dna": "Genetic material.",
    "rna": "Molecule for protein synthesis.",
    "mutation": "Change in genetic sequence.",
    "inheritance": "Passing traits to offspring.",
    "dominant trait": "Expressed gene version.",
    "recessive trait": "Hidden gene version.",
    "genotype": "Genetic makeup.",
    "phenotype": "Observable traits.",
    "hybrid": "Offspring from different parents.",
    "purebred": "Offspring with same traits.",
    "carrier": "Organism with hidden gene.",
    "fertility": "Ability to reproduce.",
    "infertility": "Inability to reproduce.",
    "ivf": "In vitro fertilization technique.",
    "embryo transfer": "Moving embryo into uterus.",
    "amniotic fluid": "Protective liquid around fetus.",
    "umbilical cord": "Connects fetus to placenta.",
    "lactation": "Milk production after birth.",
    "mammary glands": "Organs producing milk.",
    "gestational age": "Age of fetus in weeks.",
    "reproductive cycle": "Sequence of fertility events.",
    "spermatogenesis": "Process of making sperm.",
    "oogenesis": "Process of making eggs.",
    "gonad": "Organ producing gametes.",
    "soccer": "A team sport played between two teams of eleven players with a spherical ball.",
    "football": "A team sport where two sides compete to score goals by moving a ball into the opponent’s area; varies by region (soccer, American football, rugby).",
    "basketball": "A game played between two teams of five players where points are scored by throwing a ball through a hoop.",
    "baseball": "A bat-and-ball sport played between two teams where players hit a pitched ball and run bases to score runs.",
    "cricket": "A bat-and-ball game played between two teams of eleven players on a field with a 22-yard pitch.",
    "rugby": "A team sport played with an oval ball that can be kicked, carried, and passed by hand.",
    "tennis": "A racket sport played individually against a single opponent or between two teams of two players each.",
    "badminton": "A racket sport played by hitting a shuttlecock over a net.",
    "volleyball": "A team sport where two sides hit a ball over a high net, aiming to ground it on the opponent’s side.",
    "hockey": "A sport played by two teams using sticks to hit a ball or puck into the opponent’s goal.",
    "ice hockey": "A fast-paced team sport played on ice, using sticks to hit a puck into the goal.",
    "table tennis": "A racket sport played on a small table where players hit a lightweight ball back and forth across a net.",
    "golf": "A sport where players use clubs to hit balls into holes on a course in as few strokes as possible.",
    "boxing": "A combat sport in which two people throw punches at each other for a predetermined set of time.",
    "karate": "A Japanese martial art focusing on strikes, kicks, and defensive techniques.",
    "judo": "A Japanese martial art emphasizing throws and grappling techniques.",
    "taekwondo": "A Korean martial art that emphasizes high, fast kicks and jumping techniques.",
    "wrestling": "A combat sport where two competitors attempt to pin each other to the ground.",
    "mma": "Mixed Martial Arts, a full-contact combat sport combining techniques from boxing, wrestling, jiu-jitsu, and others.",
    "archery": "The sport or skill of shooting arrows with a bow at a target.",
    "fencing": "A sport of fighting with swords such as foil, épée, or sabre.",
    "rowing": "The sport of propelling a boat using oars.",
    "canoeing": "A sport where athletes paddle a canoe with single-bladed paddles.",
    "kayaking": "A sport where athletes paddle a kayak using double-bladed paddles.",
    "surfing": "A water sport where participants ride waves on a board.",
    "swimming": "An individual or team sport that involves using the whole body to move through water.",
    "diving": "A sport where athletes jump into water while performing acrobatics.",
    "sailing": "A sport involving controlling a boat powered by wind in its sails.",
    "windsurfing": "A water sport combining surfing and sailing using a sailboard.",
    "kitesurfing": "A water sport using a kite to harness wind power while riding a board.",
    "snowboarding": "A winter sport where athletes descend snowy slopes on a board.",
    "skiing": "A winter sport using skis to glide over snow.",
    "alpine skiing": "A form of skiing involving racing downhill on marked courses.",
    "cross-country skiing": "A long-distance skiing discipline across snowy terrains.",
    "ski jumping": "A winter sport where athletes jump from a ramp on skis and aim for distance.",
    "ice skating": "The act of gliding on ice using skates.",
    "figure skating": "An artistic form of ice skating involving spins, jumps, and choreography.",
    "speed skating": "A racing sport on ice where athletes skate laps as quickly as possible.",
    "curling": "A winter sport where teams slide stones on ice toward a target area.",
    "bobsleigh": "A winter sport where teams race down icy tracks in a sled.",
    "luge": "A winter sliding sport where athletes lie on their backs on a sled and race downhill.",
    "skeleton": "A winter sliding sport similar to luge but raced face-first.",
    "track and field": "A collection of athletic events including running, jumping, and throwing.",
    "marathon": "A long-distance running event of 42.195 kilometers.",
    "sprint": "A short-distance running event focused on maximum speed.",
    "relay race": "A running event where teams of runners pass a baton to each other.",
    "hurdles": "A running race where athletes jump over barriers.",
    "long jump": "A track and field event where athletes jump as far as possible from a take-off point.",
    "high jump": "A jumping event where athletes leap over a horizontal bar.",
    "triple jump": "A track and field event combining a hop, step, and jump.",
    "pole vault": "A jumping event where athletes use a pole to leap over a high bar.",
    "shot put": "A throwing event where athletes throw a heavy spherical object.",
    "discus": "A throwing event involving a heavy disc.",
    "javelin": "A throwing event where athletes hurl a spear-like object.",
    "hammer throw": "A track and field event involving throwing a heavy weight on a chain.",
    "cycling": "A sport involving riding bicycles competitively.",
    "road cycling": "Long-distance competitive racing on roads.",
    "mountain biking": "Cycling on off-road trails with specialized bikes.",
    "bmx": "Bicycle motocross racing and tricks on dirt tracks or ramps.",
    "track cycling": "Cycling races held on oval velodromes.",
    "triathlon": "A multi-sport event consisting of swimming, cycling, and running.",
    "decathlon": "A track and field event consisting of ten athletic disciplines.",
    "heptathlon": "A combined track and field event for women with seven disciplines.",
    "gymnastics": "A sport involving exercises requiring strength, flexibility, and balance.",
    "artistic gymnastics": "Gymnastics disciplines with floor routines, bars, vault, and beam.",
    "rhythmic gymnastics": "A form of gymnastics using apparatus like ribbons, balls, and hoops.",
    "trampolining": "A sport involving acrobatic routines performed on a trampoline.",
    "cheerleading": "A sport combining dance, gymnastics, and stunts to encourage teams.",
    "skateboarding": "A sport where athletes perform tricks using a skateboard.",
    "parkour": "A discipline of moving rapidly through environments using jumps, vaults, and climbing.",
    "esports": "Competitive video gaming played professionally.",
    "chess": "A strategic board game considered a sport by the International Olympic Committee.",
    "polo": "A horseback team sport where players hit a ball with mallets to score goals.",
    "equestrian": "Competitive horseback riding, including jumping and dressage.",
    "show jumping": "An equestrian discipline where horses jump over obstacles.",
    "dressage": "An equestrian discipline showcasing horse training and movements.",
    "eventing": "An equestrian triathlon of dressage, cross-country, and jumping.",
    "handball": "A fast-paced team sport where players pass and throw a ball to score in the opponent’s goal.",
    "water polo": "A team water sport played with a ball in a swimming pool.",
    "lacrosse": "A team sport where players use sticks with nets to catch and throw a ball.",
    "softball": "A bat-and-ball sport similar to baseball but played with a larger ball and shorter field.",
    "netball": "A ball sport similar to basketball but with no dribbling and specialized positions.",
    "squash": "A racket sport played indoors where players hit a ball against a wall.",
    "racquetball": "A racket sport played indoors with a hollow rubber ball.",
    "pickleball": "A paddle sport combining elements of tennis, badminton, and ping pong.",
    "dodgeball": "A team sport where players throw balls at opponents while avoiding being hit.",
    "kabaddi": "A South Asian team contact sport combining tag and wrestling elements.",
    "sepaktakraw": "A Southeast Asian sport where players use their feet, head, knees, and chest to hit a ball over a net.",
    "petanque": "A French outdoor game where players throw metal balls aiming to land close to a target ball.",
    "bocce": "An Italian ball sport where players roll balls to get closest to a smaller ball.",
    "gaelic football": "An Irish sport combining elements of soccer and rugby.",
    "hurling": "An Irish stick-and-ball game similar to field hockey but faster.",
    "shinty": "A Scottish stick-and-ball sport played with curved sticks.",
    "aussie rules football": "A contact sport played mainly in Australia with an oval ball and large field.",
    "ultimate frisbee": "A non-contact team sport played with a flying disc (frisbee).",
    "disc golf": "A sport similar to golf but using flying discs aimed at baskets.",
    "quidditch": "A sport inspired by the Harry Potter books, played with brooms and a ball.",
    "sumo wrestling": "A Japanese combat sport where two wrestlers try to force each other out of a ring.",
    "capoeira": "A Brazilian martial art combining dance, acrobatics, and music.",
}
# Paste your big dict above this comment
# WORD_DICTIONARY = { "school": "A place ...", ... }

def check_spelling(user_input):
    blob = TextBlob(user_input)
    corrected = str(blob.correct())
    if corrected.lower() != user_input.lower():
        return f"Did you mean: {corrected}?"
    return None

def wiki_lookup(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return f"(From Wikipedia) {summary}"
    except Exception:
        return None


# ---------- 2) Safe load/save for conversation history ----------
def load_data():
    try:
        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = f.read().strip()
            if not raw:
                return []
            data = json.loads(raw)
            return data if isinstance(data, list) else [data]
    except Exception:
        # corrupt file -> rename and start fresh
        try:
            os.replace(DATA_FILE, DATA_FILE + ".bak")
        except Exception:
            pass
        return []

def save_data_entry(entry: dict):
    data = load_data()
    data.append(entry)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ---------- 3) Helpers to find reply in WORD_DICTIONARY ----------
# Precompute a lowercase-key map for speed
LOWER_KB = {}
try:
    for k, v in WORD_DICTIONARY.items():
        LOWER_KB[k.strip().lower()] = v
except NameError:
    LOWER_KB = {}

def find_in_kb(user_msg: str):
    if not LOWER_KB:
        return None
    msg = user_msg.strip().lower()

    # 1) exact match
    if msg in LOWER_KB:
        return LOWER_KB[msg]

    # 2) whole-word token match (if user typed extra words like "what is school")
    tokens = re.findall(r'\b[\w\-]+\b', msg)
    for t in tokens:
        if t in LOWER_KB:
            return LOWER_KB[t]

    # 3) substring match (fallback) - looks for KB key inside message
    # (use carefully; for many keys this may return first match)
    for k in LOWER_KB:
        if k in msg:
            return LOWER_KB[k]

    return None

# ---------- 4) Math helper (sympy preferred, else safe eval fallback) ----------
try:
    import sympy as sp
except Exception:
    sp = None

def try_solve_math(expr: str):
    s = expr.strip().replace('^', '**')
    # allow digits, operators, parentheses, decimals and spaces only
    if not re.match(r'^[0-9\.\s\+\-\*\/\^\(\)]+$', s):
        raise ValueError("not a safe math expression")
    if sp:
        try:
            r = sp.sympify(s)
            if getattr(r, "is_number", False):
                return str(r)
        except Exception:
            raise
    else:
        # safe eval fallback (globals/locals locked down)
        try:
            return str(eval(s, {"__builtins__": None}, {}))
        except Exception:
            raise

# ---------- 5) Respond function ----------
GREETINGS = {"hi","hello","hey","salam","assalam","asalam","good morning","good evening"}

import re

def respond(user_msg):
    msg = user_msg.strip().lower()

    # 1. Detect and solve math anywhere in the text
    math_expr = re.findall(r"[\d\+\-\*/\(\)\.]+", msg)  # find numbers and operators
    if math_expr:
        try:
            expr = "".join(math_expr)   # join pieces into expression
            result = eval(expr)
            return str(result)
        except:
            pass

    # 2. Check dictionary (your 700 words)
    if msg in WORD_DICTIONARY:
        return WORD_DICTIONARY[msg]

    # 3. Fallback
    return "Sorry, I don't know that yet."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_response():
    user_msg = request.args.get("msg", "")
    if not user_msg.strip():
        return "Please type something!"
    reply = respond(user_msg)

    # save conversation as consistent schema
    try:
        save_data_entry({"user": user_msg, "bot": reply})
    except Exception:
        pass

    return reply

@app.route("/view")
def view_data():
    return jsonify(load_data())

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)



