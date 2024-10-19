const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { removeWarning, getWarnings } = require('../database.js');
const config = require('../config.json'); // config dosyanızı buradan alın

module.exports = {
    data: new SlashCommandBuilder()
        .setName('unwarn')
        .setDescription('Kullanıcıdan warn kaldırır')
        .addUserOption(option => 
            option.setName('hedef')
            .setDescription('Warn kaldıracağın kullanıcıyı seç')
            .setRequired(true))
        .addIntegerOption(option => 
            option.setName('seviye')
            .setDescription('Kaldırılacak warn seviyesini seç')
            .setRequired(true)),
    async execute(interaction) {
        const target = interaction.options.getUser('hedef');
        const level = interaction.options.getInteger('seviye');

        // Kullanıcının var olan warnlarını getir
        getWarnings(target.id, async (warnings) => {
            const embed = new MessageEmbed()
                .setColor('#00cc99') // Yeşil renk
                .setTitle(`✅ ${target.tag} Uyarısı Kaldırıldı`)
                .addField('Warn Seviyesi', `${level}`, true)
                .setFooter({ text: `${target.tag} kullanıcısından ${level} seviyesindeki warn başarıyla kaldırıldı.` })
                .setTimestamp();

            if (warnings.length === 0) {
                return interaction.reply({ content: `${target.tag} kullanıcısında hiç warn bulunmuyor.`, ephemeral: true });
            }

            // Veritabanından warn kaldır
            const changes = await removeWarning(target.id, level);
            if (changes > 0) {
                interaction.reply({ embeds: [embed] });
            } else {
                interaction.reply({ content: `Bu seviyede bir warn bulunamadı.`, ephemeral: true });
            }
        });
    }
};
