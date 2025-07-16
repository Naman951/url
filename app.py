from flask import Flask, request, redirect, render_template
import string
import random
import json
import os

app = Flask(__name__)
DB_FILE = 'urls.json'

# Load database or create new
if os.path.exists(DB_FILE):
    with open(DB_FILE, 'r') as f:
        url_map = json.load(f)
else:
    url_map = {}

# Generate random short ID
def generate_short_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = ""
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_id = generate_short_id()
        while short_id in url_map:
            short_id = generate_short_id()
        url_map[short_id] = long_url
        with open(DB_FILE, 'w') as f:
            json.dump(url_map, f)
        short_url = request.host_url + short_id
    return render_template('index.html', short_url=short_url)

@app.route('/<short_id>')
def redirect_to_long_url(short_id):
    long_url = url_map.get(short_id)
    if long_url:
        return redirect(long_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
