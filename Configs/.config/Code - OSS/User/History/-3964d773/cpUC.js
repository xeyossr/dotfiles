const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('ban')
        .setDescription('Bir kullanıcıyı banlar.')
        .addUserOption(option => 
            option.setName('hedef')
            .setDescription('Banlamak istediğin kullanıcıyı seç')
            .setRequired(true))
        .addStringOption(option => 
            option.setName('sebep')
            .setDescription('Ban sebebini belirt')
            .setRequired(false)),
    async execute(interaction) {
        const target = interaction.options.getUser('hedef');
        const reason = interaction.options.getString('sebep') || 'Sebep belirtilmemiş';
        const executor = interaction.user.id;

        if (!interaction.member.permissions.has('BAN_MEMBERS')) {
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

        await member.ban({ reason });

        const embed = new MessageEmbed()
            .setColor('#ff0000')
            .setTitle(`🚫 ${target.tag} Banlandı`)
            .addField('Sebep', reason, true)
            .addField('Banlayan', `<@${executor}>`, true)
            .setTimestamp();

        interaction.reply({ embeds: [embed] });
    }
};
