import discord
from .utils.dataIO_import_dataIO
from__main__import_settings

class red-mtg:
    def  __init__(self, bot):
        self.bot = bot
        # load any local files here if desired
        self.owner = '<![]>'.format(settings.owner)

    async def listener(self, message):
        # listener code here
        channel = message.channel
        author = message.author.id

        if author == '127883009889140736' and channel == '224417319189872650':
            if "hello" in message.content:
                await self.bot.say('Hello There')

def setup(bot):
    n = red-mtg(bot)
    bot.add_listener(n.listener, "on_message")
    bot.add_cog(n)