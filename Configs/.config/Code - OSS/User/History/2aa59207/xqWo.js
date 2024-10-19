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

// Discord'a giriş yap
client.login(config.token);
