const { SlashCommandBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('sil')
        .setDescription('Belirtilen sayıda mesajı siler. Opsiyonel olarak bir kullanıcıyı etiketleyebilirsin.')
        .addIntegerOption(option => 
            option.setName('sayısı')
                .setDescription('Silinecek mesaj sayısı')
                .setRequired(true))
        .addUserOption(option => 
            option.setName('kullanıcı')
                .setDescription('Mesajları silinecek kullanıcı')
                .setRequired(false)),
    async execute(interaction) {
        // Kullanıcının mesaj silme yetkisini kontrol et
        if (!interaction.member.permissions.has('MANAGE_MESSAGES')) {
            return interaction.reply('Bu komutu kullanabilmek için "Mesajları Yönet" iznine sahip olmalısın!', { ephemeral: true });
        }

        const sayi = interaction.options.getInteger('sayısı');
        const kullanici = interaction.options.getUser('kullanıcı');

        // Mesajları almak için kanalın en son mesajlarını çek
        const messages = await interaction.channel.messages.fetch({ limit: sayi + 1 }); // 1 ekliyoruz çünkü bot mesajı da dahil

        let silinecekMesajlar = messages;

        // Eğer kullanıcı belirtilmişse, sadece o kullanıcının mesajlarını seç
        if (kullanici) {
            silinecekMesajlar = messages.filter(msg => msg.author.id === kullanici.id);
        }

        // Mesajları sil
        try {
            await interaction.channel.bulkDelete(silinecekMesajlar, true); // İkinci parametreyi true yaparak silinemeyen mesajları atlayabiliriz
            await interaction.reply(`Başarıyla **${silinecekMesajlar.size}** mesaj silindi.`);
        } catch (error) {
            console.error('Mesaj silinirken hata oluştu:', error);
            await interaction.reply('Mesajlar silinirken bir hata oluştu. Lütfen tekrar deneyin.');
        }
    },
};
