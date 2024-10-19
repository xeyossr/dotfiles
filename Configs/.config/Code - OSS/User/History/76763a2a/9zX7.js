const { checkBanStatus, removeBan } = require('./database.js');
const { MessageEmbed } = require('discord.js');

setInterval(async () => {
    const users = await getAllBannedUsers(); // Tüm yasaklı kullanıcıları al

    users.forEach(async (user) => {
        const banEndDate = new Date(user.banDate);
        banEndDate.setDate(banEndDate.getDate() + user.duration); // Ban süresi

        if (new Date() >= banEndDate) {
            // Ban süresi dolmuşsa
            await removeBan(user.userId); // Banı kaldır

            // Kullanıcıya mesaj gönder
            const embed = new MessageEmbed()
                .setColor('#00ff00') // Yeşil renk
                .setTitle(`🎉 Banınız kaldırıldı`)
                .setDescription(`Merhaba! Ban süreniz doldu ve banınız kaldırıldı. Artık sunucuya katılabilirsiniz!`)
                .setTimestamp();

            const userToNotify = await client.users.fetch(user.userId); // Kullanıcıyı getir
            userToNotify.send({ embeds: [embed] });
        }
    });
}, 86400000); // 24 saat
