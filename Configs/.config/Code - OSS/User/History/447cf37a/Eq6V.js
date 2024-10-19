const { SlashCommandBuilder } = require('@discordjs/builders');
const fetch = require('node-fetch');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('tarihte-bugun')
        .setDescription('Bugün tarihte ne olduğunu gösterir.'),
    async execute(interaction) {
        const today = new Date();
        const month = today.getMonth() + 1; // 0-11 arası olduğu için 1 ekliyoruz
        const day = today.getDate();

        // Wikipedia API URL'si
        const apiUrl = `https://en.wikipedia.org/api/rest_v1/page/summary/${month}-${day}`;

        try {
            const response = await fetch(apiUrl);
            const data = await response.json();

            // Eğer hata varsa
            if (data.error || !data.content_urls || !data.content_urls.desktop) {
                return interaction.reply('Bugün tarihte önemli bir olay bulunamadı.');
            }

            // Embed mesajını oluştur
            const embed = {
                color: 0x0099ff,
                title: `Tarihte Bugün: ${today.toLocaleDateString()}`,
                description: data.extract,
                fields: [
                    {
                        name: 'Daha Fazla Bilgi',
                        value: `[Wikipedia'da oku](${data.content_urls.desktop.page})`,
                    },
                ],
                footer: {
                    text: 'Kaynak: Wikipedia',
                },
            };

            await interaction.reply({ embeds: [embed] });
        } catch (error) {
            console.error('Veri çekme hatası:', error);
            await interaction.reply('Tarihte bugüne ait veriler çekilirken bir hata oluştu.');
        }
    },
};
