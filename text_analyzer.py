"""Text Analyzer - CS 250 Final Project (Fall 2026), Askatbek.

Reads a .txt file and tells you if the text is too long, too repetitive, or too slow to start.
Run:  python text_analyzer.py
"""

import math
import matplotlib.pyplot as plt

# Small words we do not want in the "top words" list (a set is fast for "is it in?" checks)
STOP_WORDS = {"the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
              "to", "of", "in", "on", "at", "for", "with", "it", "this", "that",
              "i", "you", "he", "she", "we", "they", "my", "be", "as", "by", "so",
              "than", "may", "from", "about", "when", "has", "have", "there",
              "not", "if", "can", "will", "our", "your", "us", "me", "one"}

# My own rules of thumb for the tips (you can change them)
MAX_REPEAT = 0.05         # one word should not be more than 5% of all words
MAX_FIRST_SENTENCE = 25   # the first sentence should not be longer than 25 words


def read_text(filename):
    """Read a text file and return its content as one string.
    Return an empty string if the file does not exist."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"File '{filename}' was not found.")
        return ""


def clean_words(text):
    """Return a list of lowercase words without punctuation at the edges."""
    words = [word.strip(".,!?;:\"'()-") for word in text.lower().split()]
    return [word for word in words if word != ""]


def count_sentences(text):
    """Return the number of sentences (the marks . ! ? are counted)."""
    return sum(text.count(mark) for mark in ".!?")


def count_words(words):
    """Return a dictionary {word: how many times it appears}."""
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_words(counts, n=10, skip=STOP_WORDS):
    """Return the n most common words as a list of (word, count) tuples.
    Words in the set 'skip' are ignored."""
    items = [(word, number) for word, number in counts.items() if word not in skip]
    items.sort(key=lambda pair: pair[1], reverse=True)
    return items[:n]


def speaking_time(word_count, wpm=150):
    """Return speaking time as a tuple (minutes, seconds).
    wpm = words per minute (150 is my assumption, you can change it)."""
    total_seconds = math.ceil(word_count / wpm * 60)
    return total_seconds // 60, total_seconds % 60


def get_intro(text, n=30):
    """Return the first n words of the text as one string."""
    return " ".join(text.split()[:n])


def first_sentence_length(text):
    """Return how many words the first sentence has."""
    for i, char in enumerate(text):
        if char in ".!?":
            return len(text[:i].split())
    return len(text.split())


def give_feedback(total_seconds, repeat_share, first_len, max_minutes=5):
    """Return a list of tips: is the text too long, too repetitive, or too slow to start?"""
    tips = []
    if total_seconds > max_minutes * 60:
        tips.append(f"Too long: it takes more than {max_minutes} min to say.")
    if repeat_share > MAX_REPEAT:
        tips.append(f"Repetitive: one word is {repeat_share:.0%} of the whole text.")
    if first_len > MAX_FIRST_SENTENCE:
        tips.append(f"Slow start: the first sentence has {first_len} words.")
    if not tips:
        tips.append("Looks good!")
    return tips


def plot_top_words(top, title="Most common words"):
    """Draw a bar chart of the most common words."""
    names = [word for word, number in top]
    numbers = [number for word, number in top]
    plt.bar(names, numbers)
    plt.title(title)
    plt.xlabel("Word")
    plt.ylabel("Times used")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main(filename=None, max_minutes=5):
    """Analyze one text file: print the results, the tips, and draw the graph.
    If no file name is given, ask the user for it."""
    if filename is None:
        filename = input("Text file name (for example sample_good.txt): ")
    text = read_text(filename)
    if text == "":
        return

    words = clean_words(text)
    counts = count_words(words)
    top = top_words(counts)
    minutes, seconds = speaking_time(len(words))
    repeat_share = top[0][1] / len(words) if top else 0
    tips = give_feedback(minutes * 60 + seconds, repeat_share,
                         first_sentence_length(text), max_minutes)

    print(f"===== {filename} =====")
    print(f"Words: {len(words)} | Sentences: {count_sentences(text)}")
    print(f"Speaking time: {minutes} min {seconds} sec")
    print(f"Intro (first 30 words): {get_intro(text)}")
    print("Top words:", top)
    for tip in tips:
        print("Tip:", tip)
    plot_top_words(top, f"Most common words: {filename}")


if __name__ == "__main__":
    main()
