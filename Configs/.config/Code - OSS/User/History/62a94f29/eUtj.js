const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('invite')
        .setDescription('Davet ettiğin kullanıcıların bilgilerini gösterir.'),
    async execute(interaction) {
        const guild = interaction.guild;

        // Sunucudaki davetleri al
        const invites = await guild.invites.fetch();

        // Kullanıcının davet bilgilerini tutacak bir nesne
        const userInvites = {};
        const userLeaves = {};

        // Davet bilgilerini kullanıcıya göre ayır
        invites.forEach(invite => {
            const inviterId = invite.inviter.id;

            // Kullanıcının davet ettiği kişi sayısını güncelle
            if (!userInvites[inviterId]) {
                userInvites[inviterId] = { count: 0, invitedUsers: [] };
            }

            userInvites[inviterId].count += invite.uses;
            userInvites[inviterId].invitedUsers.push({
                code: invite.code,
                uses: invite.uses,
                maxUses: invite.maxUses,
                inviter: invite.inviter.tag,
                createdAt: invite.createdAt
            });

            // Kullanıcının davet ettiği kişilerden ayrılanları kontrol et
            invite.uses > 0 ? userLeaves[inviterId] = (userLeaves[inviterId] || 0) + invite.uses : null;
        });

        // Embed mesajını oluştur
        const embed = new MessageEmbed()
            .setColor('#0099ff')
            .setTitle(`📈 Davet Bilgileri`)
            .setDescription(`Sunucuda davet ettiğin kullanıcıların bilgileri:`)
            .setTimestamp();

        // Her kullanıcının davet bilgilerini ekle
        for (const [userId, inviteData] of Object.entries(userInvites)) {
            const user = await guild.members.fetch(userId);
            embed.addField(
                `${user.user.tag}`,
                `**Davet Sayısı:** ${inviteData.count}\n` +
                `**Davet Edilen Kullanıcılar:** ${inviteData.invitedUsers.map(u => `${u.inviter} (Kod: ${u.code}, Kullanım: ${u.uses}, Maksimum Kullanım: ${u.maxUses})`).join('\n')}`,
                false
            );
        }

        // Ayrılan kullanıcıları ekle
        embed.addField('Ayrılan Kullanıcılar', Object.keys(userLeaves).length > 0 ? Object.entries(userLeaves).map(([key, value]) => `<@${key}> - Ayrılan: ${value}`).join('\n') : 'Hiç kimse ayrılmadı.');

        interaction.reply({ embeds: [embed] });
    }
};
