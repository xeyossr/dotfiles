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

# Discord botu başlatan fonksiyon
def run_discord_bot(token):
    global bot
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print(f'Bot {bot.user} olarak giriş yaptı.')
        guild = bot.get_guild(TARGET_SERVER_ID)
        if guild:
            print(f"Sunucu: {guild.name}")
            channel = bot.get_channel(TARGET_CHANNEL_ID)
            if channel:
                messages = []
                # Eski mesajları çek
                async for message in channel.history(limit=1000):  # Son 1000 mesajı asenkron olarak çek
                    message_data = {
                        'author': message.author.name,
                        'author_id': str(message.author.id),  # Kullanıcı ID'si eklendi
                        'content': message.content,
                        'attachments': [attachment.url for attachment in message.attachments]  # Ekleri ekle
                    }
                    # Mesaj içeriğinde bir medya varsa, onu ekle
                    if message.attachments:
                        message_data['content'] = f'<img src="{message.attachments[0].url}" style="max-width: 200px;"/>'  # İlk ekin URL'sini al ve boyutlandır

                    #messages.append(message_data)  # Mesajı listeye ekle

                # Mesajları ters çevir ve gönder
                for message in reversed(messages):
                    print(f"Eski mesaj: {message['content']} | Gönderen: {message['author']} | ID: {message['author_id']}")
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
                'content': message.content,
                'attachments': [attachment.url for attachment in message.attachments]  # Ekleri ekle
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
    socketio.run(app, debug=True)
