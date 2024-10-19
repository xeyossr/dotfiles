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
    
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (session['username'],))
    user = cursor.fetchone()

    books = load_books()  # Veritabanından kitapları al

    if query:
        # Arama yap: kitap başlıkları ve yazarlar üzerinden arama
        books = [book for book in books if query.lower() in book['title'].lower() or query.lower() in book['author'].lower()]

    return render_template('index.html', books=books, username=user['username'], profile_image=user['profile_image'], user_id=user['id'])

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

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'username' not in session or session['user_id'] != 1:
        return redirect(url_for('index'))  # Kullanıcı girişi yoksa veya kullanıcı ID'si 1 değilse yönlendir

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        cover_image = request.form['cover_image']
        content = request.form['content']  # JSON formatında alındığını varsayıyoruz

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO books (title, author, description, cover_image, content) 
            VALUES (%s, %s, %s, %s, %s)
        """, (title, author, description, cover_image, content))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Kitap başarıyla eklendi!')  # Başarılı ekleme için bildirim

    # Tüm kitapları veritabanından çek
    books = load_books_from_db() 

    return render_template('add_book.html', books=books)


@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    if 'username' not in session or session['user_id'] != 1:
        return redirect(url_for('index'))  # Kullanıcı girişi yoksa yönlendir

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Kitap başarıyla silindi!')  # Silme için bildirim
    return redirect(url_for('add_book'))  # Kitap ekleme sayfasına geri dön


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
            session['user_id'] = user['id']  # Kullanıcı ID'sini oturuma kaydet
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
    app.run(port=2000, debug=True)
