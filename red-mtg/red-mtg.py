import discord
from .utils.dataIO import dataIO
from __main__ import settings
import requests

class RedMtg:
    def  __init__(self, bot):
        self.bot = bot
        self.owner = '<![]>'.format(settings.owner)

    async def listener(self, message):
        channel = message.channel.id

        # restrict usage within a specific channel
        if channel == '372159261108600833':
            #check message for [[ ]]
            msg_lower = message.content.lower()
            if self.string_find(msg_lower, "[[") and self.string_find(msg_lower, "]]"):
                #parse the message
                name = msg_lower[msg_lower.find("[[")+2:msg_lower.find("]]")] #will find the name by +2("cutting out") the
                                                                              #open brackets
                url = 'https://api.scryfall.com/cards/named?fuzzy='
                url += name
                my_header = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
                # using the name get the json for the page (json is now a dict(?))
                card_data = requests.get(url, headers=my_header, allow_redirects=True).json() #allow_redirects allow us
                                                                                              #to go all the way to the content
                try: # throws exceptions
                    link = "https://scryfall.com/card/{}/{}".format(card_data["set"], card_data["collector_number"])
                    embed_obj = discord.Embed(title=card_data["name"], url=link, description=card_data["oracle_text"])
                    # embed_obj = discord.Embed(title="", url=card["scryfall_uri"])
                    embed_obj.set_thumbnail(url=card_data["image_uris"]["png"])
                    await self.bot.send_message(message.channel, embed=embed_obj)
                    # await self.bot.send_message(message.channel, "Card: {} - Collector Number: {} - Set: {} - URL: {}".format(card["name"], card["collector_number"], card["set"], link))
                except discord.Forbidden:
                    return

    def string_find(self, content, word):
        i = content.find(word)
        if i == -1:
            return False
        return True

def setup(bot):
    n = red-mtg(bot)
    bot.add_listener(n.listener, "on_message")
    bot.add_cog(n)