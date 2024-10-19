const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('unmute')
        .setDescription('Bir kullanıcının susturmasını kaldırır.')
        .addUserOption(option => 
            option.setName('hedef')
            .setDescription('Susturmasını kaldırmak istediğin kullanıcıyı seç')
            .setRequired(true)),
    async execute(interaction) {
        const target = interaction.options.getUser('hedef');
        const executor = interaction.user.id;

        if (!interaction.member.permissions.has('MUTE_MEMBERS')) {
            return interaction.reply({
                content: '❌ Bu komutu kullanmak için yeterli yetkin yok.',
                ephemeral: true
            });
        }

        const member = interaction.guild.members.cache.get(target.id);

        if (!member || !member.isCommunicationDisabled()) {
            return interaction.reply({
                content: `❌ Kullanıcı susturulmamış veya bulunamadı.`,
                ephemeral: true
            });
        }

        await member.timeout(null);

        const embed = new MessageEmbed()
            .setColor('#00ff00')
            .setTitle(`🔊 ${target.tag} Susturma Kaldırıldı`)
            .addField('Susturmayı Kaldıran', `<@${executor}>`, true)
            .setTimestamp();

        interaction.reply({ embeds: [embed] });
    }
};
