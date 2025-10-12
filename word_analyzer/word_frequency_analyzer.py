#!/usr/bin/env python3
"""
German Word Frequency Analyzer
Analyzes German words from Anki deck format and creates frequency visualization
"""

import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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


def create_frequency_analysis(words, top_n=50):
    """Create frequency analysis and return Counter object"""
    word_freq = Counter(words)
    return word_freq


def create_visualizations(word_freq, top_n=50, output_dir="."):
    """Create various visualizations of word frequency"""
    # Get top N most frequent words
    top_words = word_freq.most_common(top_n)
    words, counts = zip(*top_words)

    # Set up the plotting style
    plt.style.use("seaborn-v0_8")
    sns.set_palette("husl")

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle("German Word Frequency Analysis", fontsize=20, fontweight="bold")

    # 1. Horizontal bar chart
    ax1 = axes[0, 0]
    bars = ax1.barh(range(len(words)), counts)
    ax1.set_yticks(range(len(words)))
    ax1.set_yticklabels(words, fontsize=10)
    ax1.set_xlabel("Frequency", fontsize=12)
    ax1.set_title(
        f"Top {top_n} Most Frequent German Words", fontsize=14, fontweight="bold"
    )
    ax1.grid(axis="x", alpha=0.3)

    # Add value labels on bars
    for i, (bar, count) in enumerate(zip(bars, counts)):
        ax1.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            str(count),
            ha="left",
            va="center",
            fontsize=9,
        )

    # 2. Vertical bar chart
    ax2 = axes[0, 1]
    bars2 = ax2.bar(range(len(words)), counts)
    ax2.set_xticks(range(len(words)))
    ax2.set_xticklabels(words, rotation=45, ha="right", fontsize=8)
    ax2.set_ylabel("Frequency", fontsize=12)
    ax2.set_title(
        f"Top {top_n} Most Frequent German Words (Vertical)",
        fontsize=14,
        fontweight="bold",
    )
    ax2.grid(axis="y", alpha=0.3)

    # 3. Pie chart for top 20
    ax3 = axes[1, 0]
    top_20 = word_freq.most_common(20)
    words_20, counts_20 = zip(*top_20)
    wedges, texts, autotexts = ax3.pie(
        counts_20,
        labels=words_20,
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 8},
    )
    ax3.set_title(
        "Top 20 Most Frequent German Words (Pie Chart)", fontsize=14, fontweight="bold"
    )

    # 4. Word cloud style visualization (scatter plot with word sizes)
    ax4 = axes[1, 1]
    # Create a scatter plot where size represents frequency
    scatter = ax4.scatter(
        range(len(words)),
        [1] * len(words),
        s=[count * 10 for count in counts],
        alpha=0.6,
        c=counts,
        cmap="viridis",
    )

    # Add word labels
    for i, (word, count) in enumerate(zip(words, counts)):
        ax4.annotate(
            word,
            (i, 1),
            ha="center",
            va="center",
            fontsize=8,
            weight="bold" if count > word_freq.most_common(10)[-1][1] else "normal",
        )

    ax4.set_xlim(-1, len(words))
    ax4.set_ylim(0.5, 1.5)
    ax4.set_title("Word Frequency Bubble Chart", fontsize=14, fontweight="bold")
    ax4.set_xlabel("Words (ordered by frequency)", fontsize=12)
    ax4.set_yticks([])
    ax4.grid(True, alpha=0.3)

    # Add colorbar for the scatter plot
    cbar = plt.colorbar(scatter, ax=ax4)
    cbar.set_label("Frequency", fontsize=10)

    plt.tight_layout()

    # Save the plot
    output_path = os.path.join(output_dir, "german_word_frequency_analysis.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Visualization saved to: {output_path}")

    return fig


def save_frequency_data(word_freq, output_dir="."):
    """Save frequency data to CSV and text files"""
    # Convert to DataFrame
    df = pd.DataFrame(word_freq.most_common(), columns=["Word", "Frequency"])

    # Save to CSV
    csv_path = os.path.join(output_dir, "german_word_frequency.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Frequency data saved to: {csv_path}")

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

    return df


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

    print("\nTop 20 Most Frequent Words:")
    print("-" * 40)
    for i, (word, count) in enumerate(word_freq.most_common(20), 1):
        print(f"{i:2d}. {word:15s} : {count:4d}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze German word frequency from Anki deck"
    )
    parser.add_argument("input_file", help="Path to the German text file")
    parser.add_argument(
        "--top-n",
        type=int,
        default=50,
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
    df = save_frequency_data(word_freq, args.output_dir)

    # Create visualizations
    print("Creating visualizations...")
    create_visualizations(word_freq, args.top_n, args.output_dir)

    print(f"\nAnalysis complete! Check the output directory: {args.output_dir}")


if __name__ == "__main__":
    main()
