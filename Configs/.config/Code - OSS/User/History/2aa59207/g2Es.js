const fs = require('fs');
const { Client, Collection, Intents } = require('discord.js');
const config = require('./config.json');

// Client oluştur
const client = new Client({ intents: [Intents.FLAGS.GUILDS] });

// Komutlar ve eventler için koleksiyonlar oluştur
client.commands = new Collection();

// Commands klasöründen komutları yüklüyoruz
const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));
for (const file of commandFiles) {
    const command = require(`./commands/${file}`);
    client.commands.set(command.data.name, command);
}

// Events klasöründen eventleri yüklüyoruz
const eventFiles = fs.readdirSync('./events').filter(file => file.endsWith('.js'));
for (const file of eventFiles) {
    const event = require(`./events/${file}`);
    if (event.once) {
        client.once(event.name, (...args) => event.execute(...args, client));
    } else {
        client.on(event.name, (...args) => event.execute(...args, client));
    }
}


client.on('messageCreate', async (message) => {
    if (message.author.bot) return; // Bot mesajlarını atla

    const userId = message.author.id;
    const characterCount = message.content.length;

    // Veritabanında kullanıcıyı güncelle
    await updateUserPoints(userId, characterCount);
});

async function updateUserPoints(userId, characterCount) {
    // Veritabanına bağlan
    const db = require('../database.js');

    // Kullanıcının puanlarını güncelle
    db.query(`INSERT INTO user_points (user_id, total_characters, total_points) VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE total_characters = total_characters + ?, total_points = total_points + ?`, [userId, characterCount, characterCount, characterCount]);
}


client.on('voiceStateUpdate', async (oldState, newState) => {
    if (newState.channel) { // Kullanıcı bir ses kanalına katıldıysa
        const userId = newState.id;

        // Başlangıç zamanını kaydet
        const joinTime = Date.now();

        // Ses kanalından çıktığında süreyi hesapla
        newState.guild.voiceStates.on('end', async () => {
            const voiceDuration = Math.floor((Date.now() - joinTime) / 1000); // Süreyi saniye cinsinden al

            // Kullanıcının puanlarını güncelle
            await updateUserVoicePoints(userId, voiceDuration);
        });
    }
});

async function updateUserVoicePoints(userId, duration) {
    const db = require('../database.js');
    // Kullanıcının ses puanlarını güncelle
    db.query(`INSERT INTO user_points (user_id, total_voice_time, total_points) VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE total_voice_time = total_voice_time + ?, total_points = total_points + ?`, [userId, duration, duration, duration]);
}

// Discord'a giriş yap
client.login(config.token);
