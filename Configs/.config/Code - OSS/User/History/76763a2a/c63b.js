const { checkBanStatus, removeBan } = require('./database.js');
const { MessageEmbed } = require('discord.js');

async function createInvite(guild) {
    try {
        const channel = guild.channels.cache.find(channel => channel.type === 'text'); // İlk metin kanalını al
        if (!channel) throw new Error("Metin kanalı bulunamadı.");

        // Daveti oluştur
        const invite = await channel.createInvite({
            maxAge: 0, // Süresiz
            maxUses: 1, // Sadece bir kez kullanılabilir
            unique: true // Benzersiz bir davet linki
        });

        return invite.url; // Davet linkini döndür
    } catch (error) {
        console.error('Davet oluşturulurken hata:', error);
        return null; // Hata durumunda null döndür
    }
}

setInterval(async () => {
    const users = await getAllBannedUsers(); // Tüm yasaklı kullanıcıları al

    users.forEach(async (user) => {
        const banEndDate = new Date(user.banDate);
        banEndDate.setDate(banEndDate.getDate() + user.duration); // Ban süresi

        if (new Date() >= banEndDate) {
            // Ban süresi dolmuşsa
            await removeBan(user.userId); // Banı kaldır

            // Kullanıcıya davet linki oluştur
            const guild = client.guilds.cache.get(user.guildId); // Kullanıcının bulunduğu sunucuyu al
            const inviteLink = await createInvite(guild); // Davet linkini oluştur

            // Kullanıcıya mesaj gönder
            const userToNotify = await client.users.fetch(user.userId); // Kullanıcıyı getir
            const embed = new MessageEmbed()
                .setColor('#00ff00') // Yeşil renk
                .setTitle(`🎉 Banınız kaldırıldı`)
                .setDescription(`Merhaba! Ban süreniz doldu ve banınız kaldırıldı. Artık sunucuya katılabilirsiniz!`)
                .addField('Davet Linki', inviteLink ? inviteLink : 'Davet linki oluşturulamadı.', false)
                .setTimestamp();

            userToNotify.send({ embeds: [embed] });
        }
    });
}, 86400000); // 24 saat
