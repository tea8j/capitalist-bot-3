import discord
from discord.ext import commands
import json
import os
from shutil import copyfile
import datetime
import random


bot = commands.Bot(command_prefix='>')


async def userdata(ctx):
    if not os.path.isfile('userdata/' + str(ctx.author.id) + '.json'):
        copyfile('userdata/default.json', 'userdata/{0}.json'.format(str(ctx.author.id)))
    with open('userdata/{0}.json'.format(str(ctx.author.id)), 'r') as userdata:
        return json.load(userdata)


async def userdatadump(ctx, path, val):
    with open('userdata/{0}.json'.format(str(ctx.author.id)), 'r') as file:
        print(val)
        json_data = json.load(file)
        json_data.pop(path)
        json_data[path] = val
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


@bot.command()
async def work(ctx):
    b10code = random.randint(1,18446744073709551615)
    hexcode = hex(b10code)[2:]
    await ctx.author.send("go to https://cb3.t8j.monster/jobs/bird/" + hexcode + " to work")


@bot.command()
async def buypet(ctx, pet):
    if pet == "dog":
        userdatajson = await userdata(ctx)
        if userdatajson["bal"] >= 500:
            pet = list(userdatajson["pets"])
            pet.append("dog")
            await userdatadump(ctx, "pets", pet)
            await userdatadump(ctx, "bal", userdatajson["bal"] - 500)
            await ctx.send("you have purchased a dog :dog:")
        else:
            await ctx.send("you are poor so no dog for you :clown::rofl:")
    else:
        await ctx.send("that's not a pet :clown:")


@bot.command()
async def pets(ctx):
    userdatajson = await userdata(ctx)
    await ctx.send(userdatajson["pets"])


with open('token.txt', 'r') as token:
    bot.run(token.read())
