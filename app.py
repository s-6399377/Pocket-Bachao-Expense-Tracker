# Banaya: Sukriti, CSE 1st Year, Chandigarh Group Of Colleges
from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from collections import defaultdict
app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('pocket.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.execute('CREATE TABLE IF NOT EXISTS kharcha (id INTEGER PRIMARY KEY, amount REAL, category TEXT, note TEXT, date TEXT)')
    db.commit()

@app.route('/')
def dashboard():
    db = get_db()
    kharche = db.execute('SELECT * FROM kharcha ORDER BY id DESC').fetchall()
    total = db.execute('SELECT SUM(amount) FROM kharcha').fetchone()[0] or 0  
    budget = 3000
    jeb = budget- total

    category_data = defaultdict(int)
    for item in kharche:
        category_data[item['category']] += item['amount']

    db.close()

    status = "Abhi to Ameer Hu😎" if jeb > 1000 else "Bhai Bach Ke Reh🤔" if jeb > 0 else "Gareeb Ho Gaya💀"
    return render_template('index.html', kharche=kharche, total=total, jeb=jeb, status=status, chart_data=dict(category_data))

@app.route('/add', methods=['POST'])
def add_kharcha():
    db = get_db()
    db.execute('INSERT INTO kharcha (amount, category, note, date) VALUES (?,?,?,?)',
               [request.form['amount'], request.form['category'], request.form['note'], datetime.now()])
    db.commit()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
