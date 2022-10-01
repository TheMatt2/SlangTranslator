import os
import re
import csv

from flask import Flask, request, redirect, render_template

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():
    # If this is a post, divert to the appropriate function
    if request.form:
        action = request.form.get("action")
        if action == "load_data":
            load_data()

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host = '0.0.0.0')
