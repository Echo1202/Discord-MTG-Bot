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
            key, name = self.message_find(message)
            url = "https://api.scryfall.com/cards/named?fuzzy="
            url += name
            my_header = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
            card_data = requests.get(url, headers=my_header, allow_redirects=True).json()
            print(url)
            embed_obj = self.key_display(key, card_data)
            try:
                await self.bot.send_message(message.channel, embed=embed_obj)
            except discord.Forbidden:
                return

    def message_find(self, message):
        msg_lower = message.content.lower()
        if self.string_find(msg_lower, "[[") and self.string_find(msg_lower, "]]"):
            name = msg_lower[msg_lower.find("[[") + 2:msg_lower.find("]]")]
            if self.string_find(name, "$"):
                name = name[name.find("$")+1:]
                return "$", name
            elif self.string_find(name, "!"):
                name = name[name.find("!")+1:]
                return "!", name
            elif self.string_find(name, "?"):
                name = name[name.find("?")+1:]
                return "?", name
            else:
                return "0", name

    def key_display(self,key,card_data):
        if key == "$":
            link = "https://scryfall.com/card/{}/{}".format(card_data["set"], card_data["collector_number"])
            embed_obj = discord.Embed(title="Price of "+card_data["name"], url=link, description=card_data["set"]+" $" + card_data["prices"]["usd"])
            return embed_obj
        elif key == "!":
            link = "https://scryfall.com/card/{}/{}".format(card_data["set"], card_data["collector_number"])
            embed_obj = discord.Embed(title=card_data["name"], url=link)
            embed_obj.set_image(url=card_data["image_uris"]["normal"])
            return embed_obj
        elif key == "?":
            ruling_link = card_data["rulings_uri"]
            embed_obj = discord.Embed(title="Ruling for "+card_data["name"], url=ruling_link)
            for line in card_data:
                embed_obj.add_field(name=card_data["published_at"], value=card_data["comment"], inline=False)
            return embed_obj
        elif key == "0":
            link = "https://scryfall.com/card/{}/{}".format(card_data["set"], card_data["collector_number"])
            print(key)
            embed_obj = discord.Embed(title=card_data["name"], url=link, description=card_data["oracle_text"])
            embed_obj.add_field(name="type_line")
            embed_obj.set_thumbnail(url=card_data["image_uris"]["png"])
            return embed_obj
        else:
            print("key display nothing")
            return

    def string_find(self, content, word):
        i = content.find(word)
        if i == -1:
            return False
        return True

def setup(bot):
    n = RedMtg(bot)
    bot.add_listener(n.listener, "on_message")
    bot.add_cog(n)