import discord
from redbot.core import commands
import random
import re
from functools import reduce

BaseCog = getattr(commands, "Cog", object)


class Zalgo(BaseCog):
    def __init__(self, bot):
        self.bot = bot

        async def april_fools(message):
            # Prevent acting on DM's
            it_isnt_april_fools = (
                random.random() <= 0.99
                or (message.guild is None)
            )

            if it_isnt_april_fools:
                return

            ctx = await self.bot.get_context(message)

            async with self.lock_config.channel(message.channel).get_lock():
                allowed: bool = await self.allowed(ctx, message)
                if not allowed:
                    return

                # new_msg = random.choice([self.uwuify, self.oobify])(message.content)
                new_msg = self.uwuify(message.content)

                await ctx.message.delete()
                await ctx.send(new_msg)
            await self.log_last_message(ctx, message)

        self.bot.add_listener(april_fools, "on_message")

    @commands.command()
    async def zalgo(self, ctx):
        """Zalgo the text"""
        # first pull out the .zalgo part of the message
        raw_msg = " ".join(ctx.message.clean_content.split(" ")[1:])
        if raw_msg == "":
            raw_msg = "HE COMES"

        # random intensity
        intensity = random.randint(50, 150)

        # zalgo characters to fuck with
        zalgo_chrs = [chr(x) for x in range(0x0300, 0x036F + 1)]
        zalgo_chrs += ["\u0488", "\u0489"]

        msg_array = list(raw_msg)
        for i in range(intensity):
            index = random.randint(0, len(msg_array) - 1)
            msg_array.insert(index, random.choice(zalgo_chrs))

        zalgo_msg = "".join(msg_array)

        await ctx.message.delete()
        await ctx.send(zalgo_msg)

    def uwuify(self, msg):
        replacements = {
            "r": "w",
            "R": "W",
            "l": "w",
            "L": "W",
            "this": "dis",
            "This": "Dis",
            "they": "dey",
            "They": "Dey",
            "there": "dere",
            "There": "Dere",
            "the": "da",
            "The": "Da",
        }

        new_msg = msg
        for regex, replacement in replacements.items():
            new_msg, _ = re.subn(regex, replacement, new_msg)

        new_msg += " *uwu*"

        return new_msg

    def oobify(self, msg):
        vowels = "aeiouy"
        first_pass = "".join(
            "oob" if (c in vowels and random.random() < 0.5) else c for c in msg
        )
        vowels = "AEIOUY"
        return "".join(
            "OOB" if (c in vowels and random.random() < 0.5) else c for c in first_pass
        )

    @commands.command()
    async def uwu(self, ctx):
        """uwu the text"""
        # first pull out the .zalgo part of the message
        raw_msg = " ".join(ctx.message.content.split(" ")[1:])
        if raw_msg == "":
            raw_msg = "uwu"

        new_msg = self.uwuify(raw_msg)

        await ctx.message.delete()
        await ctx.send(new_msg)

    @commands.command()
    async def oob(self, ctx):
        """oobs the text"""
        # first pull out the .zalgo part of the message
        raw_msg = " ".join(ctx.message.content.split(" ")[1:])
        if raw_msg == "":
            return

        new_msg = self.oobify(raw_msg)
        await ctx.send(new_msg)

    @commands.command()
    async def spoilerify(self, ctx, *msg):
        new_msg = []
        do_it = False
        for word in msg:
            if do_it:
                new_msg.append(f"||{word}||")
            else:
                new_msg.append(word)
            do_it = not do_it
        new_msg = " ".join(new_msg)

        await ctx.message.delete()
        await ctx.send(new_msg)
