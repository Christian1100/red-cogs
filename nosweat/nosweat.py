import asyncio
from contextlib import suppress

import discord
from discord.ext import tasks
from discord import Embed, Guild, Member, Role
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context, Greedy, group
from discord.utils import get

from redbot.core import checks, Config, commands
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS

import requests
from discord import Webhook, RequestsWebhookAdapter

#----------------# CONFIG #----------------#

role_id = 721988422041862195
reaction_name = '<:fnit_gift:601709109955395585>'
message_id = 721990614228664361
webhook_id = 721997644955779102
welcome_channel_id = 603955376286728226
welcome_messages = ['{user}, benvenuto nel team No Sweat!', '{user}? Il team No Sweat ti stava aspettando!', 'Team No Sweat, finalmente anche {user} è qui con noi!']

#------------------------------------------#

class NoSweat(commands.Cog):
  """Role reaction and give the welcome by webhook to a specific channel"""
  def __init__(self, bot):
    self.bot = bot
    
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
    # Vars
    guild = self.bot.get_guild(payload.guild_id)
    role = get(guild.roles, id=role_id)
    welcome_channel = get(guild.channels, id=welcome_channel_id)
    if not guild:
      return
    member = guild.get_member(payload.user_id)

    # Reaction Role
    if member is None:
        return
    if role in member.roles:
        return
    if payload.emoji.name == reaction_name:
        await member.add_roles(role)

    # Embed
    random_message = random.choice(welcome_messages)
    embed = discord.Embed(description="{user}, benvenuto!".replace("{user}", member.mention), color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
    embed.set_author(name=member.display_name, icon_url=member.user.avatar_url)
    embed.set_footer(text=guild.name, icon_url=guild.icon_url)

    # Welcome Webhook
    hooks = await welcome_channel.webhooks()
    hook = get(hooks, id=webhook_id)
    await hook.send(embed=embed)
