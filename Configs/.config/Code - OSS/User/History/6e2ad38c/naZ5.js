const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { getWarnings } = require('../database.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('showwarns')
        .setDescription('Kullanıcının tüm warnlarını gösterir')
        .addUserOption(option => 
            option.setName('hedef')
            .setDescription('Warnlarını görmek istediğin kullanıcıyı seç')
            .setRequired(true)),
    async execute(interaction) {
        const target = interaction.options.getUser('hedef');

        // Veritabanından warnları al
        getWarnings(target.id, (warnings) => {
            const embed = new MessageEmbed()
                .setColor('#3366ff') // Mavi renk
                .setTitle(`📜 ${target.tag} Kullanıcısının Warnları`);

            if (warnings.length === 0) {
                embed.setDescription(`${target.tag} kullanıcısında hiç warn bulunmuyor.`);
                return interaction.reply({ embeds: [embed] });
            }

            // Warn listesini göster
            warnings.forEach((warn, index) => {
                embed.addField(
                    `**${index + 1}. Warn**`
