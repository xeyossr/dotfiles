const { SlashCommandBuilder } = require('@discordjs/builders');
const { Permissions } = require('discord.js');

// Uyarıları kaydetmek için geçici veri yapısı
let warnings = {};

module.exports = {
    data: new SlashCommandBuilder()
        .setName('warn')
        .setDescription('Kullanıcıya warn ekler')
        .addUserOption(option => 
            option.setName('hedef')
            .setDescription('Warn vereceğin kullanıcıyı seç')
            .setRequired(true))
        .addIntegerOption(option => 
            option.setName('seviye')
            .setDescription('Warn seviyesini belirt')
            .setRequired(true))
        .addStringOption(option => 
            option.setName('açıklama')
            .setDescription('Warn sebebi')
            .setRequired(false)),
    async execute(interaction) {
        const target = interaction.options.getUser('hedef');
        const level = interaction.options.getInteger('seviye');
        const description = interaction.options.getString('açıklama') || 'Sebep belirtilmemiş';
        const executor = interaction.user.id;

        // Kullanıcının var olan uyarılarını kontrol et
        if (!warnings[target.id]) {
            warnings[target.id] = [];
        }

        // Yeni warn'ı kaydet
        warnings[target.id].push({ level, description, executor });

        // Puan hesapla ve banlama kontrolü yap
        let totalPoints = warnings[target.id].reduce((acc, warn) => acc + warn.level, 0);
        if (totalPoints >= 20) {
            const guild = interaction.guild;
            const member = guild.members.cache.get(target.id);
            if (member) {
                await member.ban({ reason: `Toplam 20 warn puanına ulaşıldı.` });
                return interaction.reply(`${target.tag} adlı kullanıcı banlandı! Toplam warn puanı: ${totalPoints}`);
            }
        }

        // Kullanıcıya bilgi ver
        return interaction.reply(`${target.tag} adlı kullanıcıya ${level} seviyesinde warn verildi. Toplam warn puanı: ${totalPoints}`);
    }
};
