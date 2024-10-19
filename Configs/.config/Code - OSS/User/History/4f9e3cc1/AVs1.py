from flask import Flask, render_template, redirect, url_for, request, session, flash
import pymysql
import json
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'b2r$93!jns#1dp@&lqk02fn@dk!'

def db_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="xeyoss",
        database="booklib",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # Burada DictCursor kullanıyoruz
    )
    return connection

# Veritabanından kitapları yükleme
def load_books():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()  # Tüm kitapları al
    cursor.close()
    conn.close()
    return books

@app.route('/', methods=['GET'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    query = request.args.get('query')
    books = load_books()  # Veritabanından kitapları al

    if query:
        # Arama yap: kitap başlıkları ve yazarlar üzerinden arama
        books = [book for book in books if query.lower() in book['title'].lower() or query.lower() in book['author'].lower()]

    return render_template('index.html', books=books)

def load_books_to_db():
    books = load_books()  # JSON dosyasını yükle
    conn = db_connection()
    cursor = conn.cursor()

    for book in books:
        cursor.execute("""
            INSERT INTO books (title, author, description, cover_image, content) 
            VALUES (%s, %s, %s, %s, %s)
        """, (book['title'], book['author'], book['description'], book['cover_image'], json.dumps(book['content'])))

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and user['password'] == password:
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            flash('Kullanıcı adı veya şifre yanlış')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Oturumdan kullanıcı adını kaldır
    return redirect(url_for('login'))  # Anasayfaya yönlendir

# Kitap detayı: Bir kitaba tıklandığında detay sayfasına git
@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = load_books()  # Veritabanından kitapları al
    book = next((book for book in books if book['id'] == book_id), None)

    if book is None:
        return redirect(url_for('index'))

    return render_template('book_details.html', book=book)

# Kitap okuma sayfası: Oku butonuna basıldığında kitabı okumaya başla
@app.route('/read/<int:book_id>')
def read_book(book_id):
    books = load_books()  # Veritabanından kitapları al
    book = next((book for book in books if book['id'] == book_id), None)

    if book is None:
        return redirect(url_for('index'))

    # JSON formatında tutulan içerikleri çözümleyelim
    pages = book['content']
    
    return render_template('reader.html', pages=pages, title=book['title'])

# Flask uygulamasını çalıştırma
if __name__ == '__main__':
    load_books_to_db()  # JSON'daki kitapları veritabanına yükle
    app.run(port=2000, debug=True)
