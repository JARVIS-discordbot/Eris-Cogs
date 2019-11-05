import discord
from redbot.core import commands, checks
import random
import re

BaseCog = getattr(commands, "Cog", object)

halloween_prefixes = list(
    {
        "afraid", "apparition", "bat", "bloodcurdling", "bloody", "bones", "broomstick", "cackle", "cadaver", "carved",
        "casket", "cauldron", "cemetery", "cobweb", "coffin", "corpse", "creepy", "decapitated", "decomposing", "eerie",
        "fangs", "frightening", "ghost", "ghoulish", "goblin", "gory", "grim reaper", "gruesome", "haunted",
        "horrifying", "howling", "jack - o - lantern", "lurking", "macabre", "magic", "mausoleum", "morbid", "mummy",
        "occult", "owl", "petrified", "phantom", "poltergeist", "scary", "scream", "shadow", "skeleton", "skull",
        "specter", "spell", "spider", "spirit", "superstition", "tomb", "trick or treat", "undead", "unearthly",
        "unnerving", "vampire", "warlock", "werewolf", "witch", "wizard", "wraith", "zombie", "afraid", "afterlife",
        "alarming", "alien", "angel", "apparition", "astronaut", "autumn", "ballerina", "bat", "beast", "bizarre",
        "black", "black cat", "blood", "bloodcurdling", "bogeyman", "bone", "boo", "broomstick", "cackle", "cadaver",
        "candy", "cape", "carve", "casket", "cat", "cauldron", "cemetery", "chilling", "cloak", "clown", "cobweb",
        "coffin", "corpse", "costume", "cowboy", "cowgirl", "creepy", "crown", "crypt", "dark", "darkness", "dead",
        "death", "demon", "devil", "devilish", "disguise", "dreadful", "dress-up", "eerie", "elf", "enchant", "evil",
        "eyeballs", "eyepatch", "face paint", "fairy", "fall", "fangs", "fantasy", "fear", "firefighter", "flashlight",
        "fog", "fright", "frighten", "frightening", "frightful", "genie", "ghastly", "ghost", "ghostly", "ghoul",
        "ghoulish", "goblin", "goodies", "gory", "gown", "grave", "gravestone", "grim", "grim reaper", "grisly",
        "gruesome", "hair-raising", "halloween", "hat", "haunt", "haunted house", "hayride", "headstone", "hobgoblin",
        "hocus pocus", "horrible", "horrify", "howl", "imp", "jack-o'-lantern", "jumpsuit", "kimono", "king", "lantern",
        "macabre", "magic", "magic wand", "make-believe", "make-up", "mask", "masquerade", "mausoleum", "midnight",
        "mist", "monster", "moon", "moonlight", "moonlit", "morbid", "mummy", "mysterious", "night", "nightmare",
        "ninja", "october", "ogre", "orange", "otherworldly", "owl", "party", "petrify", "phantasm", "phantom",
        "pirate", "pitchfork", "poltergeist", "potion", "prank", "pretend", "prince", "princess", "pumpkin", "queen",
        "repulsive", "revolting", "robe", "robot", "scare", "scarecrow", "scary", "scream", "shadow", "shadowy",
        "shock", "shocking", "skeleton", "skull", "soldier", "specter", "spell", "spider", "spider web",
        "spine-chilling", "spirit", "spook", "spooky", "startling", "strange", "superhero", "supernatural",
        "superstition", "sweets", "tarantula", "terrible", "terrify", "thirty-first", "thrilling", "tiara", "toga",
        "tomb", "tombstone", "treat", "treats", "trick", "trick-or-treat", "troll", "tutu", "unearthly", "unnerving",
        "vampire", "vanish", "wand", "warlock", "web", "weird", "werewolf", "wicked", "wig", "witch", "witchcraft",
        "wizard", "wizardry", "wraith", "zombie", 'awful', 'disgusting', 'disturbing', 'eerie', 'frightening',
        'hideous', 'dead', 'haunted', 'rude', 'low', 'creepy', 'deceased', 'defiant', 'foul', 'sinful', 'bereftoflife',
        'horrid', 'divine', 'black', 'cold', 'up-to-no-good', 'holy', 'phantasmal', 'direful', 'ungodly', 'slimy',
        'ignominious', 'indecent', 'degrading', 'strange', 'threatening', 'pitiful', 'gross', 'spooky', 'gruesome',
        'grievous', 'distasteful', 'horrible', 'pagan', 'unearthly', 'objectionable', 'terrifying', 'offending',
        'weird', 'reprehensible', 'dark', 'frightful', 'alarming', 'nauseating', 'abusive', 'nasty', 'disreputable',
        'supernatural', 'scary', 'corpselike', 'obnoxious', 'abhorrent', 'monstrous', 'base', 'fearful', 'deadly',
        'shocking', 'superstitious', 'annoying', 'intense', 'contemptible', 'beastly', 'pale', 'minacious',
        'irritating', 'distressing', 'irreverent', 'dirty', 'uncanny', 'ghostlike', 'spectral', 'terrible', 'dire',
        'bad', 'disguised', 'godless', 'no-good', 'phantom', 'repulsive', 'illusory', 'rotten', 'biting', 'masked',
        'bloody', 'appalling', 'dreadful', 'sordid', 'formidable', 'off-color', 'odious', 'detestable', 'mean',
        'insolent', 'frozen', 'vampiric', 'spooked', 'infamous', 'lousy', 'ghostly', 'disgraceful', 'invidious',
        'horrific', 'cutting', 'unholy', 'baleful', 'blasphemous', 'scared', 'nightmarish', 'hair-raising', 'repugnant',
        'spiritual', 'wicked', 'grody', 'heathen', 'blood-curdling', 'violating', 'filthy', 'evil', 'desecrating',
        'horrendous', 'grisly', 'repellent', 'grim', 'undead', 'tragic', 'icky', 'cheap', 'loathsome', 'obscene',
        'abominable', 'haunting', 'menacing', 'ghastly', 'lifeless', 'wraithlike', 'worthless', 'macabre',
        'bone-chilling', 'trembling', 'moonlit', 'shadowy', 'atrocious', 'buried', 'deathlike', 'unhallowed',
        'chilling', 'low-life', 'wretched', 'vile', 'ominous', 'stiff', 'departed', 'godawful', 'ghoulish',
        'impertinent', 'offensive', 'sinister', 'costumed', 'cowardly', 'crawly', 'fear-inspiring', 'gory', 'haunting',
        'magical', 'mischievous', 'nighttime', 'startled', 'startlingawful', 'disgusting', 'disturbing', 'eerie',
        'frightening', 'hideous', 'dead', 'haunted', 'rude', 'low', 'creepy', 'deceased', 'defiant', 'foul', 'sinful',
        'bereftoflife', 'horrid', 'divine', 'black', 'cold', 'up-to-no-good', 'holy', 'phantasmal', 'direful', 'creepy',
        'haunted', 'insane', 'bat shit crazy',
    }
)

