import sqlite3
import os

def create_database():
    db_file = 'database.db'
    
    # Veritabanı dosyasının varlığını kontrol et
    if not os.path.exists(db_file):
        # Veritabanı dosyası yoksa oluştur
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Tabloyu oluştur
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_points (
                user_id TEXT PRIMARY KEY,
                total_characters INTEGER DEFAULT 0,
                total_voice_time INTEGER DEFAULT 0,
                total_points INTEGER DEFAULT 0
            )
        ''')
        
        # Değişiklikleri kaydet ve bağlantıyı kapat
        conn.commit()
        conn.close()
        print(f"{db_file} oluşturuldu ve tablo oluşturuldu.")
    else:
        print(f"{db_file} zaten mevcut.")

if __name__ == '__main__':
    create_database()
