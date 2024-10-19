const { SlashCommandBuilder } = require('@discordjs/builders');
const { addWarning, getWarnings } = require('../database.js');

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

        // Veritabanına warn ekle
        addWarning(target.id, level, description, executor);

        // Warn puanlarını hesapla
        getWarnings(target.id, (warnings) => {
            let totalPoints = warnings.reduce((acc, warn) => acc + warn.level, 0);
            
            // Eğer warn puanı 20'yi geçerse banla
            if (totalPoints >= 20) {
                const guild = interaction.guild;
                const member = guild.members.cache.get(target.id);
                if (member) {
                    member.ban({ reason: `Toplam 20 warn puanına ulaşıldı.` });
                    interaction.reply(`${target.tag} adlı kullanıcı banlandı! Toplam warn puanı: ${totalPoints}`);
                }
            } else {
                interaction.reply(`${target.tag} adlı kullanıcıya ${level} seviyesinde warn verildi. Toplam warn puanı: ${totalPoints}`);
            }
        });
    }
};
