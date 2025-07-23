#!/usr/bin/env python3
"""
Anki Audio Generator CLI
A command-line tool to automatically generate and add audio to Anki cards using ElevenLabs TTS.
"""

import requests
import base64
import time
import re
from tqdm import tqdm
from elevenlabs.client import ElevenLabs

class AnkiAudioGenerator:
    def __init__(self):
        self.elevenlabs_client = None
        self.config = {}
    
    def print_banner(self):
        """Print welcome banner"""
        print("=" * 60)
        print("           🎵 ANKI AUDIO GENERATOR 🎵")
        print("    Automatically add TTS audio to your Anki cards")
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
            response = requests.post("http://localhost:8765", json={
                "action": "version",
                "version": 6
            }, timeout=5)
            result = response.json()
            
            if result.get("error"):
                print(f"❌ AnkiConnect error: {result['error']}")
                return False
            
            print(f"✅ Anki is running (AnkiConnect version {result.get('result', 'unknown')})")
            return True
            
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to Anki. Please make sure:")
            print("   1. Anki is running")
            print("   2. AnkiConnect addon is installed")
            print("   3. AnkiConnect addon URL: https://ankiweb.net/shared/info/2055492159")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def get_anki_decks(self):
        """Get list of available Anki decks"""
        try:
            response = requests.post("http://localhost:8765", json={
                "action": "deckNames",
                "version": 6
            })
            result = response.json()
            return result.get("result", [])
        except:
            return []
    
    def get_deck_fields(self, deck_name):
        """Get available fields for a deck"""
        try:
            # Get a sample note from the deck
            response = requests.post("http://localhost:8765", json={
                "action": "findNotes",
                "version": 6,
                "params": {"query": f'deck:"{deck_name}"'}
            })
            note_ids = response.json().get("result", [])
            
            if not note_ids:
                return []
            
            # Get note info for the first note
            response = requests.post("http://localhost:8765", json={
                "action": "notesInfo",
                "version": 6,
                "params": {"notes": [note_ids[0]]}
            })
            notes = response.json().get("result", [])
            
            if notes:
                return list(notes[0]["fields"].keys())
            return []
        except:
            return []
    
    def collect_configuration(self):
        """Collect all configuration from user"""
        print("\n🛠️  Step 2: Configuration")
        print("=" * 40)
        
        # Get deck name
        decks = self.get_anki_decks()
        if decks:
            print("Available decks:")
            for i, deck in enumerate(decks, 1):
                print(f"  {i}. {deck}")
            print()
            
            while True:
                deck_input = input("Enter deck name (or number from list above): ").strip()
                
                # Check if it's a number
                if deck_input.isdigit():
                    idx = int(deck_input) - 1
                    if 0 <= idx < len(decks):
                        self.config['deck_name'] = decks[idx]
                        break
                    else:
                        print("❌ Invalid number. Please try again.")
                        continue
                
                # Check if it's a deck name
                if deck_input in decks:
                    self.config['deck_name'] = deck_input
                    break
                else:
                    print("❌ Deck not found. Please try again.")
        else:
            self.config['deck_name'] = input("Enter Anki deck name: ").strip()
        
        print(f"✅ Selected deck: {self.config['deck_name']}")
        
        # Get available fields for the selected deck
        fields = self.get_deck_fields(self.config['deck_name'])
        if fields:
            print(f"\nAvailable fields in '{self.config['deck_name']}':")
            for i, field in enumerate(fields, 1):
                print(f"  {i}. {field}")
            print()
            
            # Get text field
            while True:
                text_field_input = input("Enter field name containing text to read (or number): ").strip()
                
                if text_field_input.isdigit():
                    idx = int(text_field_input) - 1
                    if 0 <= idx < len(fields):
                        self.config['text_field'] = fields[idx]
                        break
                    else:
                        print("❌ Invalid number. Please try again.")
                        continue
                
                if text_field_input in fields:
                    self.config['text_field'] = text_field_input
                    break
                else:
                    print("❌ Field not found. Please try again.")
            
            # Get audio field
            while True:
                audio_field_input = input("Enter field name where audio should be added (or number): ").strip()
                
                if audio_field_input.isdigit():
                    idx = int(audio_field_input) - 1
                    if 0 <= idx < len(fields):
                        self.config['audio_field'] = fields[idx]
                        break
                    else:
                        print("❌ Invalid number. Please try again.")
                        continue
                
                if audio_field_input in fields:
                    self.config['audio_field'] = audio_field_input
                    break
                else:
                    print("❌ Field not found. Please try again.")
        else:
            self.config['text_field'] = input("Enter field name containing text to read: ").strip()
            self.config['audio_field'] = input("Enter field name where audio should be added: ").strip()
        
        # Get ElevenLabs configuration
        print("\n🎤 ElevenLabs Configuration")
        print("=" * 30)
        
        self.config['api_key'] = input("Enter your ElevenLabs API key: ").strip()
        self.config['voice_id'] = input("Enter ElevenLabs voice ID (The voice you want to use to read the text): ").strip()
        
        # Language code with default
        language_code = input("Enter language code (Language code (ISO 639-1)  e.g., 'ar' for Arabic, 'en' for English) [en]: ").strip()
        self.config['language_code'] = language_code if language_code else "en"
        
        # Show configuration summary
        print("\n📋 Configuration Summary")
        print("=" * 30)
        print(f"Deck: {self.config['deck_name']}")
        print(f"Text field: {self.config['text_field']}")
        print(f"Audio field: {self.config['audio_field']}")
        print(f"Voice ID: {self.config['voice_id']}")
        print(f"Language: {self.config['language_code']}")
        print()
        
        confirm = input("Is this configuration correct? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Configuration cancelled. Please restart the program.")
            return False
        
        return True
    
    def initialize_elevenlabs(self):
        """Initialize ElevenLabs client"""
        try:
            self.elevenlabs_client = ElevenLabs(api_key=self.config['api_key'])
            print("✅ ElevenLabs client initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize ElevenLabs client: {e}")
            return False
    
    def call_ankiconnect(self, action, params):
        """Call AnkiConnect with error handling"""
        try:
            response = requests.post("http://localhost:8765", json={
                "action": action,
                "version": 6,
                "params": params
            }, timeout=10)
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
        clean_text = re.sub(r'\[sound:[^\]]+\]', '', field_value).strip()
        return clean_text
    
    def generate_audio_bytes(self, text):
        """Generate audio from text using ElevenLabs"""
        if not text or not text.strip():
            return None
        
        try:
            audio_generator = self.elevenlabs_client.text_to_speech.convert(
                text=text,
                voice_id=self.config['voice_id'],
                model_id="eleven_turbo_v2_5",
                output_format="mp3_44100_128",
                language_code=self.config['language_code'],
                voice_settings={
                    "stability": 0.8,
                    "similarity_boost": 0.75,
                }
            )
            
            # Convert generator to bytes
            audio_bytes = b''.join(audio_generator)
            return audio_bytes
            
        except Exception as e:
            print(f"ERROR: Failed to generate audio for '{text}': {e}")
            return None
    
    def update_note_with_audio(self, note, audio_bytes, filename):
        """Update Anki note with audio file"""
        try:
            # Store the audio file
            encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")
            
            store_response = self.call_ankiconnect("storeMediaFile", {
                "filename": filename,
                "data": encoded_audio
            })
            
            if store_response is None or store_response.get("error"):
                return False
            
            # Get current field content
            current_content = note["fields"][self.config['audio_field']]["value"]
            
            # Create new content
            if self.config['audio_field'] == self.config['text_field']:
                # Same field: append audio to text
                clean_text = self.extract_text_from_field(current_content)
                new_content = f"{clean_text} [sound:{filename}]"
            else:
                # Different field: just add audio
                new_content = f"[sound:{filename}]"
            
            # Update the field
            response = self.call_ankiconnect("updateNoteFields", {
                "note": {
                    "id": note["noteId"],
                    "fields": {
                        self.config['audio_field']: new_content
                    }
                }
            })
            
            return response is not None and not response.get("error")
            
        except Exception as e:
            print(f"ERROR: Exception while updating note {note['noteId']}: {e}")
            return False
    
    def process_deck(self):
        """Process all cards in the deck"""
        print(f"\n🎵 Step 3: Processing Deck '{self.config['deck_name']}'")
        print("=" * 50)
        
        # Get notes from deck
        result = self.call_ankiconnect("findNotes", {"query": f'deck:"{self.config["deck_name"]}"'})
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
                raw_field_value = note["fields"][self.config['text_field']]["value"]
                word = self.extract_text_from_field(raw_field_value)
                
                if not word or not word.strip():
                    skip_count += 1
                    continue
                
                # Check if audio already exists
                audio_field_value = note["fields"][self.config['audio_field']]["value"]
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
        
        # Step 3: Initialize ElevenLabs
        if not self.initialize_elevenlabs():
            return False
        
        # Step 4: Process deck
        return self.process_deck()

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
