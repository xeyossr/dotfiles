from flask import Flask, render_template, g, redirect, url_for
import sqlite3
import requests

# Uygulama tanımlaması
app = Flask(__name__)

# Veritabanı dosyası
DATABASE = 'database.db'

# Veritabanına bağlanma
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Uygulama kapandığında veritabanı bağlantısını kapatma
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Ana sayfa: Kitap listesi
@app.route('/', methods=['GET'])
def index():
    query = request.args.get('query')
    cur = get_db().cursor()
    
    if query:
        # Arama sorgusu varsa
        cur.execute("SELECT id, title, author, description, cover_image FROM books WHERE title LIKE ? OR author LIKE ?", ('%' + query + '%', '%' + query + '%'))
    else:
        # Tüm kitapları getir
        cur.execute("SELECT id, title, author, description, cover_image FROM books")
    
    books = cur.fetchall()  # Kitap listesini çek
    return render_template('index.html', books=books)

# Kitap detayı: Bir kitaba tıklandığında detay sayfasına git
@app.route('/book/<int:book_id>')
def book_details(book_id):
    cur = get_db().cursor()
    cur.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cur.fetchone()  # Kitap bilgilerini çek
    
    if book is None:
        return redirect(url_for('index'))
    
    return render_template('book_details.html', book=book)

# Kitap okuma sayfası: Oku butonuna basıldığında kitabı okumaya başla
@app.route('/read/<int:book_id>')
def read_book(book_id):
    cur = get_db().cursor()
    cur.execute("SELECT content FROM books WHERE id = ?", (book_id,))
    content = cur.fetchone()

    if content is None:
        return redirect(url_for('index'))
    
    # JSON formatında tutulan içerikleri çözümleyelim
    import json
    pages = json.loads(content[0])  # Sayfa içeriklerini al
    
    return render_template('reader.html', pages=pages)

# Flask uygulamasını çalıştırma
if __name__ == '__main__':
    app.run(port=2000, debug=True)
