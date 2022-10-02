import os
import re
import csv

from flask import Flask, request, redirect, render_template

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():
    # If this is a post, divert to the appropriate function
    slang_content = ""
    slanged_parsed = []
    last_content = "" 
    if request.form:
        action = request.form.get("action")
        if action == "load_data":
            slang_content = request.form.get("slang_content")
            print("CONTENT", slang_content)
            slanged_parsed, last_content = parse_slang(slang_content)
    return render_template("index.html", slang_content = slang_content,
        highlighted_text = slanged_parsed,
        post_highlight = last_content)

def parse_slang(slang_content):
    slanged_parsed = []
    last_end = 0
    for slang_match in SLANG_PAT.finditer(slang_content):
        slang_definition = SLANG_WORDS.get(slang_match.group().lower(), "")
        slanged_parsed.append((slang_content[last_end:slang_match.start()], slang_match.group(), slang_definition))
        last_end = slang_match.end()
    last_content = slang_content[last_end:]
    return slanged_parsed, last_content

SLANG_FILE = "slang_words.csv"

def load_slang():
    slang_words = {}
    with open(SLANG_FILE, encoding="utf8") as f:
        reader = csv.reader(f)
        next(reader, None) # skip first line
        for slang, definition in reader:
            slang_words[slang.lower()] = definition
    return slang_words

if __name__ == "__main__":
    SLANG_WORDS = load_slang()

    SLANG_RE_PATTERN = ""
    for slang in SLANG_WORDS:
        SLANG_RE_PATTERN += fr"\b{re.escape(slang)}\b|"
    # Remove last bar
    SLANG_RE_PATTERN = SLANG_RE_PATTERN[:-1]

    SLANG_PAT = re.compile(SLANG_RE_PATTERN, re.I)
    app.run(host = '0.0.0.0', debug = True)
