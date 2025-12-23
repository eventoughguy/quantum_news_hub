from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def get_news():
    conn = sqlite3.connect("quantum_news.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, url, summary, date FROM news ORDER BY date DESC")
    news = cursor.fetchall()
    conn.close()
    return news

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_news")
def get_news_json():
    return jsonify(get_news())

if __name__ == "__main__":
    app.run(debug=True)