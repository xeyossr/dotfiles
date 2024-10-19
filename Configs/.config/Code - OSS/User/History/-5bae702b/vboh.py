import sqlite3

# Veritabanını başlat
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Kitap tablosunu oluştur
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            description TEXT,
            cover_image TEXT,
            content TEXT
        )
    ''')
    
    # Test verisi ekle
    cursor.execute('''
        INSERT INTO books (title, author, description, cover_image, content) 
        VALUES (?, ?, ?, ?, ?)
    ''', ("Kitap 1", "Yazar 1", "Açıklama 1", "/static/images/cover1.jpg", '{"1": "Birinci sayfa içeriği", "2": "İkinci sayfa içeriği"}'))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
