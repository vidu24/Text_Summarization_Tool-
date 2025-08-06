# cli_summarizer.py

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import sys

# Define the language for summarization
# You can change this to 'czech', 'slovak', etc., if needed
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
    # 1. Parse the input text
    # PlaintextParser is used for raw text. HtmlParser can be used for HTML content.
    parser = PlaintextParser.from_string(text_content, Tokenizer(LANGUAGE))

    # 2. Initialize the stemmer (for reducing words to their root form)
    # Stemming helps in treating different forms of a word as the same,
    # which can improve the accuracy of sentence scoring.
    stemmer = Stemmer(LANGUAGE)

    # 3. Initialize the TextRank summarizer
    # TextRank is a graph-based algorithm that ranks sentences based on their similarity.
    summarizer = TextRankSummarizer(stemmer)

    # 4. Set stop words (common words to ignore, like 'the', 'is', 'and')
    # Ignoring stop words helps focus on more meaningful content.
    summarizer.stop_words = get_stop_words(LANGUAGE)

    # 5. Generate the summary
    # The summarizer returns an iterable of Sentence objects.
    summary_sentences = summarizer(parser.document, sentences_count)

    # 6. Join the summarized sentences into a single string
    final_summary = " ".join([str(sentence) for sentence in summary_sentences])

    return final_summary

if __name__ == "__main__":
    # This block runs when the script is executed directly from the command line.

    # Check if text is provided as a command-line argument
    if len(sys.argv) > 1:
        # If arguments are provided, assume the first argument is the text file path
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
        # If no file path is provided, use a default example text
        print("No input file provided. Using a default example text.")
        input_text = """
        Artificial intelligence (AI) is rapidly transforming various industries, from healthcare to finance.
        Machine learning, a subset of AI, enables systems to learn from data without explicit programming.
        Deep learning, a further specialization, uses neural networks with many layers to model complex patterns.
        These technologies are driving innovations like autonomous vehicles, natural language processing, and advanced robotics.
        The ethical implications of AI development are also a significant area of discussion, focusing on bias, privacy, and job displacement.
        Researchers are continuously working on improving AI's capabilities and addressing its challenges to ensure responsible development.
        """
        print("\n--- Default Input Text ---")
        print(input_text)
        print("--------------------------\n")

    # You can specify the number of sentences for the summary here
    desired_sentences = 3

    print(f"Generating a summary with {desired_sentences} sentences...\n")

    # Call the summarization function
    summary = summarize_text_extractive(input_text, desired_sentences)

    # Print the generated summary to the console
    print("--- Generated Summary ---")
    print(summary)
    print("-------------------------\n")
