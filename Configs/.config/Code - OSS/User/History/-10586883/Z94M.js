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