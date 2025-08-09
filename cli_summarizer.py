# cli_summarizer.py

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import sys

# Define the language for summarization
LANGUAGE = "english"

def summarize_text_extractive(text_content: str, sentences_count: int = 5) -> str:
    """
    Summarizes the given text content using an extractive summarization method (TextRank).

    Args:
        text_content (str): The input text to be summarized.
        sentences_count (int): The desired number of sentences in the summary.

    Returns:
        str: The generated extractive summary.
    """
    if not text_content or len(text_content.strip()) == 0:
        return "Error: No text provided to summarize."

    # 1. Parse the input text
    parser = PlaintextParser.from_string(text_content, Tokenizer(LANGUAGE))

    # 2. Initialize the stemmer
    stemmer = Stemmer(LANGUAGE)

    # 3. Initialize the TextRank summarizer
    summarizer = TextRankSummarizer(stemmer)

    # 4. Set stop words
    summarizer.stop_words = get_stop_words(LANGUAGE)

    # 5. Generate the summary
    summary_sentences = summarizer(parser.document, sentences_count)

    # 6. Join the summarized sentences into a single string
    final_summary = " ".join([str(sentence) for sentence in summary_sentences])

    return final_summary

if __name__ == "__main__":
    # Handle both file input and direct user input
    input_text = ""
    
    # Check if a file path is provided as a command-line argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                input_text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    else:
        # If no file path is provided, prompt the user for multi-line input
        print("Please enter the text to summarize. Press Ctrl+D (or Ctrl+Z on Windows) followed by Enter to finish.")
        try:
            # sys.stdin.read() reads all subsequent input until EOF (Ctrl+D/Ctrl+Z)
            input_text = sys.stdin.read()
        except KeyboardInterrupt:
            # This handles cases where the user just presses Ctrl+C
            print("\nOperation cancelled.")
            sys.exit(0)

    # You can specify the number of sentences for the summary here
    # You could also add a command-line flag for this later if you want

    desired_sentences = int(input("Enter the number of sentences for the summary (Atleast 5 sentences): ") )

    # Check if the user provided any text at all
    if not input_text or len(input_text.strip()) == 0:
        print("\nNo text was provided. Exiting.")
        sys.exit(1)

    print(f"\nGenerating a summary with {desired_sentences} sentences...\n")

    # Call the summarization function
    summary = summarize_text_extractive(input_text, desired_sentences)

    # Print the generated summary to the console
    print("--- Generated Summary ---")
    print(summary)
    print("-------------------------\n")
