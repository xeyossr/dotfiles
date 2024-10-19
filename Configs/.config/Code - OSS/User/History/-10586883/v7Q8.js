const socket = io();

// Sayfa yüklendiğinde mesajları yükle
window.onload = function() {
    const savedMessages = JSON.parse(localStorage.getItem('messages')) || [];
    savedMessages.forEach(message_data => {
        addMessageToChat(message_data);
    });
};

// Yeni mesaj geldiğinde
socket.on('new_message', function(message_data) {
    addMessageToChat(message_data);
    saveMessageToLocalStorage(message_data);
});

function addMessageToChat(message_data) {
    const messageElement = document.createElement('div');
    messageElement.innerHTML = `<strong><a href="#" onclick="addMention('${message_data.author_id}')">${message_data.author}</a></strong>: ${message_data.content}`;
    
    // Ekli dosyaları göster
    /*if (message_data.attachments.length > 0) {
        message_data.attachments.forEach(url => {
            const imgElement = document.createElement('img');
            imgElement.src = url;
            imgElement.style.maxWidth = '250px';  // Resim boyutunu ayarla
            imgElement.style.display = 'block';  // Alt alta göstermek için
            messageElement.appendChild(imgElement);
        });
    }*/

    document.getElementById('messages').appendChild(messageElement);
    document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight; // Aşağı kaydır
}

function saveMessageToLocalStorage(message_data) {
    const savedMessages = JSON.parse(localStorage.getItem('messages')) || [];
    savedMessages.push(message_data);
    localStorage.setItem('messages', JSON.stringify(savedMessages));
}

// Kullanıcı ID'sini inputa eklemek için
function addMention(userId) {
    const messageInput = document.getElementById('message');
    messageInput.value += `<@${userId}> `;
    messageInput.focus();
}

// Mesaj gönderme
document.getElementById('send-button').addEventListener('click', function() {
    const messageContent = document.getElementById('message').value;
    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: messageContent })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Mesaj gönderildi!');
            document.getElementById('message').value = ''; // Mesaj kutusunu sıfırla
        } else {
            console.error('Mesaj gönderilemedi.');
        }
    })
    .catch((error) => {
        console.error('Hata:', error);
    });
});


// Server bilgilerini dinle ve logoları listele
socket.on('servers_data', function(servers) {
    console.log("Sunucu bilgileri alındı:", servers);
    const serverListElement = document.getElementById('server-list');
    servers.forEach(server => {
        const serverDiv = document.createElement('div');
        serverDiv.style.marginBottom = '10px';
        serverDiv.style.textAlign = 'center';
        
        if (server.icon_url) {
            const serverIcon = document.createElement('img');
            serverIcon.src = server.icon_url;
            serverIcon.style.width = '50px';
            serverIcon.style.height = '50px';
            serverIcon.style.cursor = 'pointer';
            
            serverIcon.addEventListener('click', function() {
                showChannels(server);  // Kanalları göster fonksiyonunu çağır
            });
            
            serverDiv.appendChild(serverIcon);
        } else {
            serverDiv.textContent = server.name;
        }
        
        serverListElement.appendChild(serverDiv);
    });
});


// Kanalları gösteren fonksiyon
function showChannels(server) {
    // Üç noktalı menü oluşturma
    let menuButton = document.getElementById('menu-button');
    if (!menuButton) {
        menuButton = document.createElement('button');
        menuButton.id = 'menu-button';
        menuButton.textContent = '⋮';
        menuButton.style.position = 'fixed';
        menuButton.style.top = '20px';
        menuButton.style.right = '20px';
        menuButton.style.background = '#7289DA';
        menuButton.style.color = 'white';
        menuButton.style.border = 'none';
        menuButton.style.borderRadius = '5px';
        menuButton.style.padding = '10px';
        menuButton.style.cursor = 'pointer';
        document.body.appendChild(menuButton);
    }

    // Butona tıklandığında kanalların listesini göster
    menuButton.addEventListener('click', function() {
        let channelMenu = document.getElementById('channel-menu');
        if (!channelMenu) {
            channelMenu = document.createElement('div');
            channelMenu.id = 'channel-menu';
            channelMenu.style.position = 'fixed';
            channelMenu.style.top = '60px';
            channelMenu.style.right = '20px';
            channelMenu.style.background = '#2F3136';
            channelMenu.style.border = '1px solid #40444B';
            channelMenu.style.borderRadius = '5px';
            channelMenu.style.padding = '10px';
            channelMenu.style.zIndex = '999';  // Menüyü üste getiriyoruz
            document.body.appendChild(channelMenu);
        }

        // Kanal listesi temizleniyor
        channelMenu.innerHTML = '';
        server.channels.forEach(channel => {
            const channelDiv = document.createElement('div');
            channelDiv.textContent = channel.name;
            channelDiv.style.color = 'white';
            channelDiv.style.cursor = 'pointer';
            channelDiv.style.marginBottom = '5px';
            channelDiv.addEventListener('click', function() {
                console.log(server.id, channel.id);
                selectServerChannel(server.id, channel.id);  // Kanal seçildiğinde fonksiyonu çağır
            });
            channelMenu.appendChild(channelDiv);
        });
    });
}

let TARGET_SERVER_ID = null;
let TARGET_CHANNEL_ID = null;

// Kullanıcı sunucu veya kanal seçtiğinde bu fonksiyon tetiklenir
function selectServerChannel(serverId, channelId) {
    TARGET_SERVER_ID = serverId;
    TARGET_CHANNEL_ID = channelId;

    // Python tarafına yeni sunucu ve kanal ID'lerini gönder
    socket.emit('load_messages', {
        'server_id': TARGET_SERVER_ID,
        'channel_id': TARGET_CHANNEL_ID
    });
    console.log("load_messages event emitted");
    // Önce mesaj kutusunu temizle
    document.getElementById('messages').innerHTML = '';
}

// Mesajları biriktirin
let messagesToDisplay = [];

// Mesajları yüklemek için buraya gelen socket olayını dinleyin
socket.on('load_messages_response', function(messages) {
    messages.forEach(function(message_data) {
        messagesToDisplay.push(message_data);
    });

    // Tüm mesajları bir defada ekle
    messagesToDisplay.forEach(function(message_data) {
        addMessageToChat(message_data);
    });
});

function addMessageToChat(message_data) {
    const messageElement = document.createElement('div');
    messageElement.innerHTML = `<strong><a href="#" onclick="addMention('${message_data.author_id}')">${message_data.author}</a></strong>: ${message_data.content}`;
    document.getElementById('messages').appendChild(messageElement);
    document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight; // Aşağı kaydır
}
