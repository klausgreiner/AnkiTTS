# 🎵 AnkiTTS - Complete Anki Learning Toolkit

A comprehensive toolkit for German language learning with Anki:

- **Anki Helper**: Generate vocabulary with Gemini AI and add TTS audio with ElevenLabs
- **Word Analyzer**: Analyze word frequency in your decks to focus on what matters most

## 🔧 Prerequisites

1. **Anki** - Make sure Anki is installed and running
2. **AnkiConnect Addon** - Required for communication between this tool and Anki
3. **Google Gemini API** - Get your API key from Google AI Studio
4. **ElevenLabs Account** - Get your API key and voice ID from ElevenLabs
5. **Python 3.7+** - Make sure Python is installed

### 📥 Installing AnkiConnect

AnkiConnect is essential for this tool to work. Here's how to install it:

1. **Open Anki** on your computer
2. **Go to Tools → Add-ons** (or press `Ctrl+Shift+A` / `Cmd+Shift+A`)
3. **Click "Get Add-ons..."**
4. **Enter the code:** `2055492159`
5. **Click "OK"** and wait for installation
6. **Restart Anki** completely
7. **Verify installation** by going to Tools → Add-ons and confirming "AnkiConnect" is listed

**Alternative method:**

- Visit: https://ankiweb.net/shared/info/2055492159
- Download the `.ankiaddon` file
- Double-click to install in Anki

## 📁 Project Structure

```
AnkiTTS/
├── anki_helper/          # TTS audio generation & card creation
│   ├── main.py           # Main TTS generator
│   ├── generate_anki_cards.py  # Create flashcards from word lists
│   └── requirements.txt  # Dependencies for anki_helper
│
├── word_analyzer/        # Word frequency analysis tools
│   ├── simple_word_analyzer.py    # Basic analyzer (no dependencies)
│   ├── visual_word_analyzer.py    # Advanced with graphs
│   ├── word_frequency_analyzer.py # Legacy version
│   ├── requirements.txt  # Dependencies for visualizations
│   └── german.txt        # Your Anki deck for analysis
│
├── examples/             # Example files and outputs
│   ├── example_word_list.txt
│   ├── food_words.txt
│   └── *.txt (generated cards)
│
├── data/                 # Analysis output files
│   ├── german_word_frequency.json
│   ├── german_word_frequency.csv
│   ├── german_word_frequency.txt
│   └── german_word_frequency_analysis.png
│
└── venv/                 # Python virtual environment
```

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/selmetwa/AnkiTTS.git
cd AnkiTTS

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies (choose based on what you need)
pip install -r anki_helper/requirements.txt    # For TTS and card generation
pip install -r word_analyzer/requirements.txt  # For word frequency analysis
```

## 🚀 Usage

**⚠️ IMPORTANT: Always activate the virtual environment first!**

```bash
# Activate virtual environment (from project root)
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

### 1. Anki Helper (TTS & Card Generation)

```bash
# Make sure venv is activated first!
cd anki_helper

# Generate TTS audio for existing cards
python3 main.py

# Create new flashcards from word lists
python3 generate_anki_cards.py --create-example  # Create example template
python3 generate_anki_cards.py --word-list ../examples/food_words.txt --output new_cards.txt

# Generate from most frequent words
python3 generate_anki_cards.py --frequency-json ../data/german_word_frequency.json --top-n 30 --output cards.txt
```

### Quick One-Liners (from project root)

```bash
# Activate venv and run main.py
source venv/bin/activate && cd anki_helper && python3 main.py

# Activate venv and analyze words
source venv/bin/activate && cd word_analyzer && python3 visual_word_analyzer.py german.txt
```

### 2. Word Analyzer (Find What to Study)

```bash
cd word_analyzer

# Simple analysis (no dependencies)
python3 simple_word_analyzer.py german.txt --top-n 30

# Advanced analysis with graphs
python3 visual_word_analyzer.py german.txt --top-n 30

# Output files go to ../data/
```

### Quick Workflow Example

```bash
# Step 1: Analyze your deck to find common words
cd word_analyzer
python3 visual_word_analyzer.py german.txt --top-n 50

# Step 2: Generate practice cards for top words
cd ../anki_helper
python3 generate_anki_cards.py \
  --frequency-json ../data/german_word_frequency.json \
  --output ../examples/practice_cards.txt \
  --top-n 20 \
  --include-phrases

# Step 3: Add TTS audio to all your cards
python3 main.py
```

