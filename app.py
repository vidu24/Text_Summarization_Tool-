# app.py

from flask import Flask, render_template, request
from cli_summarizer import summarize_text_extractive  # Import your summarization function

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles requests for the homepage.
    - On GET: Renders the empty form.
    - On POST: Processes the user's text, summarizes it, and renders the page with the summary.
    """
    summary = ""
    original_text = ""

    if request.method == 'POST':
        # Get the text from the form
        original_text = request.form['text_to_summarize']

        if original_text:
            # Call your summarization function
            # We'll stick with 3 sentences for now, but you could make this configurable
            summary = summarize_text_extractive(original_text, sentences_count=3)
        else:
            summary = "Error: Please provide some text to summarize."
    
    # Render the HTML template, passing the variables
    return render_template('index.html', summary=summary, original_text=original_text)

if __name__ == '__main__':
    # Run the Flask application in debug mode
    # debug=True allows for automatic reloading when you make changes
    app.run(debug=True)
