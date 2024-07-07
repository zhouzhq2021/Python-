from flask import Flask, render_template, request, flash, redirect
import pandas as pd
import sqlite3
import os
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('还没有上传文件')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('无')
            return redirect(request.url)
        if file:
            filename = file.filename
            file_extension = filename.split('.')[-1]
            if file_extension in ['txt', 'csv', 'xlsx', 'json']:
                db_filename = process_file(file, filename, file_extension)
                return redirect(f'/show_data/{db_filename}')
            else:
                flash('文件格式不支持')
    return render_template('index.html')
def process_file(file, filename, file_extension):
    if file_extension == 'csv':
        df = pd.read_csv(file)
    elif file_extension == 'txt':
        df = pd.read_csv(file, delimiter='\t')
    elif file_extension == 'xlsx':
        df = pd.read_excel(file)
    elif file_extension == 'json':
        df = pd.read_json(file)
    db_filename = filename.rsplit('.', 1)[0] + '.db'
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Tournaments (
            id INTEGER PRIMARY KEY,
            month varchar(15),
            day INTEGER,
            time varchar(15),
            team1 varchar(50),
            score1 INTEGER,
            score2 INTEGER,
            team2 varchar(50),
            status varchar(15),
            PenaltyKick varchar(15)
        )''')

    for i in range(len(df.index)):
        values = tuple(str(val) for val in df.iloc[i])
        placeholders = ', '.join(['?'] * len(df.columns))
        sql_text = f"INSERT INTO Tournaments VALUES ({placeholders})"
        cur.execute(sql_text, values)
        conn.commit()
    conn.commit()
    conn.close()
    return db_filename
@app.route('/show_data/<db_filename>')
def show_data(db_filename):
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    cur.execute('SELECT * FROM Tournaments')
    data = cur.fetchall()
    conn.close()
    return render_template('show_data.html', data=data)
if __name__ == '__main__':
    app.run(debug=True)