import discord
from discord.ext import commands
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import threading 

# Bot tokenini buraya ekle
TOKEN = 'MTI4OTI0ODU3MTMwODExMzk0MQ.GQ0md1.kQBkkdAqah-KhujmYu42utk_Y3AMcbMbsTPtOg'

# Botun prefix'ini belirle
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Belirli bir sunucu ve kanal ID'sini burada tanımla
TARGET_SERVER_ID = 1280331756947640360  # Sunucu ID'sini buraya ekle
TARGET_CHANNEL_ID = 1289252050747527258  # Kanal ID'sini buraya ekle

@bot.event
async def on_ready():
    print(f'Bot {bot.user} olarak giriş yaptı.')
    guild = bot.get_guild(TARGET_SERVER_ID)
    if guild:
        print(f"Sunucu: {guild.name}")
    else:
        print("Sunucu bulunamadı.")

# Yeni bir mesaj geldiğinde tetiklenir
@bot.event
async def on_message(message):
    # Belirtilen kanal dışındaki mesajları yok say
    if message.guild.id == TARGET_SERVER_ID and message.channel.id == TARGET_CHANNEL_ID:
        print(f"Yeni mesaj: {message.content} | Gönderen: {message.author}")

    # Mesajlar üzerinde işlem yapmadan önce botun kendi mesajlarını yok saymak önemlidir
    await bot.process_commands(message)

# Kanaldaki geçmiş mesajları çekme
@bot.command()
async def fetch_messages(ctx):
    if ctx.guild.id == TARGET_SERVER_ID and ctx.channel.id == TARGET_CHANNEL_ID:
        await ctx.send("Geçmiş mesajlar çekiliyor...")
        messages = await ctx.channel.history(limit=100).flatten()  # Son 100 mesajı çek
        for msg in messages:
            print(f"{msg.author}: {msg.content}")

# Botu çalıştır
bot.run(TOKEN)
