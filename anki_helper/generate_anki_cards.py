#!/usr/bin/env python3
"""
Anki Card Generator from Word Frequency Analysis
Generates new Anki flashcards using frequent words and creates practice phrases
"""

import re
import json
import argparse
import os
from collections import Counter
from datetime import datetime


def load_word_frequency(json_file):
    """Load word frequency data from JSON file"""
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_custom_word_list(txt_file):
    """Load custom word list from text file (one word per line)"""
    words = []
    with open(txt_file, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word and not word.startswith("#"):
                words.append(word.lower())
    return words


def generate_practice_phrases(word, complexity="simple"):
    """Generate practice phrases/sentences for a given word"""
    # Common German sentence patterns
    phrases = {
        "simple": [
            f"Das ist {word}.",
            f"Ich habe {word}.",
            f"Wo ist {word}?",
            f"Das {word} ist hier.",
        ],
        "questions": [
            f"Was ist {word}?",
            f"Wie sagt man {word} auf Englisch?",
            f"Wo kann ich {word} finden?",
            f"Wann brauche ich {word}?",
        ],
        "contexts": [
            f"Ich suche {word}.",
            f"Kannst du mir {word} geben?",
            f"Das {word} gefällt mir.",
            f"Ich möchte {word} lernen.",
        ],
    }

    if complexity in phrases:
        return phrases[complexity]
    return phrases["simple"]


def create_anki_card(word, translation="", audio_file="", card_type="simple"):
    """Create a single Anki card in the proper format"""
    # Generate audio filename if not provided
    if not audio_file:
        timestamp = int(datetime.now().timestamp() * 1000)
        audio_file = f"{word}_{timestamp}.mp3"

    # Basic card format
    if card_type == "word":
        front = f"{word} [sound:{audio_file}]"
        back = translation if translation else f"Translation for: {word}"

    elif card_type == "phrase":
        # For phrases, create a more detailed card
        front = f"<strong>{word}</strong> [sound:{audio_file}]"
        back = (
            f"<div>{translation}</div>"
            if translation
            else f"Practice phrase with: {word}"
        )

    elif card_type == "question":
        # Question format
        front = f"<strong>Was bedeutet '{word}'?</strong> [sound:{audio_file}]"
        back = translation if translation else f"Meaning of: {word}"

    else:
        # Default simple format
        front = f"{word} [sound:{audio_file}]"
        back = translation if translation else ""

    return f"{front}\t{back}"


def generate_anki_deck_from_frequency(
    word_freq_json,
    output_file,
    top_n=50,
    card_type="simple",
    include_phrases=False,
):
    """Generate Anki deck from word frequency JSON"""
    # Load frequency data
    word_freq = load_word_frequency(word_freq_json)

    # Get top N words
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]

    cards = []

    # Add Anki header
    cards.append("#separator:tab")
    cards.append("#html:true")

    for word, frequency in sorted_words:
        # Create basic word card
        timestamp = int(datetime.now().timestamp() * 1000)
        audio_file = f"{word}_{timestamp}.mp3"

        card = create_anki_card(word, "", audio_file, card_type)
        cards.append(card)

        # Optionally add practice phrases
        if include_phrases:
            phrases = generate_practice_phrases(word, "simple")
            for i, phrase in enumerate(phrases[:2]):  # Limit to 2 phrases per word
                phrase_timestamp = timestamp + i + 1
                phrase_audio = f"phrase_{word}_{phrase_timestamp}.mp3"
                phrase_card = create_anki_card(phrase, "", phrase_audio, "phrase")
                cards.append(phrase_card)

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(cards))

    print(f"Generated {len(cards) - 2} cards from {top_n} most frequent words")
    print(f"Anki deck saved to: {output_file}")

    return cards


def generate_anki_deck_from_list(
    word_list_file, output_file, card_type="simple", include_phrases=False
):
    """Generate Anki deck from custom word list"""
    # Load word list
    words = load_custom_word_list(word_list_file)

    cards = []

    # Add Anki header
    cards.append("#separator:tab")
    cards.append("#html:true")

    for word in words:
        # Create basic word card
        timestamp = int(datetime.now().timestamp() * 1000)
        audio_file = f"{word}_{timestamp}.mp3"

        card = create_anki_card(word, "", audio_file, card_type)
        cards.append(card)

        # Optionally add practice phrases
        if include_phrases:
            phrases = generate_practice_phrases(word, "simple")
            for i, phrase in enumerate(phrases[:2]):
                phrase_timestamp = timestamp + i + 1
                phrase_audio = f"phrase_{word}_{phrase_timestamp}.mp3"
                phrase_card = create_anki_card(phrase, "", phrase_audio, "phrase")
                cards.append(phrase_card)

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(cards))

    print(f"Generated {len(cards) - 2} cards from {len(words)} words")
    print(f"Anki deck saved to: {output_file}")

    return cards


