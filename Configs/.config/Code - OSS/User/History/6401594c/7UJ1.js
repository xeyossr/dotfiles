const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { addWarning, getWarnings, addBan } = require('../database.js');
const { ownerId } = require('../config.json'); // Sahip ID'sini config'den al

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
        const executor = interaction.user;

        // Kullanıcının ban yetkisi kontrolü
        if (!interaction.member.permissions.has('BAN_MEMBERS') && executor.id !== ownerId) {
            return interaction.reply({ content: 'Bu komutu kullanmak için yeterli izniniz yok.', ephemeral: true });
        }

        // Veritabanına warn ekle
        addWarning(target.id, level, description, executor.id);

        // Warn puanlarını hesapla
        getWarnings(target.id, async (warnings) => {
            let totalPoints = warnings.reduce((acc, warn) => acc + warn.level, 0);
            const guild = interaction.guild;

            // Warn embed mesajı
            const embed = new MessageEmbed()
                .setColor('#ffcc00') // Sarı renk
                .setTitle(`⚠️ ${target.tag} Uyarıldı`)
                .setDescription(`${target.tag} adlı kullanıcıya ${level} seviyesinde warn verildi.`)
                .addField('Warn Seviyesi', `${level}`, true)
                .addField('Sebep', `${description}`, true)
                .addField('Warnı Veren', `<@${executor.id}>`, true)
                .setFooter({ text: `Toplam Warn Puanı: ${totalPoints}` })
                .setTimestamp();

            // Eğer warn puanı 20'yi geçerse banla
            if (totalPoints >= 20) {
                const member = guild.members.cache.get(target.id);
                if (member) {
                    await member.ban({ reason: `Toplam 20 warn puanına ulaşıldı.` });
                    await addBan(target.id, guild.id, 25); // 25 gün ban ekle
                    embed.setColor('#ff0000') // Kırmızı renk
                        .setTitle(`🚫 ${target.tag} Banlandı`)
                        .setDescription(`${target.tag} toplam 20 warn puanına ulaştı ve banlandı. Ban süresi 25 gündür.`);
                }
            }

            interaction.reply({ embeds: [embed] });
        });
    }
};
