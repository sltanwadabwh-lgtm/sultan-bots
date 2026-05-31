import discord
from discord.ext import commands
import yt_dlp

# إعدادات البوت
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='', intents=intents)

# إعدادات يوتيوب مع تحسينات لمنع التقطيع
ytdl_format_options = {
    'format': 'bestaudio/best',
    'quiet': True,
    'noplaylist': True,
}
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

@bot.event
async def on_ready():
    print(f'البوت {bot.user} جاهز للعمل!')

# أمر التشغيل (ش)
@bot.command(name="ش")
async def play_msg(ctx, *, query: str):
    user = ctx.author
    if not user.voice:
        await ctx.send("ادخل روم صوتي أولاً")
        return

    channel = user.voice.channel
    if ctx.voice_client is None:
        voice_client = await channel.connect()
    else:
        voice_client = ctx.voice_client
        if voice_client.channel != channel:
            await voice_client.move_to(channel)

    await ctx.send(f"جاري البحث عن {query}")

    search_query = f"ytsearch1:{query}"
    data = ytdl.extract_info(search_query, download=False)
    
    if 'entries' in data:
        data = data['entries'][0]
    
    url = data['url']
    
    # تحسينات FFmpeg لمنع التقطيع
    audio = discord.FFmpegPCMAudio(
        executable="ffmpeg.exe", 
        source=url, 
        before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 10M -analyzeduration 0"
    )
    voice_client.play(audio)
    await ctx.send(f"تم  : {data['title']}")

# أمر التوقف والخروج (ت)
@bot.command(name="ت")
async def stop_and_leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("تم الفكه منك والخروج.")
    else:
        await ctx.send("أنا مو في روم أصلاً.")

# أمر السكب (س)
@bot.command(name="س")
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("لا تنفخ سكبت الأغنية.")
    else:
        await ctx.send("ياحمار ما فيه شيء شغال عشان أسكبه.")

# 
import os
# 
bot.run(os.environ['TOKEN'])