const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const config = require('../config.json'); // config dosyanızı buradan alın
const { getGuildById } = require('../database.js'); // Gerekli veritabanı fonksiyonunu buradan ekleyin

module.exports = {
    data: new SlashCommandBuilder()
        .setName('manage')
        .setDescription('Yönetim eylemlerini gerçekleştirir.')
        .addStringOption(option =>
            option.setName('eylem')
                .setDescription('Gerçekleştirilecek eylemi seçin.')
                .setRequired(true)
                .addChoices(
                    { name: 'Ban', value: 'ban' }
                ))
        .addUserOption(option =>
            option.setName('kullanıcı')
                .setDescription('Banlayacağınız kullanıcıyı seçin.')
                .setRequired(true))
        .addStringOption(option =>
            option.setName('açıklama')
                .setDescription('Ban açıklaması.')
                .setRequired(false)),
    async execute(interaction) {
        // Komutu sadece sahipid olan kullanıcı kullanabilir
        if (interaction.user.id !== config.sahipid) {
            return interaction.user.send('Bu komutu kullanma yetkiniz yok.');
        }

        const action = interaction.options.getString('eylem');
        const targetUser = interaction.options.getUser('kullanıcı');
        const description = interaction.options.getString('açıklama') || 'Sebep belirtilmemiş';
        const guildId = config.guildId;

        // Ban eylemi
        if (action === 'ban') {
            const guild = await interaction.client.guilds.fetch(guildId);
            const member = await guild.members.fetch(targetUser.id);

            try {
                await member.ban({ reason: description });

                const embed = new MessageEmbed()
                    .setColor('#ff0000') // Kırmızı renk
                    .setTitle(`🚫 ${targetUser.tag} Banlandı`)
                    .setDescription(`${targetUser.tag} adlı kullanıcı banlandı.`)
                    .addField('Açıklama', description)
                    .setTimestamp();

                // Kullanıcıya DM gönder
                await interaction.user.send({ embeds: [embed] });
            } catch (error) {
                console.error('Banlanırken hata oluştu:', error);
                await interaction.user.send('Kullanıcıyı banlarken bir hata oluştu. Lütfen yetkilerinizi kontrol edin.');
            }
        }
    }
};
