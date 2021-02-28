import discord
from discord.ext import commands
import json
import os
from shutil import copyfile
import datetime

bot = commands.Bot(command_prefix='>')


async def userdata(ctx):
    if not os.path.isfile('userdata/' + str(ctx.author.id) + '.json'):
        copyfile('userdata/default.json', 'userdata/{0}.json'.format(str(ctx.author.id)))
    with open('userdata/{0}.json'.format(str(ctx.author.id)), 'r') as userdata:
        return json.load(userdata)


async def userdatadump(ctx, path, val):
    with open('userdata/{0}.json'.format(str(ctx.author.id)), 'r') as file:
        json_data = json.load(file)
        json_data.update({path: val})
    with open('userdata/{0}.json'.format(str(ctx.author.id)), 'w') as file:
        json.dump(json_data, file)


@bot.command()
async def bal(ctx):
    userdatajson = await userdata(ctx)
    await ctx.send("your current balance is: €" + str(userdatajson["bal"]))


@bot.command()
async def daily(ctx):
    userdatajson = await userdata(ctx)
    if userdatajson["last_daily"] != datetime.datetime.now().strftime('%Y' + '%j'):
        await userdatadump(ctx, "bal", int(userdatajson["bal"] + 250))
        await userdatadump(ctx, "last_daily", datetime.datetime.now().strftime('%Y' + '%j'))
        await ctx.send("added €250 to your account. your balance is now €" + str(userdatajson["bal"] + 250))
    else:
        await ctx.send("you really thought you could trick me FOOL? :clown::rofl:")


with open('token.txt', 'r') as token:
    bot.run(token.read())
