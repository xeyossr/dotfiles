const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('unban')
        .setDescription('Bir kullanıcının banını kaldırır.')
        .addStringOption(option => 
            option.setName('kullanıcı_id')
            .setDescription('Banını kaldırmak istediğin kullanıcının ID\'sini gir')
            .setRequired(true)),
    async execute(interaction) {
        const userId = interaction.options.getString('kullanıcı_id');
        const executor = interaction.user.id;

        if (!interaction.member.permissions.has('BAN_MEMBERS')) {
            return interaction.reply({
                content: '❌ Bu komutu kullanmak için yeterli yetkin yok.',
                ephemeral: true
            });
        }

        try {
            await interaction.guild.bans.remove(userId);

            interaction.reply({
                content: `🔓 Kullanıcının banı kaldırıldı: <@${userId}>`,
                ephemeral: true
            });
        } catch (error) {
            interaction.reply({
                content: `❌ Ban kaldırma işlemi başarısız oldu: ${error.message}`,
                ephemeral: true
            });
        }
    }
};
