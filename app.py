from flask import Flask, render_template, jsonify, request, send_file, Response
from gtts import gTTS
import io

app = Flask(__name__)

# ══════════════════════════════════════════════════════════════
#  உயிர் எழுத்துக்கள் — 12 Vowels + ஃ Aayutham = 13
#  (ஃ shown under Uyir page as per school curriculum)
# ══════════════════════════════════════════════════════════════
UYIR = [
    {"ta": "அ",  "en": "A",   "roman": "a",   "sub_ta": "குறில்",  "speak": "அ"},
    {"ta": "ஆ",  "en": "Aa",  "roman": "aa",  "sub_ta": "நெடில்",  "speak": "ஆ"},
    {"ta": "இ",  "en": "E",   "roman": "i",   "sub_ta": "குறில்",  "speak": "இ"},
    {"ta": "ஈ",  "en": "Ee",  "roman": "ii",  "sub_ta": "நெடில்",  "speak": "ஈ"},
    {"ta": "உ",  "en": "U",   "roman": "u",   "sub_ta": "குறில்",  "speak": "உ"},
    {"ta": "ஊ",  "en": "Oo",  "roman": "uu",  "sub_ta": "நெடில்",  "speak": "ஊ"},
    {"ta": "எ",  "en": "Ye",  "roman": "e",   "sub_ta": "குறில்",  "speak": "எ"},
    {"ta": "ஏ",  "en": "Yae", "roman": "ee",  "sub_ta": "நெடில்",  "speak": "ஏ"},
    {"ta": "ஐ",  "en": "I",   "roman": "ai",  "sub_ta": "குறில்",  "speak": "ஐ"},
    {"ta": "ஒ",  "en": "O",   "roman": "o",   "sub_ta": "குறில்",  "speak": "ஒ"},
    {"ta": "ஓ",  "en": "Oa",  "roman": "oo",  "sub_ta": "நெடில்",  "speak": "ஓ"},
    {"ta": "ஔ",  "en": "Ow",  "roman": "au",  "sub_ta": "நெடில்",  "speak": "ஔ"},
    # 13th — ஃ Aayutha Ezhuthu placed after Ow as requested
    {"ta": "ஃ",  "en": "ak",  "roman": "ak",  "sub_ta": "ஆயுதம்", "speak": "அக்", "is_aayutham": True},
]

# ══════════════════════════════════════════════════════════════
#  Vowel header row for the matrix (12 vowels only, no ஃ)
# ══════════════════════════════════════════════════════════════
VOWEL_HEADERS = [
    {"ta": "அ",  "en": "A",   "speak": "அ"},
    {"ta": "ஆ",  "en": "Aa",  "speak": "ஆ"},
    {"ta": "இ",  "en": "E",   "speak": "இ"},
    {"ta": "ஈ",  "en": "Ee",  "speak": "ஈ"},
    {"ta": "உ",  "en": "U",   "speak": "உ"},
    {"ta": "ஊ",  "en": "Oo",  "speak": "ஊ"},
    {"ta": "எ",  "en": "Ye",  "speak": "எ"},
    {"ta": "ஏ",  "en": "Yae", "speak": "ஏ"},
    {"ta": "ஐ",  "en": "I",   "speak": "ஐ"},
    {"ta": "ஒ",  "en": "O",   "speak": "ஒ"},
    {"ta": "ஓ",  "en": "Oa",  "speak": "ஓ"},
    {"ta": "ஔ",  "en": "Ow",  "speak": "ஔ"},
]

# ══════════════════════════════════════════════════════════════
#  மெய் எழுத்துக்கள் — 18 Consonants (rows)
# ══════════════════════════════════════════════════════════════
# (base, mei_form, roman, speak_text)
CONSONANT_ROWS = [
    ("க",  "க்",  "K",   "Ik",  "இக்"),
    ("ங",  "ங்",  "Ng",  "Ing", "இங்"),
    ("ச",  "ச்",  "Ch",  "Ich", "இச்"),
    ("ஞ",  "ஞ்",  "Gn",  "Inj", "இஞ்"),
    ("ட",  "ட்",  "T",   "It",  "இட்"),
    ("ண",  "ண்",  "N",   "In",  "இண்"),
    ("த",  "த்",  "Th",  "Ith", "இத்"),
    ("ந",  "ந்",  "N",   "Inth","இந்த்"),
    ("ப",  "ப்",  "P",   "Ip",  "இப்"),
    ("ம",  "ம்",  "M",   "Im",  "இம்"),
    ("ய",  "ய்",  "Y",   "Iy",  "இய்"),
    ("ர",  "ர்",  "R",   "Ir",  "இர்"),
    ("ல",  "ல்",  "L",   "Il",  "இல்"),
    ("வ",  "வ்",  "V",   "Iv",  "இவ்"),
    ("ழ",  "ழ்",  "Zh",  "Izh", "இழ்"),
    ("ள",  "ள்",  "L",   "Il",  "இள்"),
    ("ற",  "ற்",  "R",   "Ir",  "இற்"),
    ("ன",  "ன்",  "N",   "In",  "இன்"),
]

