const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { addWarning, getWarnings } = require('../database.js');
const config = require('../config.json'); // config.json'dan sahip id'yi çekiyoruz

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

        // Komutu kullanan kişinin yetkisini kontrol et
        if (!interaction.member.permissions.has('BAN_MEMBERS') && executor !== config.sahipid) {
            return interaction.reply({ 
                content: "❌ Bu komutu kullanmak için yeterli yetkin yok. Ban yetkisine sahip olman gerekiyor.",
                ephemeral: true 
            });
        }

        // Veritabanına warn ekle
        addWarning(target.id, level, description, executor);

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
                .addField('Warnı Veren', `<@${executor}>`, true)
                .setFooter({ text: `Toplam Warn Puanı: ${totalPoints}` })
                .setTimestamp();

            // Eğer warn puanı 20'yi geçerse banla
            if (totalPoints >= 20) {
                const member = guild.members.cache.get(target.id);

                if (member) {
                    // Botun ban yetkisi olup olmadığını kontrol et
                    if (!interaction.guild.me.permissions.has('BAN_MEMBERS')) {
                        embed.setColor('#ff0000') // Kırmızı renk
                            .setTitle(`🚫 Banlama Yetkim Yok`)
                            .setDescription(`${target.tag} kullanıcısı 20 warn puanına ulaştı ancak banlama yetkim yok.`);
                    } else {
                        try {
                            await member.ban({ reason: `Toplam 20 warn puanına ulaşıldı.` });
                            embed.setColor('#ff0000') // Kırmızı renk
                                .setTitle(`🚫 ${target.tag} Banlandı`)
                                .setDescription(`${target.tag} toplam 20 warn puanına ulaştı ve banlandı.`);
                        } catch (error) {
                            embed.setColor('#ff0000') // Kırmızı renk
                                .setTitle(`🚫 Banlama Başarısız`)
                                .setDescription(`${target.tag} kullanıcısını banlamaya çalıştım fakat bir hata oluştu.`);
                            console.error('Banlama işlemi sırasında hata oluştu:', error);
                        }
                    }
                }
            }

            interaction.reply({ embeds: [embed] });
        });
    }
};
