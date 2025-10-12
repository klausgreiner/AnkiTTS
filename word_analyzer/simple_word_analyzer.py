#!/usr/bin/env python3
"""
Simple German Word Frequency Analyzer
Analyzes German words from Anki deck format using only built-in Python libraries
"""

import re
import json
from collections import Counter
import argparse
import os


def clean_german_text(text):
    """Clean German text by removing HTML tags, sound references, and extra formatting"""
    # Remove sound references like [sound:filename.mp3]
    text = re.sub(r"\[sound:[^\]]+\]", "", text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Remove extra whitespace and normalize
    text = re.sub(r"\s+", " ", text).strip()

    # Remove special characters but keep German umlauts and ß
    text = re.sub(r"[^\w\säöüßÄÖÜ]", " ", text)

    return text


def extract_german_words(file_path):
    """Extract German words from Anki deck format file"""
    words = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line_num, line in enumerate(file, 1):
            # Skip header lines
            if line.startswith("#") or not line.strip():
                continue

            # Split by tab to get German and English parts
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                german_part = parts[0]

                # Clean the German text
                cleaned_text = clean_german_text(german_part)

                # Split into individual words
                line_words = cleaned_text.lower().split()

                # Filter out very short words and common German articles/prepositions
                stop_words = {
                    "der",
                    "die",
                    "das",
                    "ein",
                    "eine",
                    "einen",
                    "einem",
                    "einer",
                    "und",
                    "oder",
                    "aber",
                    "mit",
                    "von",
                    "zu",
                    "in",
                    "auf",
                    "für",
                    "an",
                    "ist",
                    "sind",
                    "war",
                    "waren",
                    "haben",
                    "hat",
                    "hatte",
                    "hatten",
                    "werden",
                    "wird",
                    "wurde",
                    "wurden",
                    "können",
                    "kann",
                    "konnte",
                    "konnten",
                    "müssen",
                    "muss",
                    "musste",
                    "mussten",
                    "wollen",
                    "will",
                    "wollte",
                    "wollten",
                    "sollen",
                    "soll",
                    "sollte",
                    "sollten",
                    "dürfen",
                    "darf",
                    "durfte",
                    "durften",
                    "mögen",
                    "mag",
                    "mochte",
                    "mochten",
                    "ich",
                    "du",
                    "er",
                    "sie",
                    "es",
                    "wir",
                    "ihr",
                    "sie",
                    "mir",
                    "mich",
                    "dir",
                    "dich",
                    "ihm",
                    "ihn",
                    "ihr",
                    "uns",
                    "euch",
                    "ihnen",
                    "mein",
                    "meine",
                    "meinen",
                    "meinem",
                    "meiner",
                    "dein",
                    "deine",
                    "deinen",
                    "deinem",
                    "deiner",
                    "sein",
                    "seine",
                    "seinen",
                    "seinem",
                    "seiner",
                    "ihr",
                    "ihre",
                    "ihren",
                    "ihrem",
                    "ihrer",
                    "unser",
                    "unsere",
                    "unseren",
                    "unserem",
                    "unserer",
                    "euer",
                    "eure",
                    "euren",
                    "eurem",
                    "eurer",
                    "ihr",
                    "ihre",
                    "ihren",
                    "ihrem",
                    "ihrer",
                    "das",
                    "die",
                    "der",
                    "den",
                    "dem",
                    "des",
                    "ein",
                    "eine",
                    "einen",
                    "einem",
                    "einer",
                    "eines",
                    "kein",
                    "keine",
                    "keinen",
                    "keinem",
                    "keiner",
                    "keines",
                    "alle",
                    "allem",
                    "allen",
                    "aller",
                    "alles",
                    "manche",
                    "manchem",
                    "manchen",
                    "mancher",
                    "manches",
                    "viele",
                    "vieler",
                    "vielen",
                    "vieles",
                    "wenige",
                    "weniger",
                    "wenigen",
                    "weniges",
                    "andere",
                    "anderem",
                    "anderen",
                    "anderer",
                    "anderes",
                    "jede",
                    "jedem",
                    "jeden",
                    "jeder",
                    "jedes",
                    "jene",
                    "jenem",
                    "jenen",
                    "jener",
                    "jenes",
                    "diese",
                    "diesem",
                    "diesen",
                    "dieser",
                    "dieses",
                    "solche",
                    "solchem",
                    "solchen",
                    "solcher",
                    "solches",
                    "welche",
                    "welchem",
                    "welchen",
                    "welcher",
                    "welches",
                    "auch",
                    "nur",
                    "noch",
                    "schon",
                    "erst",
                    "dann",
                    "danach",
                    "deshalb",
                    "deswegen",
                    "trotzdem",
                    "jedoch",
                    "obwohl",
                    "falls",
                    "während",
                    "sobald",
                    "überall",
                    "nirgends",
                    "irgendwann",
                    "manchmal",
                    "oft",
                    "selten",
                    "immer",
                    "nie",
                    "vielleicht",
                    "wahrscheinlich",
                    "möglich",
                    "unmöglich",
                    "eigentlich",
                    "wirklich",
                    "sogar",
                    "nur",
                    "auch",
                    "noch",
                    "schon",
                    "erst",
                    "dann",
                    "danach",
                    "deshalb",
                    "deswegen",
                    "trotzdem",
                    "jedoch",
                    "obwohl",
                    "falls",
                    "während",
                    "sobald",
                    "überall",
                    "nirgends",
                    "irgendwann",
                    "manchmal",
                    "oft",
                    "selten",
                    "immer",
                    "nie",
                    "vielleicht",
                    "wahrscheinlich",
                    "möglich",
                    "unmöglich",
                    "eigentlich",
                    "wirklich",
                    "sogar",
                }

                # Add words that are not stop words and have at least 2 characters
                for word in line_words:
                    if len(word) >= 2 and word not in stop_words:
                        words.append(word)

    return words


def create_frequency_analysis(words):
    """Create frequency analysis and return Counter object"""
    word_freq = Counter(words)
    return word_freq


def save_frequency_data(word_freq, output_dir="."):
    """Save frequency data to CSV and text files"""
    # Save to text file
    txt_path = os.path.join(output_dir, "german_word_frequency.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("German Word Frequency Analysis\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Total unique words: {len(word_freq)}\n")
        f.write(f"Total word occurrences: {sum(word_freq.values())}\n\n")
        f.write("Word Frequency (Most to Least Used):\n")
        f.write("-" * 40 + "\n")

        for i, (word, count) in enumerate(word_freq.most_common(), 1):
            f.write(f"{i:4d}. {word:20s} : {count:4d}\n")

    print(f"Detailed frequency list saved to: {txt_path}")

    # Save to JSON for easy processing
    json_path = os.path.join(output_dir, "german_word_frequency.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dict(word_freq.most_common()), f, ensure_ascii=False, indent=2)

    print(f"JSON data saved to: {json_path}")

    return word_freq


def print_summary(word_freq):
    """Print summary statistics"""
    total_words = sum(word_freq.values())
    unique_words = len(word_freq)

    print("\n" + "=" * 60)
    print("GERMAN WORD FREQUENCY ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Total word occurrences: {total_words:,}")
    print(f"Unique words: {unique_words:,}")
    print(f"Average frequency: {total_words/unique_words:.2f}")
    print(
        f"Most frequent word: '{word_freq.most_common(1)[0][0]}' ({word_freq.most_common(1)[0][1]} times)"
    )

    # Words that appear only once
    hapax_legomena = sum(1 for count in word_freq.values() if count == 1)
    print(
        f"Words appearing only once: {hapax_legomena:,} ({hapax_legomena/unique_words*100:.1f}%)"
    )

    print("\nTop 30 Most Frequent Words:")
    print("-" * 40)
    for i, (word, count) in enumerate(word_freq.most_common(30), 1):
        print(f"{i:2d}. {word:15s} : {count:4d}")


def create_simple_visualization(word_freq, top_n=30, output_dir="."):
    """Create a simple text-based visualization"""
    top_words = word_freq.most_common(top_n)

    # Create a simple bar chart using text
    max_freq = top_words[0][1]
    bar_length = 50

    viz_path = os.path.join(output_dir, "german_word_frequency_viz.txt")
    with open(viz_path, "w", encoding="utf-8") as f:
        f.write("German Word Frequency Visualization\n")
        f.write("=" * 60 + "\n\n")
        f.write("Text-based bar chart (bar length represents frequency):\n\n")

        for word, count in top_words:
            bar_size = int((count / max_freq) * bar_length)
            bar = "█" * bar_size + "░" * (bar_length - bar_size)
            f.write(f"{word:15s} |{bar}| {count:4d}\n")

    print(f"Text visualization saved to: {viz_path}")

    # Also print to console
    print("\n" + "=" * 60)
    print("TEXT-BASED FREQUENCY VISUALIZATION")
    print("=" * 60)
    print("Word            |Frequency Bar (█ = frequency)| Count")
    print("-" * 60)

    for word, count in top_words:
        bar_size = int((count / max_freq) * bar_length)
        bar = "█" * bar_size + "░" * (bar_length - bar_size)
        print(f"{word:15s} |{bar}| {count:4d}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze German word frequency from Anki deck"
    )
    parser.add_argument("input_file", help="Path to the German text file")
    parser.add_argument(
        "--top-n",
        type=int,
        default=30,
        help="Number of top words to show in visualizations",
    )
    parser.add_argument(
        "--output-dir", default=".", help="Output directory for results"
    )

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' not found!")
        return

    print(f"Analyzing German words from: {args.input_file}")
    print("Extracting words...")

    # Extract words
    words = extract_german_words(args.input_file)
    print(f"Extracted {len(words)} word occurrences")

    # Create frequency analysis
    print("Creating frequency analysis...")
    word_freq = create_frequency_analysis(words)

    # Print summary
    print_summary(word_freq)

    # Save data
    print("\nSaving frequency data...")
    save_frequency_data(word_freq, args.output_dir)

    # Create simple visualization
    print("Creating text-based visualization...")
    create_simple_visualization(word_freq, args.top_n, args.output_dir)

    print(f"\nAnalysis complete! Check the output directory: {args.output_dir}")


if __name__ == "__main__":
    main()
