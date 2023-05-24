import discord
import psutil
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
status_message = None

async def update_status():
    global status_message
    await bot.wait_until_ready()
    while not bot.is_closed():
        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent
        total_ram = psutil.virtual_memory().total / (1024**3)
        used_ram = psutil.virtual_memory().used / (1024**3)

       
        net_io = psutil.net_io_counters()
        network_inbound = net_io.bytes_recv / (1024**2)
        network_outbound = net_io.bytes_sent / (1024**2)  

       
        server_ping = bot.latency * 1000 

        embed = discord.Embed(title="Serverstatus", color=discord.Color.blue())
        embed.add_field(name="CPU-Auslastung", value=f"{cpu_percent}%", inline=False)
        embed.add_field(name="RAM-Auslastung", value=f"{ram_percent}%", inline=False)
        embed.add_field(name="Gesamter RAM", value=f"{total_ram} GB", inline=False)
        embed.add_field(name="Verwendeter RAM", value=f"{used_ram} GB", inline=False)
        embed.add_field(name="Network (Inbound)", value=f"{network_inbound} MB", inline=False)
        embed.add_field(name="Network (Outbound)", value=f"{network_outbound} MB", inline=False)
        embed.add_field(name="Server-Ping", value=f"{server_ping} ms", inline=False)

        channel = bot.get_channel(1104357841625677824)  # YOUR_CHANNEL_ID

        if status_message:
            await status_message.delete() 

        status_message = await channel.send(embed=embed)  

        await asyncio.sleep(5)  #  Time for resend

@bot.event
async def on_ready():
    print(f'Bot ist eingeloggt als {bot.user.name}')
    print('-----')
    bot.loop.create_task(update_status())  # Starte Serverstatus


bot.run("")
