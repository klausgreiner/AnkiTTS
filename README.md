# 🎵 Anki Audio & Content Generator CLI

A command-line tool to generate German vocabulary using Gemini AI and add text-to-speech audio to your Anki cards using ElevenLabs TTS.

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

4. **Create .env file (optional but recommended)**
   ```bash
   cp env.example .env
   # Edit .env with your API keys and configuration
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
4. **API Setup** - Enter your Gemini and ElevenLabs API keys
5. **Menu Selection** - Choose what you want to do:
   - Generate German content with Gemini
   - Add audio to existing cards
   - Both (generate content + add audio)

## 📋 What You'll Need

- **Gemini API Key**: Your Google Gemini API key from [AI Studio](https://aistudio.google.com/)
- **ElevenLabs API Key**: Your ElevenLabs API key from [ElevenLabs](https://elevenlabs.io/)
- **Voice ID**: The ElevenLabs voice ID you want to use
- **Language Code**: e.g., 'de' for German, 'en' for English

### Optional (can be set in .env file):

- **Deck Name**: The name of your Anki deck
- **Text Field**: The field containing text to convert to speech
- **Audio Field**: Where to store the generated audio (can be same as text field)

## 🔧 Configuration

### Using .env file (Recommended)

Create a `.env` file in the project directory with your configuration:

```bash
# Copy the example file
cp env.example .env

# Edit with your values
nano .env
```

Example `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=your_voice_id_here
LANGUAGE_CODE=de
ANKI_DECK_NAME=German Vocabulary
TEXT_FIELD=Front
AUDIO_FIELD=Front
```

If you use a `.env` file, the script will automatically load these values and skip the interactive prompts for those settings.

## 🎯 Features

- ✅ **German Content Generation** - Generate German words and phrases using Gemini AI
- ✅ **Deck Analysis** - Analyze existing deck content to avoid duplicates
- ✅ **Topic-based Generation** - Generate vocabulary for specific topics
- ✅ **Interactive CLI** - Step-by-step guidance with menu system
- ✅ **Automatic Detection** - Deck and field detection
- ✅ **Audio Generation** - Support for all ElevenLabs voices and languages
- ✅ **Smart Processing** - Skip cards that already have audio
- ✅ **Progress Tracking** - Visual progress bars with tqdm
- ✅ **Error Handling** - Robust error handling and recovery
- ✅ **Flexible Fields** - Support for appending audio to text or separate fields

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