def generate_anki_deck_from_multiple_lists(
    word_list_files, output_file, card_type="simple", include_phrases=False
):
    """Generate Anki deck from multiple word list files"""
    all_words = []

    for word_file in word_list_files:
        print(f"Loading words from: {word_file}")
        words = load_custom_word_list(word_file)
        all_words.extend(words)

    # Remove duplicates while preserving order
    seen = set()
    unique_words = []
    for word in all_words:
        if word not in seen:
            seen.add(word)
            unique_words.append(word)

    print(f"Total unique words: {len(unique_words)}")

    cards = []

    # Add Anki header
    cards.append("#separator:tab")
    cards.append("#html:true")

    for word in unique_words:
        # Create basic word card
        timestamp = int(datetime.now().timestamp() * 1000)
        audio_file = f"{word}_{timestamp}.mp3"

        card = create_anki_card(word, "", audio_file, card_type)
        cards.append(card)

        # Optionally add practice phrases
        if include_phrases:
            phrases = generate_practice_phrases(word, "simple")
            for i, phrase in enumerate(phrases[:2]):
                phrase_timestamp = timestamp + i + 1
                phrase_audio = f"phrase_{word}_{phrase_timestamp}.mp3"
                phrase_card = create_anki_card(phrase, "", phrase_audio, "phrase")
                cards.append(phrase_card)

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(cards))

    print(f"Generated {len(cards) - 2} cards from {len(unique_words)} unique words")
    print(f"Anki deck saved to: {output_file}")

    return cards


def create_example_word_list(filename):
    """Create an example word list file"""
    example_words = [
        "# German Word List",
        "# One word per line",
        "# Lines starting with # are comments",
        "",
        "Haus",
        "Katze",
        "Hund",
        "Wasser",
        "Brot",
        "Schule",
        "Arbeit",
        "Familie",
        "Freund",
        "Stadt",
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(example_words))

    print(f"Example word list created: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Anki flashcards from word lists or frequency analysis"
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--frequency-json",
        help="Path to word frequency JSON file (generated by word analyzer)",
    )
    input_group.add_argument(
        "--word-list", help="Path to text file with word list (one word per line)"
    )
    input_group.add_argument(
        "--word-lists",
        nargs="+",
        help="Multiple text files with word lists (one word per line each)",
    )
    input_group.add_argument(
        "--create-example", action="store_true", help="Create an example word list file"
    )

    # Output options
    parser.add_argument(
        "--output", default="generated_anki_deck.txt", help="Output Anki deck file"
    )

    # Card generation options
    parser.add_argument(
        "--top-n",
        type=int,
        default=50,
        help="Number of top frequent words to use (only with --frequency-json)",
    )
    parser.add_argument(
        "--card-type",
        choices=["simple", "word", "phrase", "question"],
        default="simple",
        help="Type of flashcard to generate",
    )
    parser.add_argument(
        "--include-phrases",
        action="store_true",
        help="Include practice phrases for each word",
    )

    args = parser.parse_args()

    # Create example word list
    if args.create_example:
        create_example_word_list("example_word_list.txt")
        return

    # Generate from frequency JSON
    if args.frequency_json:
        if not os.path.exists(args.frequency_json):
            print(f"Error: File '{args.frequency_json}' not found!")
            return

        generate_anki_deck_from_frequency(
            args.frequency_json,
            args.output,
            args.top_n,
            args.card_type,
            args.include_phrases,
        )

    # Generate from single word list
    elif args.word_list:
        if not os.path.exists(args.word_list):
            print(f"Error: File '{args.word_list}' not found!")
            return

        generate_anki_deck_from_list(
            args.word_list, args.output, args.card_type, args.include_phrases
        )

    # Generate from multiple word lists
    elif args.word_lists:
        missing_files = [f for f in args.word_lists if not os.path.exists(f)]
        if missing_files:
            print(f"Error: The following files were not found:")
            for f in missing_files:
                print(f"  - {f}")
            return

        generate_anki_deck_from_multiple_lists(
            args.word_lists, args.output, args.card_type, args.include_phrases
        )

    print("\nNext steps:")
    print("1. Import the generated file into Anki")
    print("2. Add audio files using your TTS system")
    print("3. Add translations for each card")


if __name__ == "__main__":
    main()
