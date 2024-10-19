const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('ping')
        .setDescription('Botun gecikmesini ölçer.'),
    async execute(interaction) {
        const ping = Date.now() - interaction.createdTimestamp;
        await interaction.reply(`Pong! Gecikme: ${ping}ms`);
    },
};
