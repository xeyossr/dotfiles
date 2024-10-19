const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('mute')
        .setDescription('Bir kullanıcıyı susturur.')
        .addUserOption(option => 
            option.setName('hedef')
            .setDescription('Susturmak istediğin kullanıcıyı seç')
            .setRequired(true))
        .addIntegerOption(option => 
            option.setName('süre')
            .setDescription('Susturma süresi (dakika olarak)')
            .setRequired(true)),
    async execute(interaction) {
        const target = interaction.options.getUser('hedef');
        const süre = interaction.options.getInteger('süre');
        const executor = interaction.user.id;

        if (!interaction.member.permissions.has('MUTE_MEMBERS')) {
            return interaction.reply({
                content: '❌ Bu komutu kullanmak için yeterli yetkin yok.',
                ephemeral: true
            });
        }

        const member = interaction.guild.members.cache.get(target.id);

        if (!member) {
            return interaction.reply({
                content: `❌ Kullanıcı bu sunucuda bulunamadı.`,
                ephemeral: true
            });
        }

        await member.timeout(süre * 60 * 1000, 'Susturuldu');

        const embed = new MessageEmbed()
            .setColor('#ffcc00')
            .setTitle(`🔇 ${target.tag} Susturuldu`)
            .addField('Susturan', `<@${executor}>`, true)
            .addField('Süre', `${süre} dakika`, true)
            .setTimestamp();

        interaction.reply({ embeds: [embed] });
    }
};
