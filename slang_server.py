import os
import csv

from flask import Flask, request, redirect, render_template

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():
    # If this is a post, divert to the appropriate function
    translated_slang = ""
    if request.form:
        action = request.form.get("action")
        if action == "load_data":
            content = request.form.get("content")
            print("CONTENT", content)
            translated_slang = translate_slang(content)
    return render_template("index.html")

def translate_slang(content):
    return content

SLANG_FILE = "slang_words.csv"

def load_slang():
    slang_words = []
    with open(SLANG_FILE) as f:
        reader = csv.reader(f)
        next(reader, None) # skip first line
        for slang, definition in reader:
            slang_words.append((slang, definition))
    return slang_words

if __name__ == "__main__":
    SLANG_WORDS = load_slang()
    app.run(host = '0.0.0.0', debug = True)
