const { SlashCommandBuilder } = require('@discordjs/builders');

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

        if (!warnings[target.id] || warnings[target.id].length === 0) {
            return interaction.reply(`${target.tag} kullanıcısında hiç warn bulunmuyor.`);
        }

        // İlgili seviyedeki warn'ı kaldır
        const warnIndex = warnings[target.id].findIndex(warn => warn.level === level);
        if (warnIndex !== -1) {
            warnings[target.id].splice(warnIndex, 1);
            return interaction.reply(`${target.tag} kullanıcısından ${level} seviyesindeki warn kaldırıldı.`);
        } else {
            return interaction.reply(`${target.tag} kullanıcısında ${level} seviyesinde bir warn bulunamadı.`);
        }
    }
};
