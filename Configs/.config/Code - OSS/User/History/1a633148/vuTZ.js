module.exports = {
    name: 'ready',
    once: true,
    execute(client) {
        console.log(`Bot giriş yaptı: ${client.user.tag}`);
    },
};
