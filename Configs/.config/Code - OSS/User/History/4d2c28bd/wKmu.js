const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('stats')
        .setDescription('Yazı ve ses sıralamasını gösterir.'),
    async execute(interaction) {
        // Veritabanından yazı sıralamasını al
        const db = require('../database.js');
        
        // Yazı sıralamasını al
        db.query(`SELECT user_id, total_points FROM user_points ORDER BY total_points DESC LIMIT 10`, async (err, messageResults) => {
            if (err) {
                console.error(err);
                return interaction.reply('Yazı sıralaması alınırken bir hata oluştu.');
            }

            // Ses sıralamasını al
            db.query(`SELECT user_id, total_voice_time FROM user_points ORDER BY total_voice_time DESC LIMIT 10`, async (err, voiceResults) => {
                if (err) {
                    console.error(err);
                    return interaction.reply('Ses sıralaması alınırken bir hata oluştu.');
                }

                // Yazı sıralamasını formatla
                const messageLeaderboard = messageResults.map((row, index) => {
                    return `${index + 1}. \`${row.user_id}\` - ${row.total_points} puan`;
                }).join('\n');

                // Ses sıralamasını formatla
                const voiceLeaderboard = voiceResults.map((row, index) => {
                    return `${index + 1}. \`${row.user_id}\` - ${row.total_voice_time} saniye`;
                }).join('\n');

                // Son mesajı oluştur
                const embedMessage = `
                    **📝 Yazı Sıralaması:**
                    ${messageLeaderboard}
                    
                    **🔊 Ses Sıralaması:**
                    ${voiceLeaderboard}
                `;

                await interaction.reply(embedMessage);
            });
        });
    }
};
