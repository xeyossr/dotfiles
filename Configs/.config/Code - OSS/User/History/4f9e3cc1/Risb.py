from flask import Flask, render_template, redirect, url_for, request, session, flash
import mysql.connector  # MySQL/MariaDB bağlantısı için
import json
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)


# JSON dosyasını oku
def load_books():
    with open('books.json', 'r', encoding='utf-8') as f:
        books = json.load(f)
    return books

@app.route('/', methods=['GET'])
def index():
    # Eğer kullanıcı oturumda değilse, PHP login sayfasına yönlendir
    if 'user_id' not in session:
        return redirect("http://localhost:2000/login.php")  # PHP login sayfası

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
