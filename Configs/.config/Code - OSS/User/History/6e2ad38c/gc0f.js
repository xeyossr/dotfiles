const { SlashCommandBuilder } = require('@discordjs/builders');
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
            if (warnings.length === 0) {
                return interaction.reply(`${target.tag} kullanıcısında hiç warn bulunmuyor.`);
            }

            // Warn listesini göster
            let warnList = warnings.map((warn, index) => 
                `**${index + 1}.** Seviye: ${warn.level}, Sebep: ${warn.description}, Atan: <@${warn.executorId}>, Tarih: ${warn.date}`
            ).join('\n');
            interaction.reply(`**${target.tag}** kullanıcısının warnları:\n${warnList}`);
        });
    }
};
