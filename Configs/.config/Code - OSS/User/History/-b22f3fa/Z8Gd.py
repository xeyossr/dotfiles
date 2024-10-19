import discord
from discord.ext import commands
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import threading

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
        else:
            print("Sunucu bulunamadı.")

    @bot.event
    async def on_message(message):
        if message.guild.id == TARGET_SERVER_ID and message.channel.id == TARGET_CHANNEL_ID:
            print(f"Yeni mesaj: {message.content} | Gönderen: {message.author}")

        await bot.process_commands(message)

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

@app.route('/success')
def success():
    #return "Bot başarıyla başlatıldı ve bağlantı sağlandı!"
    return render_template('botcord-main.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)