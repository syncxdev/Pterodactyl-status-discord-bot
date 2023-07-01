import discord
import psutil
import asyncio
import math
import platform
from discord.ext import commands
from datetime import datetime, timedelta

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

        disk_usage = psutil.disk_usage("/")
        total_disk = math.ceil(disk_usage.total / (1024**3))
        used_disk = math.ceil(disk_usage.used / (1024**3))
        free_disk = math.ceil(disk_usage.free / (1024**3))

        net_io = psutil.net_io_counters()
        network_inbound = math.ceil(net_io.bytes_recv / (1024**2))
        network_outbound = math.ceil(net_io.bytes_sent / (1024**2))

        server_ping = math.ceil(bot.latency * 1000)

        system_info = platform.uname()
        system_cores = psutil.cpu_count(logical=False)

     
        node_count = len(bot.guilds)

        server_count = len(bot.guilds)

       
        member_count = sum(guild.member_count for guild in bot.guilds)

        
        server_name = bot.get_guild(1054138859073589310).name

        uptime = datetime.utcnow() - bot.start_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_string = f"{days} Tage, {hours} Stunden, {minutes} Minuten, {seconds} Sekunden"

        embed = discord.Embed(title="Serverstatus", color=discord.Color.blue())
        embed.add_field(name=":desktop: CPU-Auslastung", value=f"{cpu_percent:.1f}%", inline=True)
        embed.add_field(name=":computer: RAM-Auslastung", value=f"{ram_percent:.1f}%", inline=True)
        embed.add_field(name=":bar_chart: Gesamter RAM", value=f"{total_ram} GB", inline=True)
        embed.add_field(name=":floppy_disk: Verwendeter RAM", value=f"{used_ram} GB", inline=True)
        embed.add_field(name=":cd: Gesamter Speicherplatz", value=f"{total_disk} GB", inline=True)
        embed.add_field(name=":cd: Verwendeter Speicherplatz", value=f"{used_disk} GB", inline=True)
        embed.add_field(name=":cd: Verbleibender Speicherplatz", value=f"{free_disk} GB", inline=True)
        embed.add_field(name=":arrow_down: Network (Inbound)", value=f"{network_inbound} MB", inline=True)
        embed.add_field(name=":arrow_up: Network (Outbound)", value=f"{network_outbound} MB", inline=True)
        embed.add_field(name=":ping_pong: Server-Ping", value=f"{server_ping} ms", inline=True)
        embed.add_field(name=":gear: Kerne", value=f"{system_cores}", inline=True)
        embed.add_field(name=":desktop: Betriebssystem", value=f"{system_info.system} {system_info.release}", inline=False)
        embed.add_field(name=":satellite: Nodes", value=f"{node_count}", inline=True)
        embed.add_field(name=":shield: Server", value=f"{server_count}", inline=True)
        embed.add_field(name=":busts_in_silhouette: Mitglieder", value=f"{member_count}", inline=True)
        embed.add_field(name=":blue_book: Server Name", value=f"{server_name}", inline=True)
        embed.add_field(name=":clock3: Uptime", value=f"{uptime_string}", inline=False)

        channel = bot.get_channel(1122541800658313336)  # YOUR_CHANNEL_ID

        server = bot.get_guild(1054138859073589310)  # YOUR_SERVER_ID

        if server.icon:
            embed.set_thumbnail(url=server.icon_url)
        else:
            embed.set_thumbnail(url="https://example.com/default_thumbnail.png")

        if status_message:
            await status_message.delete()

        status_message = await channel.send(embed=embed)

        # Füge Animation hinzu
        await status_message.edit(content="**Status wird überprüft...**")
        await asyncio.sleep(5)
        await status_message.edit(content="**Serverstatus**")
        await asyncio.sleep(5)

        await asyncio.sleep(50)  # Time for resend

@bot.event
async def on_ready():
    print(f'Bot ist eingeloggt als {bot.user.name}')
    print('-----')
    bot.start_time = datetime.utcnow()  # Speichere die Startzeit des Bots
    bot.loop.create_task(update_status())  

bot.run("Dein-Bot-Token")

