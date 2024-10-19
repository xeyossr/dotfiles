import discord
from discord.ext import commands
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
socketio = SocketIO(app)

bot = None
TOKEN = None
TARGET_SERVER_ID = None
TARGET_CHANNEL_ID = None
messages = []

# Discord botu başlatan fonksiyon
def run_discord_bot(token):
    global bot
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print(f'Bot {bot.user} olarak giriş yaptı.')

    @bot.event
    async def on_message(message):
        if message.guild.id == TARGET_SERVER_ID and message.channel.id == TARGET_CHANNEL_ID:
            message_data = {
                'content': message.content,
                'author': {
                    'name': message.author.name,
                    'avatar': str(message.author.avatar_url),
                    'roles': [role.name for role in message.author.roles if role.name != "@everyone"],
                }
            }
            messages.append(message_data)
            socketio.emit('new_message', message_data)  # Yeni mesajları soket üzerinden gönder
        await bot.process_commands(message)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global TOKEN, TARGET_SERVER_ID, TARGET_CHANNEL_ID
        
        TOKEN = request.form['token']
        TARGET_SERVER_ID = int(request.form['server_id'])
        TARGET_CHANNEL_ID = int(request.form['channel_id'])

        discord_thread = threading.Thread(target=run_discord_bot, args=(TOKEN,))
        discord_thread.start()

        return redirect(url_for('success'))
    return render_template('botcord.html')

@app.route('/success')
def success():
    #return redirect(url_for('main'))
    return "SAAAA!"
    
#@app.route('/main')
#def main():
#    return render_template('botcord-main.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
