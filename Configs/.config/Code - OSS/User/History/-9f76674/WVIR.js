const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const config = require('../config.json'); // config dosyanızı buradan alın

module.exports = {
    data: new SlashCommandBuilder()
        .setName('kick')
        .setDescription('Bir kullanıcıyı sunucudan atar.')
        .addUserOption(option => 
            option.setName('hedef')
            .setDescription('Atmak istediğin kullanıcıyı seç')
            .setRequired(true))
        .addStringOption(option => 
            option.setName('sebep')
            .setDescription('Atma sebebini belirt')
            .setRequired(false)),
    async execute(interaction) {
        const target = interaction.options.getUser('hedef');
        const reason = interaction.options.getString('sebep') || 'Sebep belirtilmemiş';
        const executor = interaction.user.id;

        if (!interaction.member.permissions.has('KICK_MEMBERS') && executor !== config.sahipid) {
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

        else if (member == config.sahipid){
            return interaction.reply({
                content: `❌ Yüce Kamisaki-san sunucudan atılamaz.`,
                ephemeral: true
            })
        }

        await member.kick(reason);

        const embed = new MessageEmbed()
            .setColor('#ffcc00')
            .setTitle(`👢 ${target.tag} Sunucudan Atıldı`)
            .addField('Sebep', reason, true)
            .addField('Atan', `<@${executor}>`, true)
            .setTimestamp();

        interaction.reply({ embeds: [embed] });
    }
};
