# தமிழ் கற்போம் — Learn Tamil (Flask + gTTS)

A Tamil alphabet learning web app built with **Python Flask** and **gTTS (Google Text-to-Speech)**.  
Covers all Tamil letters with speech pronunciation — free, no API key needed.

---

## 📁 File Path Map

```
tamil_learn/
│
├── app.py                    ← Flask server + all Tamil letter/number data + /speak route
├── requirements.txt          ← Python dependencies (flask, gtts)
├── README.md                 ← This file
│
├── templates/
│   └── index.html            ← Main HTML page (Jinja2 template)
│
└── static/
    ├── css/
    │   └── style.css         ← All styles (light green theme, matrix table, cards)
    └── js/
        └── main.js           ← Card rendering, matrix table, gTTS speech, tabs
```

---

## ⚙️ Install Steps

### 1. Prerequisites
- Python 3.8 or higher
- `pip` available in terminal
- **Internet connection** on the machine running Flask (gTTS calls Google internally)

### 2. Enter the project folder
```bash
cd tamil_learn
```

### 3. Create a virtual environment (recommended)
```bash
python -m venv tam
```

Activate it:
- **Windows:**    `tam\Scripts\activate`
- **macOS/Linux:** `source tam/bin/activate`

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the app
```bash
python app.py
```

### 6. Open in browser
```
http://127.0.0.1:5000
```

---

## 🔊 How Speech Works (gTTS)

```
Browser clicks 🔊 on any card or matrix cell
    → JavaScript calls  GET /speak?text=அம்மா
    → Flask runs gTTS(text, lang="ta") in Python
    → gTTS contacts Google TTS internally → returns MP3
    → Flask sends MP3 to browser
    → Browser plays audio instantly
```

- ✅ 100% Free — no API key, no account needed
- ✅ Excellent Tamil pronunciation
- ✅ Works for single letters, combined letters, words, numbers
- ⚠️ Requires internet on the server machine (gTTS contacts Google)
- ⚠️ First request may take 1–2 seconds (network call)

---

## 📚 Content Covered

| Tab | Tamil Name | Content | Count |
|-----|-----------|---------|-------|
| Vowels | உயிர் எழுத்துக்கள் | ஃ Aayutham + 12 vowels | **13** |
| Consonants | மெய் எழுத்துக்கள் | Pure consonants | **18** |
| Combined | உயிர்மெய் எழுத்துக்கள் | Matrix table 18 × 12 | **216** |
| Numbers | தமிழ் எண்கள் | Tamil numerals + Arabic + Tamil word | **13** |

### Vowels — colour coding
| Colour | Meaning |
|--------|---------|
| 🟣 Purple top border | ஃ Aayutham (special, 13th vowel) |
| 🔵 Blue top border | குறில் — Short vowel |
| 🟠 Orange top border | நெடில் — Long vowel |

### உயிர்மெய் Matrix Layout
- **Rows** = 18 மெய் consonants (pink background)
- **Columns** = 12 உயிர் vowels (green header)
- **Corner cell** = ஃ (ak)
- **Border thickness** = 4px throughout
- **Table** = centered on page
- **Spellings** = phonetic prefixes (Ng, Gn, Zh, Th...) and suffixes (a, aa, i, ee...)
- Click any cell → speaks that combined letter

---

## 🎨 Design Spec

| Property | Value |
|----------|-------|
| Body background | Light green `#e8f5e9` |
| Cards | White `#ffffff` |
| Text | Black `#111111` |
| Speech icon | Black `#111111` |
| Subtitle format | `English (தமிழ்)` |
| Font (Tamil) | Baloo Thambi 2 |
| Font (UI) | Nunito |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3 + Flask |
| Speech | gTTS (Google Text-to-Speech, free) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Data API | Flask `/api/data` → JSON |
| Speech API | Flask `/speak?text=...` → MP3 |
| Fonts | Google Fonts (Baloo Thambi 2, Nunito) |

---

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves the main HTML page |
| `/api/data` | GET | Returns all Tamil letter data as JSON |
| `/speak?text=அ` | GET | Returns MP3 audio for the given Tamil text |

---

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| No sound when clicking 🔊 | Check internet connection on the server machine |
| `gTTS error` toast appears | Run `pip install --upgrade gtts` |
| Tamil letters not displaying | Use Chrome, Firefox, or Edge (modern browser) |
| Port already in use | Change port: `app.run(debug=True, port=5001)` in `app.py` |