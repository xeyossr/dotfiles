const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Veritabanı dosyalarının yollarını belirt
const warningsDbPath = path.join(__dirname, 'warnings.db');
const bansDbPath = path.join(__dirname, 'bans.db');

// Uyarı veritabanına bağlan
const warningsDb = new sqlite3.Database(warningsDbPath, (err) => {
    if (err) {
        console.error('Uyarı veritabanına bağlanırken hata oluştu:', err);
    } else {
        console.log('Uyarı veritabanına bağlanıldı.');
    }
});

// Ban veritabanına bağlan
const bansDb = new sqlite3.Database(bansDbPath, (err) => {
    if (err) {
        console.error('Ban veritabanına bağlanırken hata oluştu:', err);
    } else {
        console.log('Ban veritabanına bağlanıldı.');
    }
});

// Warn tablosunu oluştur
warningsDb.run(`
    CREATE TABLE IF NOT EXISTS warnings (
        userId TEXT,
        level INTEGER,
        description TEXT,
        executorId TEXT,
        date TEXT
    )
`);

// Ban tablosunu oluştur
bansDb.run(`
    CREATE TABLE IF NOT EXISTS bans (
        userId TEXT,
        guildId TEXT,
        banDate TEXT,
        duration INTEGER
    )
`);

// Warn ekleme fonksiyonu
function addWarning(userId, level, description, executorId) {
    const date = new Date().toISOString();
    warningsDb.run(`
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
        warningsDb.run(`DELETE FROM warnings WHERE userId = ? AND level = ?`, [userId, level], function (err) {
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
    warningsDb.all(`SELECT * FROM warnings WHERE userId = ?`, [userId], (err, rows) => {
        if (err) {
            console.error(err.message);
            return callback([]);
        }
        callback(rows); // Kullanıcıya ait warnları geri döndür
    });
}

// Ban ekleme fonksiyonu
function addBan(userId, guildId, duration) {
    const banDate = new Date().toISOString();
    bansDb.run(`
        INSERT INTO bans (userId, guildId, banDate, duration)
        VALUES (?, ?, ?, ?)
    `, [userId, guildId, banDate, duration], function(err) {
        if (err) {
            console.error('Ban eklerken hata oluştu:', err);
        }
    });
}

// Ban kaldırma fonksiyonu
async function removeBan(userId) {
    return new Promise((resolve, reject) => {
        bansDb.run(`DELETE FROM bans WHERE userId = ?`, [userId], function (err) {
            if (err) {
                console.error(err.message);
                reject(err);
            } else {
                resolve(this.changes); // Silinen satır sayısını döndür
            }
        });
    });
}

// Tüm yasaklı kullanıcıları alma fonksiyonu
async function getAllBannedUsers() {
    return new Promise((resolve, reject) => {
        bansDb.all(`SELECT * FROM bans`, [], (err, rows) => {
            if (err) {
                console.error(err.message);
                reject(err);
            } else {
                resolve(rows); // Yasaklı kullanıcıları geri döndür
            }
        });
    });
}

// Kullanıcının ban durumunu kontrol etme fonksiyonu
async function checkBanStatus(userId) {
    return new Promise((resolve, reject) => {
        bansDb.get(`SELECT * FROM bans WHERE userId = ?`, [userId], (err, row) => {
            if (err) {
                console.error(err.message);
                reject(err);
            } else {
                resolve(row); // Kullanıcının ban durumunu geri döndür
            }
        });
    });
}

// Modül dışa aktarma
module.exports = {
    addWarning,
    removeWarning,
    getWarnings,
    addBan,
    removeBan,
    getAllBannedUsers,
    checkBanStatus
};
