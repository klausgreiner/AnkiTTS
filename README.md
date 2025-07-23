# 🎵 Anki Audio Generator CLI

A command-line tool to automatically generate and add text-to-speech audio to your Anki cards using ElevenLabs TTS.

## 🔧 Prerequisites

1. **Anki** - Make sure Anki is installed and running
2. **AnkiConnect Addon** - Install from: https://ankiweb.net/shared/info/2055492159
3. **ElevenLabs Account** - Get your API key and voice ID from ElevenLabs
4. **Python 3.7+** - Make sure Python is installed

## 📦 Installation

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/selmetwa/AnkiTTS.git
   cd AnkiTTS
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate it
   source venv/bin/activate  # On macOS/Linux
   # OR
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### For first-time setup:
```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py
```

### For subsequent runs:
```bash
source venv/bin/activate && python main.py
```

The CLI will guide you through:

1. **Anki Setup Check** - Verify Anki is running with AnkiConnect
2. **Deck Selection** - Choose which Anki deck to process
3. **Field Configuration** - Select text and audio fields
4. **ElevenLabs Setup** - Enter your API key, voice ID, and language
5. **Processing** - Watch as audio is generated and added to your cards

## 📋 What You'll Need

- **Deck Name**: The name of your Anki deck
- **Text Field**: The field containing text to convert to speech
- **Audio Field**: Where to store the generated audio (can be same as text field)
- **ElevenLabs API Key**: Your ElevenLabs API key
- **Voice ID**: The ElevenLabs voice ID you want to use
- **Language Code**: e.g., 'ar' for Arabic, 'en' for English

## 🎯 Features

- ✅ Interactive CLI with step-by-step guidance
- ✅ Automatic deck and field detection
- ✅ Support for all ElevenLabs voices and languages
- ✅ Skip cards that already have audio
- ✅ Progress tracking with tqdm
- ✅ Error handling and recovery
- ✅ Support for appending audio to text or separate fields

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