# ══════════════════════════════════════════════════════════════
#  உயிர்மெய் matrix — maatraa map (proper Unicode)
# ══════════════════════════════════════════════════════════════
MAATRA = {
    "அ":  "",
    "ஆ":  "ா",
    "இ":  "ி",
    "ஈ":  "ீ",
    "உ":  "ு",
    "ஊ":  "ூ",
    "எ":  "ெ",
    "ஏ":  "ே",
    "ஐ":  "ை",
    "ஒ":  "ொ",
    "ஓ":  "ோ",
    "ஔ":  "ௌ",
}

VOW_EN = {
    "அ":"A","ஆ":"Aa","இ":"E","ஈ":"Ee","உ":"U","ஊ":"Oo",
    "எ":"Ye","ஏ":"Yae","ஐ":"I","ஒ":"O","ஓ":"Oa","ஔ":"Ow"
}

VOWEL_SUFFIXES = {
    "அ": "a",  "ஆ": "aa", "இ": "i",  "ஈ": "ee",
    "உ": "u",  "ஊ": "oo", "எ": "e",  "ஏ": "ae",
    "ஐ": "ai", "ஒ": "o",  "ஓ": "oa", "ஔ": "ou"
}

def build_matrix():
    """
    Returns list of rows. Each row = {mei, roman_row, en_row, speak_mei, cells:[]}
    Each cell = {ta, en, speak}
    """
    rows = []
    for base, mei, roman, en_row, speak_mei in CONSONANT_ROWS:
        cells = []
        for vh in VOWEL_HEADERS:
            vow = vh["ta"]
            letter = base + MAATRA[vow]
            
            # English pronunciation like the image: Ka, Kaa, Ki, Kee...
            suffix = VOWEL_SUFFIXES[vow]
            en_cell = roman + suffix
            
            cells.append({
                "ta":    letter,
                "en":    en_cell,
                "speak": letter,
            })
        rows.append({
            "mei":       mei,
            "roman_row": roman,
            "en_row":    en_row,
            "speak_mei": speak_mei,
            "cells":     cells,
        })
    return rows

MATRIX = build_matrix()

# MEI flat list for the Mei tab cards
MEI = [
    {
        "ta":     mei,
        "en":     en_row,
        "roman":  roman,
        "sub_ta": "மெய்",
        "speak":  speak_mei,
    }
    for base, mei, roman, en_row, speak_mei in CONSONANT_ROWS
]

# ══════════════════════════════════════════════════════════════
#  தமிழ் எண்கள் — Tamil Numbers
# ══════════════════════════════════════════════════════════════
NUMBERS = [
    {"ta": "௦", "num": "0",    "en": "Zero",     "sub_ta": "சுழியம்",  "speak": "சுழியம்"},
    {"ta": "௧", "num": "1",    "en": "One",      "sub_ta": "ஒன்று",    "speak": "ஒன்று"},
    {"ta": "௨", "num": "2",    "en": "Two",      "sub_ta": "இரண்டு",   "speak": "இரண்டு"},
    {"ta": "௩", "num": "3",    "en": "Three",    "sub_ta": "மூன்று",   "speak": "மூன்று"},
    {"ta": "௪", "num": "4",    "en": "Four",     "sub_ta": "நான்கு",   "speak": "நான்கு"},
    {"ta": "௫", "num": "5",    "en": "Five",     "sub_ta": "ஐந்து",    "speak": "ஐந்து"},
    {"ta": "௬", "num": "6",    "en": "Six",      "sub_ta": "ஆறு",      "speak": "ஆறு"},
    {"ta": "௭", "num": "7",    "en": "Seven",    "sub_ta": "ஏழு",      "speak": "ஏழு"},
    {"ta": "௮", "num": "8",    "en": "Eight",    "sub_ta": "எட்டு",    "speak": "எட்டு"},
    {"ta": "௯", "num": "9",    "en": "Nine",     "sub_ta": "ஒன்பது",   "speak": "ஒன்பது"},
    {"ta": "௰", "num": "10",   "en": "Ten",      "sub_ta": "பத்து",    "speak": "பத்து"},
    {"ta": "௱", "num": "100",  "en": "Hundred",  "sub_ta": "நூறு",     "speak": "நூறு"},
    {"ta": "௲", "num": "1000", "en": "Thousand", "sub_ta": "ஆயிரம்",   "speak": "ஆயிரம்"},
]


# ══════════════════════════════════════════════════════════════
#  ROUTES
# ══════════════════════════════════════════════════════════════
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/data")
def get_data():
    return jsonify({
        "uyir":    UYIR,
        "mei":     MEI,
        "matrix":  MATRIX,
        "vowel_headers": VOWEL_HEADERS,
        "numbers": NUMBERS,
    })


@app.route("/speak")
def speak():
    """
    GET /speak?text=அம்மா
    Returns Tamil MP3 via gTTS — free, no API key, server-side (no CORS).
    """
    text = request.args.get("text", "").strip()
    if not text:
        return Response("No text", status=400)
    try:
        tts = gTTS(text=text, lang="ta", slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return send_file(buf, mimetype="audio/mpeg",
                         as_attachment=False,
                         download_name="speech.mp3")
    except Exception as e:
        return Response(f"gTTS error: {e}", status=500)


if __name__ == "__main__":
    app.run(debug=True)
