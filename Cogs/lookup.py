import discord
from Command.Mongo import MongoDB
from datetime import datetime, timedelta
from mcstatus import JavaServer
from discord.ext import commands, tasks
from discord.ext.commands import Cog

class Lookup(Cog):
    def __init__(self, app):
        self.app = app
        self.messageId = 1192609974728282212
        self.pconnAddress = 'pvpconnect.xyz'
        self.todayMost = [0, datetime.now()]
        self.checkServerStatus.start()

    def cog_unload(self):
        self.checkServerStatus.cancel()

    @tasks.loop(seconds=10)
    async def checkServerStatus(self):
        try:
            server = await JavaServer.async_lookup('pvpconnect.xyz', 25565)
            status = server.status()            
            player = status.players.online
            if player > self.todayMost[0]:
                self.todayMost[0] = player
                self.todayMost[1] = datetime.now()
            if datetime.now().date() != self.todayMost[1].date():
                await MongoDB.insertTodayMostUsers(datetime.now().date(),self.todayMost[0])
                self.todayMost[0] = player
                self.todayMost[1] = datetime.now()
            channel = self.app.get_channel(1192493690699129026)
            if self.messageId is None:
                embed = discord.Embed(title='Pvpconnect Server Info',color=0xa2cfd6)
                embed.description = f'\n **{status.motd.parsed[14]}** \n \n **핑** \n > {round(status.latency)}ms \n **버전** \n > {status.version.name}\n **접속자**\n > {player}/{status.players.max}명 \n **최고 동접** \n > {self.todayMost[0]}/{status.players.max}명'
                embed.timestamp = datetime.utcnow()
                embed.set_thumbnail(url='https://cdn.discordapp.com/icons/1075028593421340733/94f2cee2abdf7cbb0e7d0330985de477.png?size=4096')
                message = await channel.send(embed=embed)   
                self.messageId = message.id
            else:
                message = await channel.fetch_message(self.messageId)
                embed = message.embeds[0]
                embed.timestamp = datetime.utcnow()
                embed.description = f'\n **{status.motd.parsed[14]}** \n \n **핑** \n > {round(status.latency)}ms \n **버전** \n > {status.version.name}\n **접속자**\n > {player}/{status.players.max}명 \n **최고 동접** \n > {self.todayMost[0]}/{status.players.max}명'
                await message.edit(embed=embed)
        except Exception as e:
            if e == TimeoutError:
                message = await channel.fetch_message(self.messageId)
                embed = message.embeds[0]
                embed.timestamp = datetime.utcnow()
                embed.description = f'서버가 종료되었습니다.'
                embed.color = 0xFF0000
                await message.edit(embed=embed)
            else:
                print(e)

def setup(app):
    print('[PconnMonitoring] LookUp Start')
    app.add_cog(Lookup(app))
