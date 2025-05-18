from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'
BUDGET = 500

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    ausgaben = load_data()
    if request.method == 'POST':
        beschreibung = request.form['beschreibung']
        betrag = float(request.form['betrag'])
        ausgaben.append({'beschreibung': beschreibung, 'betrag': betrag})
        save_data(ausgaben)
        return redirect(url_for('index'))
    gesamtausgaben = sum(e['betrag'] for e in ausgaben)
    verbleibend = BUDGET - gesamtausgaben
    return render_template('index.html', ausgaben=ausgaben, budget=BUDGET,
                           gesamtausgaben=gesamtausgaben, verbleibend=verbleibend)
