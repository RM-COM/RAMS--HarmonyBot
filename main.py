import discord
from discord.ext import commands
import re
import traceback
import yt_dlp

# Инициализация Discord бота с intents
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="rams.", intents=intents)

# Команда для проверки пинга
@client.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! Latency is {round(client.latency * 1000)}ms')

# Команда для воспроизведения музыки с YouTube
@client.command()
async def play(ctx, *, url: str):
    print("URL: ", url)  # Логирование URL
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    if not url_pattern.fullmatch(url):
        await ctx.send("❗ Неверный URL")
        return

    if ctx.author.voice is None:
        await ctx.send("❗ Ты не в голосовом канале!")
        return

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    try:
        ydl_opts = {'format': 'bestaudio/best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            audio_url = info_dict['formats'][0]['url']
            title = info_dict.get('title', 'Unknown')

        source = await discord.FFmpegOpusAudio.from_probe(audio_url, method='fallback')
        voice_channel.play(source)
        await ctx.send(f'🎶 Воспроизводится {title}')
    except Exception as e:
        print(traceback.format_exc())  # Вывод стектрейса
        await ctx.send(f"❗ Ошибка: {e}")
        await voice_channel.disconnect()

@client.command()
async def leave(ctx):
    if ctx.voice_client is None:
        await ctx.send("❗ Я не в голосовом канале!")
    else:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Я вышел из канала.")


@client.command()
async def pause(ctx):
    if ctx.voice_client is None:
        await ctx.send("❗ Я не в голосовом канале!")
    else:
        ctx.voice_client.pause()
        await ctx.send("⏸ Музыка на паузе.")


@client.command()
async def resume(ctx):
    if ctx.voice_client is None:
        await ctx.send("❗ Я не в голосовом канале!")
    else:
        ctx.voice_client.resume()
        await ctx.send("▶ Музыка продолжает играть.")


@client.command()
async def stop(ctx):
    if ctx.voice_client is None:
        await ctx.send("❗ Я не в голосовом канале!")
    else:
        ctx.voice_client.stop()
        await ctx.send("⏹ Музыка остановлена.")

# Запуск бота
client.run("")
