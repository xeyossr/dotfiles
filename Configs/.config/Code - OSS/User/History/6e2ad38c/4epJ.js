const { SlashCommandBuilder } = require('@discordjs/builders');

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

        if (!warnings[target.id] || warnings[target.id].length === 0) {
            return interaction.reply(`${target.tag} kullanıcısında hiç warn bulunmuyor.`);
        }

        // Warn listesini göster
        let warnList = warnings[target.id].map((warn, index) => `**${index + 1}.** Seviye: ${warn.level}, Sebep: ${warn.description}, Atan: <@${warn.executor}>`).join('\n');
        return interaction.reply(`**${target.tag}** kullanıcısının warnları:\n${warnList}`);
    }
};
