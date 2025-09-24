#!/usr/bin/env python3
"""
Anki Audio & Content Generator CLI
A command-line tool to generate German vocabulary using Gemini AI and add TTS audio to Anki cards using ElevenLabs.
"""

import requests
import base64
import time
import re
import json
import os
from tqdm import tqdm
from elevenlabs.client import ElevenLabs
import google.generativeai as genai
from dotenv import load_dotenv


class AnkiAudioGenerator:
    def __init__(self):
        self.elevenlabs_client = None
        self.gemini_client = None
        self.config = {}

    def print_banner(self):
        """Print welcome banner"""
        print("=" * 60)
        print("        🎵 ANKI AUDIO & CONTENT GENERATOR 🎵")
        print("  Generate German content with Gemini + TTS audio")
        print("=" * 60)
        print()

    def check_anki_running(self):
        """Check if Anki is running and AnkiConnect is available"""
        print("🔍 Step 1: Checking Anki Setup")
        print("=" * 40)

        # Check if Anki is running
        print("Please make sure Anki is running on your computer.")
        input("Press Enter when Anki is open and ready... ")

        # Test AnkiConnect connection
        try:
            response = requests.post(
                "http://localhost:8765",
                json={"action": "version", "version": 6},
                timeout=5,
            )
            result = response.json()

            if result.get("error"):
                print(f"❌ AnkiConnect error: {result['error']}")
                return False

            print(
                f"✅ Anki is running (AnkiConnect version {result.get('result', 'unknown')})"
            )
            return True

        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to Anki. Please make sure:")
            print("   1. Anki is running")
            print("   2. AnkiConnect addon is installed")
            print(
                "   3. AnkiConnect addon URL: https://ankiweb.net/shared/info/2055492159"
            )
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False

    def get_anki_decks(self):
        """Get list of available Anki decks"""
        try:
            response = requests.post(
                "http://localhost:8765", json={"action": "deckNames", "version": 6}
            )
            result = response.json()
            return result.get("result", [])
        except:
            return []

    def get_deck_fields(self, deck_name):
        """Get available fields for a deck"""
        try:
            # Get a sample note from the deck
            response = requests.post(
                "http://localhost:8765",
                json={
                    "action": "findNotes",
                    "version": 6,
                    "params": {"query": f'deck:"{deck_name}"'},
                },
            )
            note_ids = response.json().get("result", [])

            if not note_ids:
                return []

            # Get note info for the first note
            response = requests.post(
                "http://localhost:8765",
                json={
                    "action": "notesInfo",
                    "version": 6,
                    "params": {"notes": [note_ids[0]]},
                },
            )
            notes = response.json().get("result", [])

            if notes:
                return list(notes[0]["fields"].keys())
            return []
        except:
            return []

    def load_env_config(self):
        """Load configuration from .env file if it exists"""
        load_dotenv()

        env_config = {}
        if os.getenv("GEMINI_API_KEY"):
            env_config["gemini_api_key"] = os.getenv("GEMINI_API_KEY")
        if os.getenv("ELEVENLABS_API_KEY"):
            env_config["api_key"] = os.getenv("ELEVENLABS_API_KEY")
        if os.getenv("ELEVENLABS_VOICE_ID"):
            env_config["voice_id"] = os.getenv("ELEVENLABS_VOICE_ID")
        if os.getenv("LANGUAGE_CODE"):
            env_config["language_code"] = os.getenv("LANGUAGE_CODE")
        if os.getenv("ANKI_DECK_NAME"):
            env_config["deck_name"] = os.getenv("ANKI_DECK_NAME")
        if os.getenv("TEXT_FIELD"):
            env_config["text_field"] = os.getenv("TEXT_FIELD")
        if os.getenv("AUDIO_FIELD"):
            env_config["audio_field"] = os.getenv("AUDIO_FIELD")

        return env_config

    def collect_configuration(self):
        """Collect all configuration from user"""
        print("\n🛠️  Step 2: Configuration")
        print("=" * 40)

        # Load from .env file first
        env_config = self.load_env_config()
        if env_config:
            print("📁 Found configuration in .env file")
            for key in env_config:
                self.config[key] = env_config[key]

        # Get deck name
        if not self.config.get("deck_name"):
            decks = self.get_anki_decks()
            if decks:
                print("Available decks:")
                for i, deck in enumerate(decks, 1):
                    print(f"  {i}. {deck}")
                print()

                while True:
                    deck_input = input(
                        "Enter deck name (or number from list above): "
                    ).strip()

                    # Check if it's a number
                    if deck_input.isdigit():
                        idx = int(deck_input) - 1
                        if 0 <= idx < len(decks):
                            self.config["deck_name"] = decks[idx]
                            break
                        else:
                            print("❌ Invalid number. Please try again.")
                            continue

                    # Check if it's a deck name
                    if deck_input in decks:
                        self.config["deck_name"] = deck_input
                        break
                    else:
                        print("❌ Deck not found. Please try again.")
            else:
                self.config["deck_name"] = input("Enter Anki deck name: ").strip()
        else:
            print(f"📁 Using deck from .env: {self.config['deck_name']}")

        print(f"✅ Selected deck: {self.config['deck_name']}")

        # Get available fields for the selected deck
        if not self.config.get("text_field") or not self.config.get("audio_field"):
            fields = self.get_deck_fields(self.config["deck_name"])
            if fields:
                print(f"\nAvailable fields in '{self.config['deck_name']}':")
                for i, field in enumerate(fields, 1):
                    print(f"  {i}. {field}")
                print()

                # Get text field
                if not self.config.get("text_field"):
                    while True:
                        text_field_input = input(
                            "Enter field name containing text to read (or number): "
                        ).strip()

                        if text_field_input.isdigit():
                            idx = int(text_field_input) - 1
                            if 0 <= idx < len(fields):
                                self.config["text_field"] = fields[idx]
                                break
                            else:
                                print("❌ Invalid number. Please try again.")
                                continue

                        if text_field_input in fields:
                            self.config["text_field"] = text_field_input
                            break
                        else:
                            print("❌ Field not found. Please try again.")
                else:
                    print(f"📁 Using text field from .env: {self.config['text_field']}")

                # Get audio field
                if not self.config.get("audio_field"):
                    while True:
                        audio_field_input = input(
                            "Enter field name where audio should be added (or number): "
                        ).strip()

                        if audio_field_input.isdigit():
                            idx = int(audio_field_input) - 1
                            if 0 <= idx < len(fields):
                                self.config["audio_field"] = fields[idx]
                                break
                            else:
                                print("❌ Invalid number. Please try again.")
                                continue

                        if audio_field_input in fields:
                            self.config["audio_field"] = audio_field_input
                            break
                        else:
                            print("❌ Field not found. Please try again.")
                else:
                    print(
                        f"📁 Using audio field from .env: {self.config['audio_field']}"
                    )
            else:
                if not self.config.get("text_field"):
                    self.config["text_field"] = input(
                        "Enter field name containing text to read: "
                    ).strip()
                if not self.config.get("audio_field"):
                    self.config["audio_field"] = input(
                        "Enter field name where audio should be added: "
                    ).strip()
        else:
            print(
                f"📁 Using fields from .env: text='{self.config['text_field']}', audio='{self.config['audio_field']}'"
            )

        # Get Gemini configuration
        print("\n🤖 Gemini Configuration")
        print("=" * 30)

        if not self.config.get("gemini_api_key"):
            self.config["gemini_api_key"] = input(
                "Enter your Google Gemini API key: "
            ).strip()
        else:
            print("📁 Using Gemini API key from .env")

        # Get ElevenLabs configuration
        print("\n🎤 ElevenLabs Configuration")
        print("=" * 30)

        if not self.config.get("api_key"):
            self.config["api_key"] = input("Enter your ElevenLabs API key: ").strip()
        else:
            print("📁 Using ElevenLabs API key from .env")

        if not self.config.get("voice_id"):
            self.config["voice_id"] = input(
                "Enter ElevenLabs voice ID (The voice you want to use to read the text): "
            ).strip()
        else:
            print(f"📁 Using voice ID from .env: {self.config['voice_id']}")

        # Language code with default
        if not self.config.get("language_code"):
            language_code = input(
                "Enter language code (Language code (ISO 639-1)  e.g., 'ar' for Arabic, 'en' for English) [en]: "
            ).strip()
            self.config["language_code"] = language_code if language_code else "en"
        else:
            print(f"📁 Using language code from .env: {self.config['language_code']}")

        # Show configuration summary
        print("\n📋 Configuration Summary")
        print("=" * 30)
        print(f"Deck: {self.config['deck_name']}")
        print(f"Text field: {self.config['text_field']}")
        print(f"Audio field: {self.config['audio_field']}")
        print(
            f"Gemini API: {'✅ Configured' if self.config['gemini_api_key'] else '❌ Not configured'}"
        )
        print(
            f"ElevenLabs API: {'✅ Configured' if self.config['api_key'] else '❌ Not configured'}"
        )
        print(f"Voice ID: {self.config['voice_id']}")
        print(f"Language: {self.config['language_code']}")
        print()

        confirm = input("Is this configuration correct? (y/n): ").strip().lower()
        if confirm != "y":
            print("❌ Configuration cancelled. Please restart the program.")
            return False

        return True

    def initialize_elevenlabs(self):
        """Initialize ElevenLabs client"""
        try:
            self.elevenlabs_client = ElevenLabs(api_key=self.config["api_key"])
            print("✅ ElevenLabs client initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize ElevenLabs client: {e}")
            return False

    def initialize_gemini(self):
        """Initialize Gemini client"""
        try:
            genai.configure(api_key=self.config["gemini_api_key"])
            # Use the correct model name for the current API version
            self.gemini_client = genai.GenerativeModel("gemini-2.0-flash-001")
            print("✅ Gemini client initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize Gemini client: {e}")
            return False

    def call_ankiconnect(self, action, params):
        """Call AnkiConnect with error handling"""
        try:
            response = requests.post(
                "http://localhost:8765",
                json={"action": action, "version": 6, "params": params},
                timeout=10,
            )
            result = response.json()

            if result.get("error"):
                print(f"AnkiConnect error for action '{action}': {result['error']}")
                return None

            return result
        except Exception as e:
            print(f"ERROR: Unexpected error calling AnkiConnect: {e}")
            return None

    def extract_text_from_field(self, field_value):
        """Extract actual text content from a field, removing any [sound:...] tags"""
        clean_text = re.sub(r"\[sound:[^\]]+\]", "", field_value).strip()
        return clean_text

    def generate_audio_bytes(self, text):
        """Generate audio from text using ElevenLabs"""
        if not text or not text.strip():
            return None

        try:
            audio_generator = self.elevenlabs_client.text_to_speech.convert(
                text=text,
                voice_id=self.config["voice_id"],
                model_id="eleven_turbo_v2_5",
                output_format="mp3_44100_128",
                language_code=self.config["language_code"],
                voice_settings={
                    "stability": 0.8,
                    "similarity_boost": 0.75,
                },
            )

            # Convert generator to bytes
            audio_bytes = b"".join(audio_generator)
            return audio_bytes

        except Exception as e:
            print(f"ERROR: Failed to generate audio for '{text}': {e}")
            return None

    def update_note_with_audio(self, note, audio_bytes, filename):
        """Update Anki note with audio file"""
        try:
            # Store the audio file
            encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")

            store_response = self.call_ankiconnect(
                "storeMediaFile", {"filename": filename, "data": encoded_audio}
            )

            if store_response is None or store_response.get("error"):
                return False

            # Get current field content
            current_content = note["fields"][self.config["audio_field"]]["value"]

            # Create new content
            if self.config["audio_field"] == self.config["text_field"]:
                # Same field: append audio to text
                clean_text = self.extract_text_from_field(current_content)
                new_content = f"{clean_text} [sound:{filename}]"
            else:
                # Different field: just add audio
                new_content = f"[sound:{filename}]"

            # Update the field
            response = self.call_ankiconnect(
                "updateNoteFields",
                {
                    "note": {
                        "id": note["noteId"],
                        "fields": {self.config["audio_field"]: new_content},
                    }
                },
            )

            return response is not None and not response.get("error")

        except Exception as e:
            print(f"ERROR: Exception while updating note {note['noteId']}: {e}")
            return False

    def analyze_deck_content(self):
        """Analyze current deck content and return summary for Gemini"""
        try:
            # Get notes from deck
            result = self.call_ankiconnect(
                "findNotes", {"query": f'deck:"{self.config["deck_name"]}"'}
            )
            if not result:
                return "No existing content found in deck."

            note_ids = result.get("result", [])
            if not note_ids:
                return "No existing content found in deck."

            # Get note information
            result = self.call_ankiconnect("notesInfo", {"notes": note_ids})
            if not result:
                return "Could not retrieve deck content."

            notes = result.get("result", [])

            # Extract text content
            existing_words = []
            for note in notes[:50]:  # Limit to first 50 notes for context
                try:
                    raw_field_value = note["fields"][self.config["text_field"]]["value"]
                    word = self.extract_text_from_field(raw_field_value)
                    if word and word.strip():
                        existing_words.append(word.strip())
                except:
                    continue

            # Create summary for Gemini
            summary = f"Current deck contains {len(notes)} cards with these sample words/phrases: {', '.join(existing_words[:20])}"
            if len(existing_words) > 20:
                summary += f" (and {len(existing_words) - 20} more)"

            return summary

        except Exception as e:
            print(f"Warning: Could not analyze deck content: {e}")
            return "Could not analyze existing deck content."

    def generate_german_content(
        self, topic, num_words, num_phrases, existing_content=""
    ):
        """Generate German words and phrases using Gemini"""
        try:
            prompt = f"""
            Generate German vocabulary for the topic: "{topic}"
            
            Requirements:
            - Generate {num_words} German words with English translations
            - Generate {num_phrases} German phrases with English translations
            - Format as JSON with this structure:
            {{
                "words": [
                    {{"german": "German word", "english": "English translation"}},
                    ...
                ],
                "phrases": [
                    {{"german": "German phrase", "english": "English translation"}},
                    ...
                ]
            }}
            
            Context from existing deck: {existing_content}
            
            Make sure the content is relevant to the topic and appropriate for language learning.
            Avoid duplicating words/phrases that might already be in the deck.
            """

            response = self.gemini_client.generate_content(prompt)

            # Parse JSON response
            content = response.text.strip()
            # Remove markdown code blocks if present
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]

            return json.loads(content)

        except Exception as e:
            print(f"ERROR: Failed to generate German content: {e}")
            return None

    def create_anki_cards(self, content_data):
        """Create new Anki cards from generated content"""
        if not content_data:
            return False

        success_count = 0
        error_count = 0

        # Check if deck exists, create if it doesn't
        decks = self.call_ankiconnect("deckNames", {})
        if not decks or not decks.get("result"):
            print("❌ Could not get available decks")
            return False

        if self.config["deck_name"] not in decks["result"]:
            print(f"📁 Deck '{self.config['deck_name']}' not found, creating it...")
            create_result = self.call_ankiconnect(
                "createDeck", {"deck": self.config["deck_name"]}
            )
            if not create_result or create_result.get("error"):
                print(
                    f"❌ Failed to create deck: {create_result.get('error', 'Unknown error')}"
                )
                return False
            print(f"✅ Created deck '{self.config['deck_name']}'")

        # Get model name for the deck
        models = self.call_ankiconnect("modelNames", {})
        if not models or not models.get("result"):
            print("❌ Could not get available models")
            return False

        # Use the first available model (usually Basic)
        model_name = models["result"][0]

        # Create cards for words
        for word_data in content_data.get("words", []):
            try:
                note = {
                    "deckName": self.config["deck_name"],
                    "modelName": model_name,
                    "fields": {
                        self.config["text_field"]: word_data["german"],
                        "Back": word_data["english"],
                    },
                    "tags": ["generated", "german"],
                }

                response = self.call_ankiconnect("addNote", {"note": note})
                if response and not response.get("error"):
                    success_count += 1
                else:
                    error_count += 1

            except Exception as e:
                print(f"ERROR creating word card: {e}")
                error_count += 1

        # Create cards for phrases
        for phrase_data in content_data.get("phrases", []):
            try:
                note = {
                    "deckName": self.config["deck_name"],
                    "modelName": model_name,
                    "fields": {
                        self.config["text_field"]: phrase_data["german"],
                        "Back": phrase_data["english"],
                    },
                    "tags": ["generated", "german", "phrase"],
                }

                response = self.call_ankiconnect("addNote", {"note": note})
                if response and not response.get("error"):
                    success_count += 1
                else:
                    error_count += 1

            except Exception as e:
                print(f"ERROR creating phrase card: {e}")
                error_count += 1

        print(f"✅ Created {success_count} new cards")
        if error_count > 0:
            print(f"⚠️  {error_count} cards failed to create")

        return success_count > 0

    def generate_and_add_content(self):
        """Generate German content using Gemini and add to deck"""
        print(f"\n🤖 Step 3: Generate German Content")
        print("=" * 50)

        # Get topic
        topic = input(
            "Enter topic for German vocabulary (e.g., 'food', 'travel', 'business'): "
        ).strip()
        if not topic:
            print("❌ Topic is required")
            return False

        # Get number of words and phrases
        try:
            num_words = int(
                input("Number of German words to generate [10]: ").strip() or "10"
            )
            num_phrases = int(
                input("Number of German phrases to generate [5]: ").strip() or "5"
            )
        except ValueError:
            print("❌ Please enter valid numbers")
            return False

        # Analyze existing deck content
        print("\n📊 Analyzing existing deck content...")
        existing_content = self.analyze_deck_content()
        print(f"✅ Deck analysis complete")

        # Generate content with Gemini
        print(
            f"\n🧠 Generating {num_words} words and {num_phrases} phrases about '{topic}'..."
        )
        content_data = self.generate_german_content(
            topic, num_words, num_phrases, existing_content
        )

        if not content_data:
            print("❌ Failed to generate content")
            return False

        # Show preview
        print(f"\n📝 Generated content preview:")
        print("Words:")
        for word in content_data.get("words", [])[:3]:
            print(f"  {word['german']} = {word['english']}")
        if len(content_data.get("words", [])) > 3:
            print(f"  ... and {len(content_data['words']) - 3} more words")

        print("\nPhrases:")
        for phrase in content_data.get("phrases", [])[:2]:
            print(f"  {phrase['german']} = {phrase['english']}")
        if len(content_data.get("phrases", [])) > 2:
            print(f"  ... and {len(content_data['phrases']) - 2} more phrases")

        # Confirm creation
        confirm = (
            input(
                f"\nCreate {len(content_data.get('words', [])) + len(content_data.get('phrases', []))} new cards? (y/n): "
            )
            .strip()
            .lower()
        )
        if confirm != "y":
            print("❌ Card creation cancelled")
            return False

        # Create cards
        print("\n📚 Creating Anki cards...")
        success = self.create_anki_cards(content_data)

        if success:
            print("✅ Content generation and card creation complete!")

            # Ask if user wants to add audio
            add_audio = (
                input("\nWould you like to add audio to the new cards? (y/n): ")
                .strip()
                .lower()
            )
            if add_audio == "y":
                return self.process_deck()

        return success

    def process_deck(self):
        """Process all cards in the deck"""
        print(f"\n🎵 Step 3: Processing Deck '{self.config['deck_name']}'")
        print("=" * 50)

        # Get notes from deck
        result = self.call_ankiconnect(
            "findNotes", {"query": f'deck:"{self.config["deck_name"]}"'}
        )
        if not result:
            print("❌ Failed to get notes from deck")
            return False

        note_ids = result.get("result", [])
        if not note_ids:
            print(f"❌ No notes found in deck '{self.config['deck_name']}'")
            return False

        # Get note information
        result = self.call_ankiconnect("notesInfo", {"notes": note_ids})
        if not result:
            print("❌ Failed to get note information")
            return False

        notes = result.get("result", [])
        print(f"✅ Found {len(notes)} cards in deck")

        # Process notes
        success_count = 0
        error_count = 0
        skip_count = 0

        for note in tqdm(notes, desc="Processing cards"):
            try:
                # Extract text
                raw_field_value = note["fields"][self.config["text_field"]]["value"]
                word = self.extract_text_from_field(raw_field_value)

                if not word or not word.strip():
                    skip_count += 1
                    continue

                # Check if audio already exists
                audio_field_value = note["fields"][self.config["audio_field"]]["value"]
                if "[sound:" in audio_field_value:
                    skip_count += 1
                    continue

                # Generate and add audio
                filename = f"{note['noteId']}.mp3"
                audio = self.generate_audio_bytes(word)

                if audio:
                    if self.update_note_with_audio(note, audio, filename):
                        success_count += 1
                    else:
                        error_count += 1
                else:
                    error_count += 1

                time.sleep(0.5)  # Rate limiting

            except KeyboardInterrupt:
                print("\n⚠️ Process interrupted by user.")
                break
            except Exception as e:
                print(f"ERROR: Unexpected error processing note: {e}")
                error_count += 1

        # Print results
        print(f"\n🎉 Processing Complete!")
        print("=" * 30)
        print(f"✅ Successfully processed: {success_count} cards")
        print(f"⚠️  Skipped: {skip_count} cards")
        print(f"❌ Errors: {error_count} cards")

        return True

    def show_menu(self):
        """Show main menu options"""
        print("\n🎯 What would you like to do?")
        print("=" * 40)
        print("1. Generate German content with Gemini")
        print("2. Add audio to existing cards")
        print("3. Both (generate content + add audio)")
        print("4. Exit")
        print()

    def run(self):
        """Main CLI flow"""
        self.print_banner()

        # Step 1: Check Anki
        if not self.check_anki_running():
            print("\n❌ Please fix the Anki setup and try again.")
            return False

        # Step 2: Get configuration
        if not self.collect_configuration():
            return False

        # Step 3: Initialize clients
        if not self.initialize_gemini():
            return False

        if not self.initialize_elevenlabs():
            return False

        # Step 4: Show menu and process
        while True:
            self.show_menu()
            choice = input("Enter your choice (1-4): ").strip()

            if choice == "1":
                # Generate content only
                success = self.generate_and_add_content()
                if not success:
                    print("❌ Content generation failed")
                else:
                    print("✅ Content generation completed!")

            elif choice == "2":
                # Add audio only
                success = self.process_deck()
                if not success:
                    print("❌ Audio processing failed")
                else:
                    print("✅ Audio processing completed!")

            elif choice == "3":
                # Both
                success1 = self.generate_and_add_content()
                if success1:
                    print("\n" + "=" * 50)
                    print("Now adding audio to all cards...")
                    success2 = self.process_deck()
                    if success2:
                        print(
                            "✅ Both content generation and audio processing completed!"
                        )
                    else:
                        print("⚠️ Content generated but audio processing failed")
                else:
                    print("❌ Content generation failed")

            elif choice == "4":
                print("👋 Goodbye!")
                return True

            else:
                print("❌ Invalid choice. Please enter 1-4.")
                continue

            # Ask if user wants to continue
            if choice in ["1", "2", "3"]:
                continue_choice = (
                    input("\nWould you like to do something else? (y/n): ")
                    .strip()
                    .lower()
                )
                if continue_choice != "y":
                    print("👋 Goodbye!")
                    return True

        return True


def main():
    """Entry point"""
    try:
        app = AnkiAudioGenerator()
        success = app.run()

        if success:
            print("\n🎉 All done! Your Anki cards now have audio!")
        else:
            print("\n❌ Process completed with errors.")

    except KeyboardInterrupt:
        print("\n\n⚠️ Program interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
