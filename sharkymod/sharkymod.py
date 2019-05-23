import discord
from redbot.core import commands, checks
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS


class SharkyMod(commands.cog):
    """Sharky Moderation Tools"""

    __author__ = "Sharky The King"
    __version__ = "1.0.0"

#  Sharky's Userinfo twist
    @commands.command(name="sharkinfo", aliases=['pinfo'])
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, send_messages=True)
    async def sharkinfo(self, ctx, *, member: discord.Member):
        """
        User information with Sharky's twist
        """
        member_mention = member.mention  # Mentions
        member_disc = member.discriminator  # The four digits
        member_name = member.name  # Default Discord name
        member_id = member.id  # USERID
        member_avatar = member.avatar_url_as(static_format="png")  # Avatar, static is formated as png
        member_voice = member.voice  # Tells us the voice chat they're in
        member_bot = member.bot

        member_role = sorted(member.roles)[1:]  # this and line 35 are required for role formats
        if member_role:  # this lets us format the roles properly so theyr'e named correctly
            member_role = ", ".join([x.mention for x in member_role])  # Changed x.name to x.mention to ping the roles for color
        notice = "Puppy Shark"
        
        #  Tie this together with created_on and joined_on
        #  Credit to Red Core Userinfo command: I am not this smart yet :eyes:
        joined_at = member.joined_at  # This is REQUIRED for 'since_joined`
        member_joined = member.joined_at.strftime("%d %b %Y %H:%M")  # When the user joined the server
        since_joined = (ctx.message.created_at - joined_at).days  # Since the user joined the server in days
        member_created = member.created_at.strftime("%d %b %Y %H:%M")  # When the user account was created
        since_created = (ctx.message.created_at - member.created_at).days  # Since the user account was created in days

        created_on = ("{}\n({} days ago)").format(member_created, since_created)  # Formats when the account was created into a proper day message
        joined_on = ("{}\n({} days ago)").format(member_joined, since_joined)  # Formats when the account joined the server into a proper day message

    #   Embeds
        embed = discord.Embed(color=0xEE2222, title=f'{member_name}\'s information')
        embed.add_field(name='Name:', value=f'{member_mention}\n{member_name}#{member_disc}', inline=True)
        embed.add_field(name='ID:', value=f'{member_id}', inline=True)
        if member_bot is True:  # this is to define if a person is...well...a bot
            embed.add_field(name='Bot:', value=f"{member_mention} is a bot", inline=False)
        embed.add_field(name="Account Creation:", value=f'{created_on}', inline=True)
        embed.add_field(name="Joined Date:", value=f'{joined_on}', inline=True)
        embed.add_field(name='Roles:', value=f'{member_role}', inline=False)
        if member_voice and member_voice.channel:  # this formats the voice call chunk into a proper message
            embed.add_field(name="Current voice channel", value="<#{0.id}> (ID: {0.id})".format(member_voice.channel), inline=False)
    # Non-fielded embedsets
        embed.set_footer(text=f'{notice}')
        embed.set_thumbnail(url=member_avatar)
        embed.set_author(name=f'{member_name}#{member_disc}', icon_url=f'{member_avatar}')  
        await ctx.send(embed=embed)

