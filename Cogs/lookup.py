import discord
from Command.Mongo import MongoDB
from datetime import datetime , timedelta
from mcstatus import JavaServer
from discord.ext import commands, tasks
from discord.ext.commands import Cog

class Lookup(Cog):
    def __init__(self, app):
        self.app = app
        self.messageId = 1192609974728282212
        self.pconnAddress = 'pvpconnect.xyz'
        self.todayMostPlayer = [0, datetime.now()]
        self.todayMostPing = [0, datetime.now()]
        self.checkServerStatus.start()

    def cog_unload(self):
        self.checkServerStatus.cancel()

    @tasks.loop(seconds=10)
    async def checkServerStatus(self):
        try:
            server = await JavaServer.async_lookup(self.pconnAddress, 25565)
            status = server.status()
            player = status.players.online
            ping = int(status.latency)
            
            if player > self.todayMostPlayer[0]:
                self.todayMostPlayer = [player, datetime.now()]
            
            if ping > self.todayMostPing[0]:
                self.todayMostPing = [ping, datetime.now()]

            if datetime.now().date() != self.todayMostPlayer[1].date():
                MongoDB.insertTodayMostUsers(datetime.now().date() - timedelta(days=1), self.todayMostPlayer)
                MongoDB.insertTodayMostPing(datetime.now().date() - timedelta(days=1),self.todayMostPing)
                self.todayMostPlayer = [player, datetime.now()]
                self.todayMostPing = [ping, datetime.now()]
            
            channel = self.app.get_channel(1192493690699129026)
            message = await channel.fetch_message(self.messageId) if self.messageId else None

            embed = discord.Embed(title='Pvpconnect Server Info', color=0xa2cfd6)
            embed.description = f'\n **{status.motd.parsed[14]}** \n \n **핑** \n > {ping}ms \n **최대 핑** \n > {self.todayMostPing[0]} \n **버전** \n > {status.version.name}\n **접속자**\n > {player}/{status.players.max}명 \n **최고 동접** \n > {self.todayMostPlayer[0]}/{status.players.max}명'
            embed.timestamp = datetime.utcnow()
            embed.set_thumbnail(url='https://cdn.discordapp.com/icons/1075028593421340733/94f2cee2abdf7cbb0e7d0330985de477.png?size=4096')

            if message:
                await message.edit(embed=embed)
            else:
                message = await channel.send(embed=embed)
                self.messageId = message.id

        except TimeoutError:
            channel = self.app.get_channel(1192493690699129026)
            message = await channel.fetch_message(self.messageId) if self.messageId else None

            embed = discord.Embed(title='Pvpconnect Server Info', color=0xFF0000)
            embed.timestamp = datetime.utcnow()
            embed.description = '서버가 종료되었습니다.'

            if message:
                await message.edit(embed=embed)
            else:
                message = await channel.send(embed=embed)
                self.messageId = message.id
        except Exception as e:
            print(e)

def setup(app):
    print('[PconnMonitoring] LookUp Start')
    app.add_cog(Lookup(app))
