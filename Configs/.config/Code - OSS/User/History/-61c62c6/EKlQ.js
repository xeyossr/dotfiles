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
    db.run(`
        DELETE FROM warnings
        WHERE userId = ? AND level = ?
        LIMIT 1
    `, [userId, level], function(err) {
        if (err) {
            console.error('Warn silinirken hata oluştu:', err);
        }
    });
}

// Kullanıcının tüm warnlarını getirme fonksiyonu
function getWarnings(userId, callback) {
    db.all(`
        SELECT * FROM warnings
        WHERE userId = ?
    `, [userId], (err, rows) => {
        if (err) {
            console.error('Warnlar alınırken hata oluştu:', err);
            callback([]);
        } else {
            callback(rows);
        }
    });
}

module.exports = {
    addWarning,
    removeWarning,
    getWarnings
};