friendsgiving_prefixes = list(
    {
        'alien', 'revisionist-history'
    }
)


class Boo(BaseCog):
    def __init__(self, bot):
        self.bot = bot

    def prefix_nick(self, nick, wordlist=halloween_prefixes):
        return random.choice(wordlist) + ' ' + nick

    async def update_username(self, ctx, wordlist):
        user = ctx.message.author

        original_nick = user.nick or user.display_name

        new_nick = self.prefix_nick(original_nick, wordlist=wordlist)

        if len(new_nick) >= 32 or len(new_nick.split(' ')) > 3:
            base_nick = new_nick.split(' ')[-1]
            new_nick = self.prefix_nick(base_nick)

        new_nick = new_nick.title()

        try:
            await user.edit(nick=new_nick)
        except Exception as e:
            print(e)
            await ctx.send(user.mention + ' -> ' + new_nick)

    @commands.command()
    async def boo(self, ctx):
        await self.update_username(ctx, wordlist=halloween_prefixes)

    @commands.command()
    async def turkey(self, ctx):
        await self.update_username(ctx, wordlist=friendsgiving_prefixes)

    # @commands.command()
    # @checks.is_owner()
    # async def boo_all(self, ctx):
    #     for user in ctx.guild.members:
    #         original_nick = user.nick or user.display_name
    #
    #         new_nick = self.booify(original_nick)
    #
    #         try:
    #             await user.edit(nick=new_nick)
    #         except Exception as e:
    #             print(e)
    #             await ctx.send(user.mention + ' -> ' + new_nick)
