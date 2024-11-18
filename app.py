from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Veritabanı bağlantısı
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ana sayfa
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('deneme_listesi'))
    return render_template('index.html')

# Kayıt sayfası
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Giriş sayfası
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('deneme_listesi'))
        else:
            return 'Hatalı kullanıcı adı veya şifre', 401

    return render_template('login.html')

# Deneme listesi
@app.route('/denemeler', methods=['GET', 'POST'])
def deneme_listesi():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    if request.method == 'POST':
        deneme_adi = request.form['denemeAdi']
        tarih = request.form['tarih']
        dogru_sayisi = request.form['dogruSayisi']
        yanlis_sayisi = request.form['yanlisSayisi']
        net = int(dogru_sayisi) - int(yanlis_sayisi) * 0.25
        conn.execute('INSERT INTO denemeler (user_id, deneme_adi, tarih, dogru_sayisi, yanlis_sayisi, net) VALUES (?, ?, ?, ?, ?, ?)', 
                     (session['user_id'], deneme_adi, tarih, dogru_sayisi, yanlis_sayisi, net))
        conn.commit()

    denemeler = conn.execute('SELECT * FROM denemeler WHERE user_id = ?', (session['user_id'],)).fetchall()
    conn.close()

    return render_template('denemeler.html', denemeler=denemeler)

if __name__ == '__main__':
    app.run(debug=True)