#   Trying to find if user is banned in Discord.
    @commands.command()
    @commands.bot_has_permissions(ban_members=True, embed_links=True, send_messages=True)  # Makes sure the bot has the proper permissions to do this command.
    @checks.mod_or_permissions(manage_messages=True)  #  This makes sure a person has to be a mod or have ban_members permission to use.
    @commands.guild_only()
    async def findban(self, ctx, *, banneduser):
        """Check if a user is banned"""
        guild = ctx.guild  # Self explained
        bot = ctx.bot  # Self explained
        try:  # This tries to see if member works, if it doesn't it'll error out without this
            member = await bot.fetch_user(banneduser)  # Contains the bot.fetch_user
        except discord.NotFound:
            embed = discord.Embed(color=0xEE2222, title='Unknown User')
            embed.add_field(name=f'Not Valid', value=f'{banneduser} is not a Valid User\n Please make sure you\'re using a correct UserID.\nHow you ask? [Go here](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)')
            return await ctx.send(embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(color=0xEE2222, title='Invalid Input')
            embed.add_field(name='ID10T Error:', value=f'**{banneduser}** is not a valid input...but you knew that, didn\'t you?')
            return await ctx.send(embed=embed)
        mid = banneduser
        hammer = 'https://cdn.discordapp.com/attachments/575846797709279262/578793294897741835/ban.png'
        x_emote = 'https://media.discordapp.net/attachments/541131861687009296/579467209676554240/emoji.png'
        #  This is where the command actually works. If a ban is found it'll output that it was found
        #   If the ban isn't found, it'll error and thus cause the discord.NotFound exception
        try:
            tban = await guild.fetch_ban(await bot.fetch_user(banneduser))
            #   embeds
            embed = discord.Embed(color=0xEE2222, title='Ban Found')
            embed.add_field(name=f'User Found:', value=f'{member}\n({mid})', inline=True)
            embed.add_field(name=f'Ban reason:', value=f'{tban[0]}', inline=False)
            embed.set_thumbnail(url=hammer)
            return await ctx.send(embed=embed)
        # Exception that if the person isn't found banned
        except discord.NotFound:
            embed = discord.Embed(color=0xEE2222, title='Ban **NOT** Found')
            embed.add_field(
                name=f'They are not banned from the server.',
                value=f'{member} ({mid})')
            embed.set_thumbnail(url=x_emote)
            return await ctx.send(embed=embed)

#   User Avatar
    @commands.command()
    @commands.bot_has_permissions(embed_links=True, send_messages=True)
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def av(self, ctx, *, user: discord.Member):
        """A user's avatar"""
        user_mention = user.mention  # Mentions
        user_disc = user.discriminator  # The four digits
        user_name = user.name  # Default Discord name
        user_id = user.id  # USERID
        user_av = user.avatar_url_as(static_format="png")  # Avatar, static is formated as png

        #  Tie this together with created_on and joined_on
        #  Credit to Red Core Userinfo command: I am not this smart yet :eyes:
        joined_at = user.joined_at  # This is REQUIRED for 'since_joined`
        user_joined = user.joined_at.strftime("%d %b %Y %H:%M")  # When the user joined the server
        since_joined = (ctx.message.created_at - joined_at).days  # Since the user joined the server in days
        user_created = user.created_at.strftime("%d %b %Y %H:%M")  # When the user account was created
        since_created = (ctx.message.created_at - user.created_at).days  # Since the user account was created in days

        created_on = ("{}\n({} days ago)").format(user_created, since_created)  # Formats when the account was created into a proper day message
        joined_on = ("{}\n({} days ago)").format(user_joined, since_joined)  # Formats when the account joined the server into a proper day message

        embed = discord.Embed(color=0xEE2222, title=f'Avatar Info')
        embed.add_field(name=f'User Info:', value=f'{user_mention}\n({user_id})')
        embed.add_field(name=f'Discord Name:', value=f'{user_name}#{user_disc}')
        embed.add_field(name=f'Account Age:', value=f'{created_on}')
        embed.add_field(name=f'Join Date:', value=f'{joined_on}')
        embed.set_image(url=user_av)
        await ctx.send(embed=embed)

#   User menu, combinds most if not all of the commands together
    @commands.command(name="usermenu", aliases=['umenu', 'userm', 'um'])
    @commands.bot_has_permissions(embed_links=True, send_messages=True, add_reactions=True)
    @commands.guild_only()
    async def _umenu(self, ctx, *, member: discord.Member):
        """Ties all of the commands together, but in a menu! :D"""
        embeds = []

    # This is the list of definitions
        member_mention = member.mention  # Mentions
        member_disc = member.discriminator  # The four digits
        member_name = member.name  # Default Discord name
        member_id = member.id  # USERID
        member_avatar = member.avatar_url_as(static_format="png")  # Avatar, static is formated as png
        member_voice = member.voice  # Tells us the voice chat they're in
        member_bot = member.bot

        member_role = sorted(member.roles, reverse=True)[:-1]  # this and if member_role are required for role formats
        if member_role:  # this lets us format the roles properly so theyr'e named correctly
            member_role = ", ".join([x.mention for x in member_role])
        else:
            member_role = None  # changed x.name to x.mention to make it ping the roles

        #  Tie this together with created_on and joined_on
        #  Credit to Red Core Userinfo command: I am not this smart yet :eyes:
        joined_at = member.joined_at  # This is REQUIRED for 'since_joined`
        member_joined = member.joined_at.strftime("%d %b %Y %H:%M")  # When the user joined the server
        since_joined = (ctx.message.created_at - joined_at).days  # Since the user joined the server in days
        member_created = member.created_at.strftime("%d %b %Y %H:%M")  # When the user account was created
        since_created = (ctx.message.created_at - member.created_at).days  # Since the user account was created in days

        created_on = ("{}\n({} days ago)").format(member_created, since_created)  # Formats when the account was created into a proper day message
        joined_on = ("{}\n({} days ago)").format(member_joined, since_joined)  # Formats when the account joined the server into a proper day message

    # This is where the magic will hopefully happen
        for x in map(str, range(1, 4)):
            first = discord.Embed(
                color=0xEE2222,
                title=f'{member_name}\'s information')
            first.add_field(
                name='Name:',
                value=f'{member_mention}\n{member_name}#{member_disc}',
                inline=True)
            first.add_field(
                name='ID:',
                value=f'{member_id}',
                inline=True)
            if member_bot is True:  # this is to define if a person is...well...a bot
                first.add_field(
                    name=('Bot:'),
                    value=(f"{member_mention} is a bot"),
                    inline=False)
            if member_voice and member_voice.channel:  # this formats the voice call chunk into a proper message
                first.add_field(name="Current voice channel", value="<#{0.id}> (ID: {0.id})".format(member_voice.channel), inline=False)
            first.set_thumbnail(url=member_avatar)
            embeds.append(first)
            second = discord.Embed(color=0xEE2222, title=f'{member_name}\'s information')
            second.add_field(name="Account Creation:", value=f'{created_on}', inline=True)
            second.add_field(name="Joined Date:", value=f'{joined_on}', inline=True)
            if member_role is not None:
                second.add_field(name='Roles:', value=f'{member_role}', inline=False)
            second.set_thumbnail(url=member_avatar)
            embeds.append(second)
            third = discord.Embed(
                color=0xEE2222,
                title=f'{member_name}\'s Avatar')
            third.set_image(url=member_avatar)
            embeds.append(third)
        await menu(ctx, embeds, DEFAULT_CONTROLS)