### Main TTS Tool Features

When you run `python3 main.py`, the CLI guides you through:

1. **Anki Setup Check** - Verify Anki is running with AnkiConnect
2. **Deck Selection** - Choose which Anki deck to process
3. **Field Configuration** - Select text and audio fields
4. **API Setup** - Enter your Gemini and ElevenLabs API keys
5. **Choose Action**:
   - Generate German content with Gemini
   - Add TTS audio to existing cards
   - Both (generate content + add audio)

## 📋 What You'll Need

- **Gemini API Key**: Your Google Gemini API key from [AI Studio](https://aistudio.google.com/)
- **ElevenLabs API Key**: Your ElevenLabs API key from [ElevenLabs](https://elevenlabs.io/)
- **Voice ID**: The ElevenLabs voice ID you want to use
- **Language Code**: e.g., 'de' for German, 'en' for English

### Optional Configuration (.env file)

Create a `.env` file in `anki_helper/` directory:

```bash
cp anki_helper/env.example anki_helper/.env
# Edit with your API keys
```

The script will automatically load these values and skip prompts.

## 🎯 Features

### Anki Helper

- ✅ **TTS Audio Generation** - Add natural-sounding speech to cards with ElevenLabs
- ✅ **Content Generation** - Generate German vocabulary with Gemini AI
- ✅ **Card Creation** - Create flashcards from word lists or frequency analysis
- ✅ **Practice Phrases** - Automatically generate example sentences
- ✅ **Smart Processing** - Skip cards that already have audio
- ✅ **Progress Tracking** - Visual progress bars

### Word Analyzer

- ✅ **Frequency Analysis** - Find the most common words in your deck
- ✅ **Visual Graphs** - Beautiful charts showing word distribution
- ✅ **Multiple Formats** - Export to JSON, CSV, TXT, PNG
- ✅ **Stop Word Filtering** - Automatically removes common German articles/prepositions
- ✅ **Zero Dependencies Option** - Simple analyzer works without any packages

## 🔧 Troubleshooting

**"Cannot connect to Anki"**

- Make sure Anki is running
- Install AnkiConnect addon: https://ankiweb.net/shared/info/2055492159
- Restart Anki after installing the addon

**"ElevenLabs API Error"**

- Check your API key is correct
- Verify your voice ID exists
- Make sure you have sufficient API credits

## 📝 Example Usage

```
🎵 ANKI AUDIO GENERATOR 🎵
    Automatically add TTS audio to your Anki cards
============================================================

🔍 Step 1: Checking Anki Setup
========================================
Please make sure Anki is running on your computer.
Press Enter when Anki is open and ready...
✅ Anki is running (AnkiConnect version 6)

🛠️  Step 2: Configuration
========================================
Available decks:
  1. Spanish Vocabulary
  2. Arabic Colors
  3. French Verbs

Enter deck name (or number from list above): 2
✅ Selected deck: Arabic Colors

Available fields in 'Arabic Colors':
  1. Front
  2. Back
  3. Audio

Enter field name containing text to read (or number): 1
Enter field name where audio should be added (or number): 1

🎤 ElevenLabs Configuration
==============================
Enter your ElevenLabs API key: sk_...
Enter ElevenLabs voice ID: nPczCjzI2devNBz1zQrb
Enter language code (e.g., 'ar' for Arabic, 'en' for English) [en]: ar

📋 Configuration Summary
==============================
Deck: Arabic Colors
Text field: Front
Audio field: Front
Voice ID: nPczCjzI2devNBz1zQrb
Language: ar

Is this configuration correct? (y/n): y
✅ ElevenLabs client initialized successfully

🎵 Step 3: Processing Deck 'Arabic Colors'
==================================================
✅ Found 25 cards in deck
Processing cards: 100%|████████████| 25/25 [00:45<00:00,  1.82s/it]

🎉 Processing Complete!
==============================
✅ Successfully processed: 25 cards
⚠️  Skipped: 0 cards
❌ Errors: 0 cards

🎉 All done! Your Anki cards now have audio!
```
