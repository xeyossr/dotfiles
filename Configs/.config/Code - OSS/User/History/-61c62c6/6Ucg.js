const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Veritabanı dosyasını oluştur veya bağlan
const db = new sqlite3.Database(path.join(__dirname, 'warnings.db'), (err) => {
    if (err) {
        console.error('Veritabanına bağlanırken hata oluştu:', err);
    } else {
        console.log('Veritabanına bağlanıldı.');
    }
});

// Warn tablosunu oluştur
db.run(`
    CREATE TABLE IF NOT EXISTS warnings (
        userId TEXT,
        level INTEGER,
        description TEXT,
        executorId TEXT,
        date TEXT
    )
`);

// Ban tablosunu oluştur
db.run(`
    CREATE TABLE IF NOT EXISTS bans (
        userId TEXT,
        banDate TEXT,
        banReason TEXT,
        executorId TEXT,
        duration INTEGER
    )
`);

// Warn ekleme fonksiyonu
function addWarning(userId, level, description, executorId) {
    const date = new Date().toISOString();
    db.run(`
        INSERT INTO warnings (userId, level, description, executorId, date)
        VALUES (?, ?, ?, ?, ?)
    `, [userId, level, description, executorId, date], function(err) {
        if (err) {
            console.error('Warn eklerken hata oluştu:', err);
        }
    });
}

// Warn silme fonksiyonu (belirli seviyede)
function removeWarning(userId, level) {
    return new Promise((resolve, reject) => {
        // İlk eşleşen kaydı silmek için ROWID kullanıyoruz
        db.run(`DELETE FROM warnings WHERE userId = ? AND level = ?`, [userId, level], function (err) {
            if (err) {
                console.error(err.message);
                reject(err);
            } else {
                resolve(this.changes); // Silinen satır sayısını döndür
            }
        });
    });
}

// Kullanıcının tüm uyarılarını getirme fonksiyonu
function getWarnings(userId, callback) {
    db.all(`SELECT * FROM warnings WHERE userId = ?`, [userId], (err, rows) => {
        if (err) {
            console.error(err.message);
            return callback([]);
        }
        callback(rows); // Kullanıcıya ait warnları geri döndür
    });
}

// Ban ekleme fonksiyonu
function addBan(userId, reason, executorId, duration) {
    const banDate = new Date().toISOString();
    db.run(`
        INSERT INTO bans (userId, banDate, banReason, executorId, duration)
        VALUES (?, ?, ?, ?, ?)
    `, [userId, banDate, reason, executorId, duration], function(err) {
        if (err) {
            console.error('Ban eklerken hata oluştu:', err);
        }
    });
}

// Kullanıcının ban durumunu kontrol etme fonksiyonu
function checkBanStatus(userId, callback) {
    db.get(`SELECT * FROM bans WHERE userId = ?`, [userId], (err, row) => {
        if (err) {
            console.error(err.message);
            return callback(null);
        }
        callback(row); // Kullanıcının ban bilgilerini geri döndür
    });
}

// Banı kaldırma fonksiyonu
function removeBan(userId) {
    return new Promise((resolve, reject) => {
        db.run(`DELETE FROM bans WHERE userId = ?`, [userId], function (err) {
            if (err) {
                console.error(err.message);
                reject(err);
            } else {
                resolve(this.changes); // Silinen satır sayısını döndür
            }
        });
    });
}

module.exports = {
    addWarning,
    removeWarning,
    getWarnings,
    addBan,
    checkBanStatus,
    removeBan
};
