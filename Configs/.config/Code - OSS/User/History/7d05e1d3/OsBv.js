const { SlashCommandBuilder } = require('@discordjs/builders');
const { removeWarning, getWarnings } = require('../database.js');

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
        getWarnings(target.id, (warnings) => {
            if (warnings.length === 0) {
                return interaction.reply(`${target.tag} kullanıcısında hiç warn bulunmuyor.`);
            }

            // Warn kaldır
            removeWarning(target.id, level);
            interaction.reply(`${target.tag} kullanıcısından ${level} seviyesindeki warn kaldırıldı.`);
        });
    }
};
