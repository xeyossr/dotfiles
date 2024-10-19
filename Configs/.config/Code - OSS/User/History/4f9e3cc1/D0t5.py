from flask import Flask, render_template, redirect, url_for, request, session, flash
import mysql.connector  # MySQL/MariaDB bağlantısı için
import json
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'xeyoss'

# MySQL/MariaDB bağlantı bilgileri
DATABASE_CONFIG = {
    'user': 'root',
    'password': 'xeyoss',
    'host': 'localhost',
    'database': 'booklib',
    'charset': 'utf8mb4',
}

# Veritabanına bağlanma
def get_db():
    return mysql.connector.connect(**DATABASE_CONFIG)

# Kullanıcıyı veritabanından çekme
def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# JSON dosyasını oku
def load_books():
    with open('books.json', 'r', encoding='utf-8') as f:
        books = json.load(f)
    return books

# Giriş sayfası
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['profile_image'] = user['profile_image']
            flash('Başarıyla giriş yaptınız!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Geçersiz kullanıcı adı veya şifre', 'danger')

    return render_template('login.html')

# Çıkış yapma
@app.route('/logout')
def logout():
    session.clear()
    flash('Çıkış yaptınız', 'success')
    return redirect(url_for('login'))

@app.route('/', methods=['GET'])
def index():
    # Eğer kullanıcı oturumda değilse, PHP login sayfasına yönlendir
    if 'user_id' not in session:
        return redirect("http://localhost/login.php")  # PHP login sayfası

    query = request.args.get('query')
    books = load_books()

    if query:
        # Arama yap: kitap başlıkları ve yazarlar üzerinden arama
        books = [book for book in books if query.lower() in book['title'].lower() or query.lower() in book['author'].lower()]

    return render_template('index.html', books=books)


# Kitap detayı: Bir kitaba tıklandığında detay sayfasına git
@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = load_books()
    book = next((book for book in books if book['id'] == book_id), None)

    if book is None:
        return redirect(url_for('index'))

    return render_template('book_details.html', book=book)

# Kitap okuma sayfası: Oku butonuna basıldığında kitabı okumaya başla
@app.route('/read/<int:book_id>')
def read_book(book_id):
    books = load_books()
    book = next((book for book in books if book['id'] == book_id), None)

    if book is None:
        return redirect(url_for('index'))

    # JSON formatında tutulan içerikleri çözümleyelim
    pages = book['content']
    
    return render_template('reader.html', pages=pages, title=book['title'])

# Flask uygulamasını çalıştırma
if __name__ == '__main__':
    app.run(port=2000, debug=True)
