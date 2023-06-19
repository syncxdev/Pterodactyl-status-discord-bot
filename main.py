import discord
import psutil
import asyncio
import math
import platform
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
status_message = None

async def update_status():
    global status_message
    await bot.wait_until_ready()
    while not bot.is_closed():
        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent
        total_ram = math.ceil(psutil.virtual_memory().total / (1024**3))
        used_ram = psutil.virtual_memory().used / (1024**3)
        used_ram = math.ceil(used_ram)

        net_io = psutil.net_io_counters()
        network_inbound = math.ceil(net_io.bytes_recv / (1024**2))
        network_outbound = math.ceil(net_io.bytes_sent / (1024**2))

        server_ping = math.ceil(bot.latency * 1000)

        system_info = platform.uname()
        system_cores = psutil.cpu_count(logical=False)

        embed = discord.Embed(title="Serverstatus", color=discord.Color.blue())
        embed.add_field(name="CPU-Auslastung", value=f"{cpu_percent}%", inline=True)
        embed.add_field(name="RAM-Auslastung", value=f"{ram_percent}%", inline=True)
        embed.add_field(name="Gesamter RAM", value=f"{total_ram} GB", inline=True)
        embed.add_field(name="Verwendeter RAM", value=f"{used_ram} GB", inline=True)
        embed.add_field(name="Network (Inbound)", value=f"{network_inbound} MB", inline=True)
        embed.add_field(name="Network (Outbound)", value=f"{network_outbound} MB", inline=True)
        embed.add_field(name="Server-Ping", value=f"{server_ping} ms", inline=True)
        embed.add_field(name="Kerne", value=f"{system_cores}", inline=True)
        embed.add_field(name="Betriebssystem", value=f"{system_info.system} {system_info.release}", inline=False)

        channel = bot.get_channel(1119938696133742693)  # YOUR_CHANNEL_ID

        server = bot.get_guild(1054138859073589310)  # YOUR_SERVER_ID

        if server.icon:
            embed.set_thumbnail(url=server.icon_url)
        else:
            embed.set_thumbnail(url="https://example.com/default_thumbnail.png")

        if status_message:
            await status_message.delete()

        status_message = await channel.send(embed=embed)

        await asyncio.sleep(60)  # Time for resend

@bot.event
async def on_ready():
    print(f'Bot ist eingeloggt als {bot.user.name}')
    print('-----')
    bot.loop.create_task(update_status())  # Starte Serverstatus


bot.run("Your-Bot-Token")
