import discord
from discord.ext import commands
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
import threading
import asyncio

app = Flask(__name__)
socketio = SocketIO(app)

# Botu başlatmak için global değişkenler
bot = None
TOKEN = None
TARGET_SERVER_ID = None
TARGET_CHANNEL_ID = None
messages_cache = {} # Tüm mesajları biriktir

# Discord botu başlatan fonksiyon
def run_discord_bot(token):
    global bot
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print(f'Bot {bot.user} olarak giriş yaptı.')

        SERVERS_DATA = []
        for guild in bot.guilds:
            server_data = {
                'name': guild.name,
                'id': str(guild.id),
                'icon_url': guild.icon.url if guild.icon else None,
                'channels': [{'name': channel.name, 'id': (channel.id)} for channel in guild.text_channels]
            }
            SERVERS_DATA.append(server_data)
        
        # Socket ile bilgileri front-end'e gönder
        print(SERVERS_DATA)
        socketio.emit('servers_data', SERVERS_DATA)
        print("Sunucu ve kanal bilgileri frontend'e gönderildi.")


        for guild in bot.guilds:
            for channel in guild.text_channels:
                channel_key = f"{guild.id}_{channel.id}"  # Sunucu ve kanal ID'si birleşimi
                messages = []
                async for message in channel.history(limit=100):
                    message_data = {
                        'author': message.author.name,
                        'author_id': str(message.author.id),
                        'content': message.content
                    }
                    if message.attachments:
                        message_data['content'] = f'<img src="{message.attachments[0].url}" style="max-width: 200px;"/>'
                    messages.append(message_data)
                
                # Mesajları cache'de depola
                messages_cache[channel_key] = messages
                socketio.emit('response_data', messages_cache)  # JavaScript'e veri gönder
                print(messages_cache)

        guild = bot.get_guild(TARGET_SERVER_ID)
        if guild:
            print(f"Sunucu: {guild.name}")
            channel = bot.get_channel(TARGET_CHANNEL_ID)
            if channel:
                messages = []
                # Eski mesajları çek
                async for message in channel.history(limit=100):  # Son 100 mesajı asenkron olarak çek
                    message_data = {
                        'author': message.author.name,
                        'author_id': str(message.author.id),  # Kullanıcı ID'si eklendi
                        'content': message.content
                    }
                    # Mesaj içeriğinde bir medya varsa, onu ekle
                    if message.attachments:
                        message_data['content'] = f'<img src="{message.attachments[0].url}" style="max-width: 200px;"/>'  # İlk ekin URL'sini al ve boyutlandır

                    messages.append(message_data)  # Mesajı listeye ekle

                # Mesajları ters çevir ve gönder
                for message in reversed(messages):
                    print(f"Eski mesaj: {message['content']} | Gönderen: {message['author']}")
                    socketio.emit('new_message', message)  # Eski mesajları soket üzerinden gönder
            else:
                print("Kanal bulunamadı.")
        else:
            print("Sunucu bulunamadı.")

    @bot.event
    async def on_message(message):
        if message.guild.id == TARGET_SERVER_ID and message.channel.id == TARGET_CHANNEL_ID:
            message_data = {
                'author': message.author.name,
                'author_id': str(message.author.id),  # Kullanıcı ID'si eklendi
                'content': message.content
            }
            # Mesaj içeriğinde bir medya varsa, onu ekle
            if message.attachments:
                message_data['content'] = f'<img src="{message.attachments[0].url}" style="max-width: 200px;"/>'  # İlk ekin URL'sini al ve boyutlandır

            print(f"Yeni mesaj: {message.content} | Gönderen: {message.author}")
            socketio.emit('new_message', message_data)  # Yeni mesajları soket üzerinden gönder

        await bot.process_commands(message)

    @bot.command()
    async def send_message(ctx, *, content):
        channel = bot.get_channel(TARGET_CHANNEL_ID)
        await channel.send(content)

    bot.run(token)



@socketio.on('load_messages')
def load_messages(data):
    server_id = data['server_id']
    channel_id = data['channel_id']
    channel_key = f"{server_id}_{channel_id}"

    if channel_key in messages_cache:
        messages = messages_cache[channel_key]
        socketio.emit('messages_response', messages)
        print(f"{channel_key} için mesajlar gönderildi.")
    else:
        print(f"{channel_key} için mesaj bulunamadı.")

@socketio.on('load_messages_sync')
def load_messages_sync(data):
    server_id = data['server_id']
    channel_id = data['channel_id']

    # Dinamik anahtar oluştur
    channel_key = f"{server_id}_{channel_id}"
    
    # Mesajları cache'den al
    messages = messages_cache.get(channel_key, [])
    
    # Mesajları front-end'e gönder
    socketio.emit('load_messages_response', messages)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global TOKEN, TARGET_SERVER_ID, TARGET_CHANNEL_ID
        
        # Kullanıcıdan gelen form verilerini alıyoruz
        TOKEN = request.form['token']
        TARGET_SERVER_ID = int(request.form['server_id'])
        TARGET_CHANNEL_ID = int(request.form['channel_id'])

        # Discord botunu başka bir thread'de çalıştırıyoruz
        discord_thread = threading.Thread(target=run_discord_bot, args=(TOKEN,))
        discord_thread.start()

        return redirect(url_for('success'))
    return render_template('botcord.html')

@app.route('/send_message', methods=['POST'])
def send_message_route():
    content = request.json.get('content')  # POST isteğinden gelen içerik
    if content:
        channel = bot.get_channel(TARGET_CHANNEL_ID)
        asyncio.run_coroutine_threadsafe(channel.send(content), bot.loop)  # Mesajı kanala gönder
        return jsonify(success=True), 200
    return jsonify(success=False), 400

@app.route('/success')
def success():
    return render_template('botcord-main.html')

if __name__ == '__main__':
    socketio.run(app, port=2000, debug=True)
