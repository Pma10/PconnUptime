import discord,time
from datetime import datetime, timedelta
from mcstatus.server import JavaServer
from discord.ext import commands, tasks
from discord.ext.commands import Cog


class Lookup(Cog):
    def __init__(self, app):
        self.app = app
        self.message_id = 1194152509783167037
        self.channel_id = 1194151956407664711
        self.pconn_address = 'pvpconnect.xyz'
        self.today_most_player = [0, 0]
        self.today_most_ping = [0, 0]
        self.check_server_status.start()

    def cog_unload(self):
        self.check_server_status.cancel()

    @tasks.loop(seconds=10)
    async def check_server_status(self):
        try:
            server = await JavaServer.async_lookup(self.pconn_address, 25565)
            status = server.status()
            nowTimestamp = int(time.mktime(time.localtime()))
            player, ping, max_players = status.players.online, int(status.latency), status.players.max

            if player > self.today_most_player[0]:
                self.today_most_player = [player, nowTimestamp]

            if ping > self.today_most_ping[0]:
                self.today_most_ping = [ping, nowTimestamp]

            channel = self.app.get_channel(self.channel_id)
            message = await channel.fetch_message(self.message_id) if self.message_id else None

            embed = discord.Embed(title='Pvpconnect Server Info', color=0xa2cfd6)
            embed.description = f'\n **{status.motd.parsed[14]}** \n \n **핑** \n > {ping}ms \n **최대 핑** \n > {self.today_most_ping[0]}ms <t:{self.today_most_ping[1]}:R> \n **버전** \n > {status.version.name}\n **접속자**\n > {player}/{max_players}명 \n **최고 동접** \n > {self.today_most_player[0]}/{max_players}명 <t:{self.today_most_player[1]}:R>'
            embed.timestamp = datetime.utcnow() + timedelta(hours=9)
            embed.set_thumbnail(url='https://cdn.discordapp.com/icons/1075028593421340733/94f2cee2abdf7cbb0e7d0330985de477.png?size=4096')

            if message:
                await message.edit(embed=embed)
            else:
                message = await channel.send(embed=embed)
                self.message_id = message.id

        except TimeoutError:
            channel = self.app.get_channel(self.channel_id)
            message = await channel.fetch_message(self.message_id) if self.message_id else None

            embed = discord.Embed(title='Pvpconnect Server Info', color=0xFF0000)
            embed.timestamp = datetime.utcnow()
            embed.description = '서버가 종료되었습니다.'

            if message:
                await message.edit(embed=embed)
            else:
                message = await channel.send(embed=embed)
                self.message_id = message.id
        except Exception as e:
            print(e)

def setup(app):
    print('[PconnMonitoring] LookUp Start')
    app.add_cog(Lookup(app))
