import discord
from discord.ext import commands
import yt_dlp
import os

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='', intents=intents)

ytdl_format_options = {
    'format': 'bestaudio/aac',
    'quiet': True,
    'noplaylist': True,
    'nocheckcertificate': True,
}
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

@bot.event
async def on_ready():
    print(f'البوت {bot.user} جاهز للعمل!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # أوامر مباشرة (بدون تعجب)
    if message.content.startswith("ش "):
        query = message.content[2:]
        user = message.author
        if not user.voice:
            await message.channel.send("ادخل روم صوتي أولاً")
            return
        channel = user.voice.channel
        voice_client = await channel.connect() if message.guild.voice_client is None else message.guild.voice_client
        if voice_client.channel != channel:
            await voice_client.move_to(channel)
        
        await message.channel.send(f"جاري البحث عن {query}")
        data = ytdl.extract_info(f"ytsearch1:{query}", download=False)
        if 'entries' in data: data = data['entries'][0]
        
        audio = discord.FFmpegPCMAudio(
            executable="ffmpeg", source=data['url'], 
            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 10M -analyzeduration 0 -bufsize 20M"
        )
        voice_client.play(audio)
        await message.channel.send(f"تم التشغيل: {data['title']}")

    elif message.content == "ت":
        if message.guild.voice_client:
            await message.guild.voice_client.disconnect()
            await message.channel.send("تم الفكه منك والخروج.")
            
    elif message.content == "س":
        if message.guild.voice_client and message.guild.voice_client.is_playing():
            message.guild.voice_client.stop()
            await message.channel.send("لا تنفخ سكبت الأغنية.")

token = os.environ.get('TOKEN')
if token: bot.run(token)
